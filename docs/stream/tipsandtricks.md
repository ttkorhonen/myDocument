# Tips and Tricks

[]{#argvar}

## I have many almost identical protocols

You can give [arguments](protocol.html#argvar) to a protocol. In the
`INP` or `OUT` link, write:

` field (OUT, "@protocolfile protocol(arg1,arg2,arg3) bus") `

In the protocol, reference arguments as `$1 $2 $3` or inside strings as
`"\$1 \$2 \$3"`.

` moveaxis {out "move\$1 %.6f";}`\
`field (OUT, "@motor.proto moveaxis(X) motor1") `

` readpressure {out 0x02 0x00 $1; in 0x82 0x00 $1 "%2r";}`\
`field (INP, "@vacuumgauge.proto readpressure(0x84) gauge3") `

[]{#iointr}

## I have a device that sends unsolicited data

Use [`I/O Intr` processing](processing.html#iointr). The record receives
any input and processes only when the input matches.

` read {in "new value = %f";} `

` record (ai, "$(RECORD)") {`\
`  field (DTYP, "stream")`\
`  field (INP, "@$(DEVICETYPE).proto read $(BUS)")`\
`  field (SCAN, "I/O Intr")`\
`} `

[]{#multiline}

## I have a device that sends multi-line messages

    Here is the value:
    3.1415

Use as many `in` commands as you get input lines.

` read_value {in "Here is the value:"; in "%f";} `

[]{#writemany}

## I need to write more than one value in one message

There is more than one solution to this problem. Different approaches
have different requirements.

### A) All values have the same type and are separated by the same string

Use array records (e.g. [waveform](waveform.html), [aao](aao.html)).

` array_out {separator=", "; out "an array: (%.2f)";} `

The format `%.2f` is repeated for each element of the array. All
elements are separated by `", "`.\
Output will look like this:

    an array: (3.14, 17.30, -12.34)

### B) We have up to 12 numeric values

Use a [calcout](calcout.html) record and [redirection to
fields](formats.html#redirection).

` write_ABC {out "A=%(A).2f B=%(B).6f C=%(C).0f";} `

You must specify a valid expression in the `CALC` field even if you
don\'t use it.

` record (calcout, "$(RECORD)") {`\
`  field (INPA, "$(A_RECORD)")`\
`  field (INPB, "$(B_RECORD)")`\
`  field (INPC, "$(C_RECORD)")`\
`  field (CALC, "0")`\
`  field (DTYP, "stream")`\
`  field (OUT, "@$(DEVICETYPE).proto write_ABC $(BUS)")`\
`} `

### C) Values are in other records on the same IOC

Use [redirection to records](formats.html#redirection).

` acquire {out 'ACQUIRE "%(\$1:directory)s/%s",%(\$1:time).3f;';} `

You can specify a record name or record.FIELD in parentheses directly
after the `%`. To avoid plain record names in protocol files use
[protocol arguments](protocol.html#argvar) like `\$1`. In the link,
specify the record name or just the basename of the other records
(device name) in parentheses.

` record (stringout, "$(DEVICE):getimage") {`\
`  field (DTYP, "stream")`\
`  field (OUT, "@$(DEVICETYPE).proto acquire($(DEVICE)) $(BUS)")`\
`} `

[]{#readmany}

## I need to read more than one value from one message

Again, there is more than one solution to this problem.

### A) All values have the same type and are separated by the same string

Use array records (e.g. [waveform](waveform.html), [aai](aai.html)).\

` array_in {separator=","; in "array = (%f)";} `

The format `%f` is repeated for each element of the array. A `","` is
expected beween element.\
Input may look like this:

    array = (3.14, 17.30, -12.34)

### B) The message and the values in it can be filtered easily

Use [`I/O Intr` processing](processing.html#iointr) and [value
skipping](formats.html#syntax) (`%*`)\

` read_A {out "GET A,B"; in "A=%f, B=%*f";}`\
`read_B {in "A=%*f, B=%f";} `

` record (ai, "$(DEVICE):A") {`\
`  field (DTYP, "stream")`\
`  field (INP, "@$(DEVICETYPE).proto read_A $(BUS)")`\
`  field (SCAN, "1 second")`\
`}`\
`record (ai, "$(DEVICE):B") {`\
`  field (DTYP, "stream")`\
`  field (INP, "@$(DEVICETYPE).proto read_B $(BUS)")`\
`  field (SCAN, "I/O Intr")`\
`} `

Record A actively requests values every second. The reply contains
values A and B. Record A filters only value A from the input and ignores
value B by using the `*` flag. Nevertheless, a complete syntax check is
performed: B must be a valid floating point number. Record B is
`I/O Intr` and gets (a copy of) any input, including input that was
directed to record A. If it finds a matching string it ignores value A,
reads value B and then processes. Any non-matching input is ignored by
record B.

### C) Values should be stored in other records on the same IOC

Use [redirection to records](formats.html#redirection). To avoid record
names in protocol files, use [protocol arguments](protocol.html#argvar).

` read_AB {out "GET A,B"; in "A=%f, B=%(\$1)f";} `

` record (ai, "$(DEVICE):A") {`\
`  field (DTYP, "stream")`\
`  field (INP, "@$(DEVICETYPE).proto read_AB($(DEVICE):B) $(BUS)")`\
`  field (SCAN, "1 second")`\
`}`\
`record (ai, "$(DEVICE):B") {`\
`} `

Whenever record A reads input, it stores the first value in its own VAL
field as usual and the second in the VAL field of record B. Because the
VAL field of record B has the PP attribute, this automatically processes
record B.

[]{#mixed}

## I have a device that sends mixed data types: numbers or strings

Use a `@mismatch` [exception handler](protocol.html#except) and
[redirection to records](formats.html#redirection). To avoid record
names in protocol files, use [protocol arguments](protocol.html#argvar).

### Example

When asked \"`CURRENT?`\", the device send something like
\"`CURRENT 3.24 A`\" or a message like \"`device switched off`\".

` read_current {out "CURRENT?"; in "CURRENT %f A"; @mismatch {in "%(\$1)39c";}} `

` record (ai, "$(DEVICE):readcurrent") {`\
`  field (DTYP, "stream")`\
`  field (INP, "@$(DEVICETYPE).proto read_current($(DEVICE):message) $(BUS)")`\
`}`\
`record (stringin, "$(DEVICE):message") {`\
`} `

After [processing](processing.html#proc) the readcurrent record, you can
see from SEVR/STAT if the read was successful or not. With some more
records, you can clean the message record if SEVR is not INVALID.

` record (calcout, "$(DEVICE):clean_1") {`\
`  field (INPA, "$(DEVICE):readcurrent.SEVR CP")`\
`  field (CALC, "A#3")`\
`  field (OOPT, "When Non-zero")`\
`  field (OUT, "$(DEVICE):clean_2.PROC")`\
`}`\
`record (stringout, "$(DEVICE):clean_2") {`\
`  field (VAL, "OK")`\
`  field (OUT, "$(DEVICE):message PP")`\
`}`\
[]{#web}

## I need to read a web page

First you have to send a correctly formatted HTML header for a GET
request. Note that this header must contain the full URL like
\"http://server/page\" and must be terminated with [two]{.underline} CR
LF sequences (`"\r\n\r\n"` or `CR LF CR LF`). The server should be the
same as in the [`drvAsynIPPortConfigure`](setup.html#sta) command (if
not using a http proxy). The web page you get often contains much more
information than you need. [Regular expressions](formats.html#regex) are
great to find what you are looking for.

### Example 1

Read the title of a web page.

` get_title {`\
`  extrainput = ignore;`\
`  replyTimeout = 1000;`\
`  out "GET http://\$1\r\n\r\n";`\
`  in "%+.1/(?im)<title>(.*)<\/title>/";`\
`} `

Terminate the request with two carriage return + newlines, either
explicit like here [or]{.underline} using an
[`outTerminator`](protocol.html#sysvar). The URI (without http:// but
including the web server host name) is passed as
[argument](protocol.html#argvar) 1 to `\$1` in this example. Note that
web servers may be slow, so allow some
[`replyTimeout`](protocol.html#argvar).

If you don\'t use an `inTerminator` then the whole page is read as one
\"line\" to the `in` command and can be parsed easily with a regular
expression. We want to see the string between `<title>` and `</title>`,
so we put it into a subexpression in `()` and request the first
subexpression with `.1`. Note that the `/` in the closing tag has be be
escaped to avoid a misinterpretation as the closing `/` of the regular
expression.

The tags may be upper or lower case like `<TITLE>` or `<Title>`, so we
ask for case insensitive matching with `(?i)`.

The string should be terminated with the first closing `</title>`, not
the last one in the file. (There should not be more than one title but
you never know.) Thus we ask not to be greedy with `(?m)`. `(?i)` and
`(?m)` can be combined to `(?im)`. See the PCRE documentation for more
regexp syntax.

The regular expression matcher ignores and discards any content before
the matching section. Content after the match is discarded with
`extrainput = ignore` so that it does not trigger errors reporting
\"surplus input\".

Finally, the title may be too long for the record. The `+` tells the
format matcher not to fail in this case but to truncate the string
instead. You can read the string with a stringin record or for longer
strings with a waveform record with data type CHAR.

` record (stringin, "$(DEVICE):title") {`\
`  field (DTYP, "stream")`\
`  field (INP, "@$(DEVICETYPE).proto get_title($(PAGE)) $(BUS)")`\
`}`\
`record (waveform, "$(DEVICE):longtitle") {`\
`  field (DTYP, "stream")`\
`  field (INP, "@$(DEVICETYPE).proto get_title($(PAGE)) $(BUS)")`\
`  field (FTVL, "CHAR")`\
`  field (NELM, "100")`\
`}`\

### Example 2

Read a number from a web page. First we have to locate the number. For
that we match against any known string right before the number (and
[discard the match](formats.html#syntax) with `*`). Then we read the
number.

` get_title {`\
`  extrainput = ignore;`\
`  replyTimeout = 1000;`\
`  out "GET http://\$1\r\n\r\n";`\
`  in "%*/Interesting value:/%f more text";`\
`} `

When using `extrainput = ignore;`, it is always a good idea to match a
few bytes after the value, too. This catches errors where loading of the
page is interrupted in the middle of the number. (You don\'t want to
miss the exponent from something like 1.23E-14).

You can read more than one value from a file with successive regular
expressions and [redirections](formats.html#redirection). But this only
works if the order of the values is predictible. *StreamDevice* is not
an XML parser! It always reads sequentially.

Dirk Zimoch, 2018
