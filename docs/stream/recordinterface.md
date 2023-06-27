# Record API

[]{#theory}

## Theory of Operation

*StreamDevice* implements the generic part of an EPICS device support.
However it cannot know the internals of a specific record type, such as
the .VAL or .RVAL fields or the .INP or .OUT links. It can only access a
record as dbCommon. Thus it is necessary to write an interface for each
record type which takes care of these details.

A record interface consists of three functions, `readData()` and
`writeData()` and `initRecord()`.

The record interface also implements the device support structure for
this record type. Most of its functions will be generic *StreamDevice*
functions. The exception is `initRecord()`.

The name of the device support structure must have the form
`dev``recordtype`{.variable}`Stream` and the name of the record
interface source code file must be
`dev``recordtype`{.variable}`Stream.c` to work seamlessly with the build
system implemented in the Makefile of *StreamDevice*.

Finally add `recordtype`{.variable} to the `RECORDTYPES` variable in the
file src/CONFIG_STREAM and rebuild.

[]{#headers}

Headers to Include

A record interface typically `#include`s the header file for the
supported record type, `"``recordtype`{.variable}`Record.h"` and
`"devStream.h"`. For many record interfaces this is sufficient, but
sometimes additional header files may be needed.

[]{#functions}

Functions to Implement

A record interface has to implement three functions:

::: indent
` static long readData(dbCommon *record, format_t *format); `
:::

::: indent
` static long writeData(dbCommon *record, format_t *format); `
:::

::: indent
` static long initRecord(dbCommon *record); `
:::

#### writeData

The function `writeData()` is called whenever a
[protocol](protocol.html#proto) needs to handle a prining [format
converter](formats.html) (without
[redirection](formats.html#redirection)), typically in an `out` command.
It is also possible that `writeData()` is called for an input record,
e.g. when the [`=` flag](formats.html#syntax) is used in an `in`
command. Thus implement this function for input records as well.

The functions is called with a `dbCommon *record` argument, which the
function should cast to the specific record type to get access to the
record specific fields, in particular .VAL and .RVAL.

The second argument, `format_t *format`, contains information about the
format converter. The only field of interest in this argument is
`format->type` which specifies the data type of the format conversion.
Its value is one of `DBF_ULONG`, `DBF_ULONG`, `DBF_ENUM`, `DBF_DOUBLE`,
or `DBF_STRING`.

The `writeData()` function may access different fields depending on
`format->type`, e.g. .VAL for `DBF_DOUBLE` but .RVAL for `DBF_LONG`. It
also may interpret the fields in a different way, e.g. cast to `long`
for `DBF_LONG` but to `unsigned long` for `DBF_ULONG`. This is typically
done with a `switch(format->type)` statement.

The function may refuse to handle `format->type` values that make no
sense for the record type, e.g. `DBF_STRING` for a record type that
cannot handle strings. In that case the function should return `ERROR`.
It is a good idea to return `ERROR` in the `default` part of the
`switch` statement.

*StreamDevice* provides a function to output a value from the record:

::: indent
` long streamPrintf(dbCommon *record, format_t *format, ...); `
:::

Once the correct record field and type cast has been chosen, the
`writeData()` function calls
`return streamPrintf(record, format, value)` where the type of value
should match `field->type` (`long`, `unsigned long`, `double`, or
`char*`), returning the result of that call.

**Example:**

    static long writeData(dbCommon *record, format_t *format)
    {
        recordtypeRecord *rec = (recordtypeRecord *)record;

        switch (format->type)
        {
            case DBF_ULONG:
            case DBF_ENUM:
                return streamPrintf(record, format, (unsigned long)rec->rval);
            case DBF_LONG:
                return streamPrintf(record, format, (long)rec->rval);
            case DBF_DOUBLE:
                return streamPrintf(record, format, rec->val);
            default:
                return ERROR;
        }
    }

#### readData

The arguments of this function are the same as for `writeData()`. But
this function stores a value into record fields depending on
`format->type`.

*StreamDevice* provides two functions to receive a value;

::: indent
` ssize_t streamScanf(dbCommon *record, format_t *format, void* value); `
:::

::: indent
` ssize_t streamScanfN(dbCommon *record, format_t *format, void* value, size_t maxStringSize); `
:::

The argument `value` is a pointer to the variable where the value is to
be stored. Its type must match `field->type` (`long*`, `unsigned long*`,
`double*`, or `char*`).

The `streamScanfN()` function is meant for strings and gets the
additional argument `maxStringSize` to specify the size of the string
buffer.

The `streamScanf()` function is actually a macro calling
`streamScanfN()` with `MAX_STRING_SIZE` (=40) for the last argument. For
`field->type` values other than `DBF_STRING`, this argument is ignored.

In case of strings, these functions return the number of characters
actually stored (which may be less than `maxStringSize`). Some record
types may want to store this value into a field of the record.

The functions return `ERROR` on failure. In this case the `readData()`
function should return `ERROR` as well. Otherwise the function should
store the value received into the appropriate record field.

If `record->pact` is `true`, the function should now return `OK` or
`DO_NOT_CONVERT` (=2), depending on wheter conversion from .RVAL to .VAL
should be left to the record or not.

If `record->pact` is `false`, the record is curretly executing the
`@init` handler. This typically only affects output records. As the
record is not processed by EPICS at this time, changes in fields would
not trigger monitor updates.

Also the record will not convert .RVAL to .VAL in this case, thus the
`readData()` function should now convert .RVAL to .VAL as usually done
by the record.

In order to make monitors work properly, the `readData()` function
should then first call `recGblResetAlarms()` and then call
`db_post_events()` as needed. Usually the code from the record support
function `monitor()` needs to be copied. Unfortunately the `monitor()`
function of the record cannot be called directly because it is `static`.

**Example:**

    static long readData(dbCommon *record, format_t *format)
    {
        recordtypeRecord *rec = (recordtypeRecord *)record;
        unsigned long rval;
        unsigned short monitor_mask;

        switch (format->type)
        {
            case DBF_ULONG:
            case DBF_LONG:
            case DBF_ENUM:
                if (streamScanf(record, format, &rval) == ERROR) return ERROR;
                rec->rval = rval;
                if (record->pact) return OK;
                /* emulate convertion to val */
                rec->val = rval * rec->eslo + rec->eoff;
                break;
            case DBF_DOUBLE:
                if (streamScanf(record, format, &rec->val) == ERROR) return ERROR;
                break;
                if (record->pact) return DO_NOT_CONVERT;
            default:
                return ERROR;
        }
        /* In @init handler, no processing, enforce monitor updates. */
        monitor_mask = recGblResetAlarms(record);
        if (rec->oraw != rec->rval)
        {
            db_post_events(record, &rec->rval, monitor_mask | DBE_VALUE | DBE_LOG);
            rec->oraw = rec->rval;
        }
        if (!(fabs(rec->mlst - rec->val) <= rec->mdel))
        {
            monitor_mask |= DBE_VALUE;
            ao->mlst = rec->val;
        }
        if (!(fabs(rec->alst - rec->val) <= rec->adel))
        {
            monitor_mask |= DBE_VALUE;
            ao->alst = rec->val;
        }
        if (monitor_mask)
            db_post_events(record, &rec->val, monitor_mask);
        return OK;
    }

#### initRecord

The main purpose of this function is to pass the .INP or .OUT link to
*StreamDevice* for parsing and to make the two functions `readData` and
`writeData` known. Often the only thing the `initRecord()` function does
is to call `streamInitRecord()` and return its result.

::: indent
` long streamInitRecord(dbCommon *record, const struct link *ioLink, streamIoFunction readData, streamIoFunction writeData); `
:::

    static long initRecord(dbCommon *record)
    {
        recordtypeRecord *rec = (recordtypeRecord *)record;

        return streamInitRecord(record, &rec->out, readData, writeData);
    }

### Device Support Structure

For most record types the device support structure contains 5 functions,
`report`, `init`, `init_record`, `get_ioint_info`, and `read` or
`write`. Few other record typess, for examle ai and ao may have
additional functions. For most of these functions simply pass one of the
provided *StreamDevice* functions `streamReport`, `streamInit`,
`streamGetIoInitInfo`, and `streamRead` or `streamWrite`. Only for
`init_record` pass your own `initRecord` function. Then export the
structure.

    struct {
        long number;
        DEVSUPFUN report;
        DEVSUPFUN init;
        DEVSUPFUN init_record;
        DEVSUPFUN get_ioint_info;
        DEVSUPFUN write;
    } devrecordtypeStream = {
        5,
        streamReport,
        streamInit,
        initRecord,
        streamGetIointInfo,
        streamWrite
    };

    epicsExportAddress(dset,devrecordtypeStream);

Dirk Zimoch, 2018
