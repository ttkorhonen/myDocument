# Format Converter API

[]{#class}

## Converter Class

A user defined converter class inherits public from
*StreamFormatConverter* and handles one or more conversion characters.
It is not necessary that a given conversion character supports both,
printing and scanning. But if it does, both must be handled by the same
converter class.

Any conversion corresponds to one data type. The converter class must
implement print and/or scan methods for this data type. It must also
implement a parse method to analyse the format string.

A converter class must be registered with a call to RegisterConverter()
in the global file context.

The converter must not contain any class variables, because there will
be only one global instance for each conversion character - not one for
each format string!

### Example: LONG converter for `%Q`

    #include "StreamFormatConverter.h"

    class MyConverter : public StreamFormatConverter
    {
        int parse(const StreamFormat&, StreamBuffer&, const char*&, bool);
        bool printLong(const StreamFormat&, StreamBuffer&, long);
        ssize_t scanLong(const StreamFormat&, const char*, long&);
    };

    RegisterConverter(MyConverter,"Q");

    // ... (implementation)

[]{#theory}

## Theory of Operation

[]{#registration}

### Registration

::: indent
` RegisterConverter(`*`converterClass`*`, "`*`characters`*`"); `
:::

This macro registers the converter class for all given conversion
characters. In most cases, you will give only one character. The macro
must be called once for each class in the global file context.

HINT: Do not branch depending on the conversion character. Provide
multiple classes, that\'s more efficient.

[]{#parsing}

### Parsing

::: indent
` int parse(const StreamFormat& fmt, StreamBuffer& info, const char*& source, bool scanFormat); `
:::

::: indent
` struct StreamFormat { char conv; StreamFormatType type; unsigned short flags; long prec; unsigned long width; unsigned long infolen; const char* info; }; `
:::

During initialization, `parse()` is called whenever one of the
conversion characters handled by your converter class is found in a
protocol. The fields `fmt.conv`, `fmt.flags`, `fmt.prec`, and
`fmt.width` have already been filled in. If a scan format is parsed,
`scanFormat` is `true`. If a print format is parsed, `scanFormat` is
`false`.

The `fmt.flags` field is a bitset and can have any of the following
flags set:

-   `left_flag`: the format contained a `-`. This is normaly used to
    indicate that the value should be printed left-aligned.
-   `sign_flag`: the format contained a `+`. This normaly requests to
    print a sign even for positive numbers.
-   `space_flag`: the format contained a \'` `\' (space). This normaly
    requests to print a space instead of a sign for positive numbers.
-   `alt_flag`: the format contained a `#`. This indicated the request
    to use an alternative format. For example in `%#x` the hex number is
    preficed with `0x`.
-   `zero_flag`: the format contained a `0`. This normaly requests to
    pad a numerical value with leading zeros instead of leading spaces.
-   `skip_flag`: the format contained a `*`. The value is parsed and
    checked but then discarded.

It is not necessary that these flags have exactly the same meaning in
your formats, but a similar and intuitive meaning is helpful for the
user.

There are two additional flags, `default_flag` indicating a `?` and
`compare_flag` indicating a `=` in the format, that are handled
internally by *StreamDevice* and are not of interest to the converter
class.

The `source` pointer points to the character of the format string just
after the conversion character. You can parse additional characters if
they belong to the format string handled by your class. Move the
`source` pointer so that is points to the first character after your
format string. This is done for example in the builtin formats
`%[charset]` or `%{enum0|enum1}`. However, many formats don\'t need
additional characters.

#### Example

     source       source
     before       after
     parse()      parse()
         |         |
    "%39[0-9a-zA-Z]constant text"
        |
     conversion
     character

You can write any data you may need later in `print*()` or `scan*()` to
the [*Streambuffer*](streambuffer.html) `info`. This will probably be
necessary if you have parsed additional characters from the format
string as in the above example\

Return `unsigned_format`, `signed_format`, `double_format`,
`string_format`, or `enum_format` depending on the datatype associated
with the conversion character. It is not necessary to return the same
value for print and for scan formats. You can even return different
values depending on the format string.

If the format is not a real data conversion but does other things with
the data (append or check a checksum, encode or decode the data,\...),
return `pseudo_format`.

Return `false` if there is any parse error or if print or scan is
requested but not supported by this conversion or flags are used that
are not supported by this conversion.

[]{#printing_scanning}

### Printing and Scanning

Provide a `print[Long|Double|String|Pseudo]()` and/or
`scan[Long|Double|String|Pseudo]()` method appropriate for the data type
you have returned in the `parse()` method. That method is called
whenever the conversion appears in an output or input, respectively. You
only need to implement the flavour of print and/or scan suitable for the
datatype returned by `parse()`. Both `unsigned_format` and
`signed_format` will use the `Long` flavour.

The possible interface methods are:

::: indent
` bool printLong(const StreamFormat& fmt, StreamBuffer& output, long value); `
:::

::: indent
` bool printDouble(const StreamFormat& fmt, StreamBuffer& output, double value); `
:::

::: indent
` bool printString(const StreamFormat& fmt, StreamBuffer& output, const char* value); `
:::

::: indent
` bool printPseudo(const StreamFormat& fmt, StreamBuffer& output); `
:::

::: indent
` ssize_t scanLong(const StreamFormat& fmt, const char* input, long& value); `
:::

::: indent
` ssize_t scanDouble(const StreamFormat& fmt, const char* input, double& value); `
:::

::: indent
` ssize_t scanString(const StreamFormat& fmt, const char* input, char* value, size_t& size); `
:::

::: indent
` ssize_t scanPseudo(const StreamFormat& fmt, StreamBuffer& inputLine, size_t& cursor); `
:::

Now, `fmt.type` contains the value returned by `parse()`. With
`fmt.info()` get access to the string you have written to `info` in
`parse()` (null terminated).

The length of the info string can be found in `fmt.infolen`.

In `print*()`, append the converted value to `output`. Do not modify
what is already in output (unless you really know what you\'re doing,
e.g. some `printPseudo` methods). Return `true` on success, `false` on
failure.

In `scan*()`, read the value from input and return the number of
consumed bytes or -1 on failure. If the `skip_flag` is set, you don\'t
need to write to `value`, since the value will be discarded anyway. In
`scanString()`, don\'t write more bytes than `maxlen` to `value` and set
`size` to the actual string length, which may be different to the number
of bytes consumed (e.g. if leading spaces are skipped). In
`scanPseudo()`, `cursor` is the index of the first byte in `inputLine`
to consider, which may be larger than `0`.

Dirk Zimoch, 2018
