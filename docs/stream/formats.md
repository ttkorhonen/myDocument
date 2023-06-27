# Format Converters

[]{#syntax}

## 1. Format Syntax

*StreamDevice* format converters work very similar to the format
converters of the C functions *printf()* and *scanf()*. But
*StreamDevice* provides more different converters and you can also write
your own converters. Formats are specified in [quoted
strings](protocol.html#str) as arguments of `out` or `in`
[commands](protocol.html#cmd).

A format converter consists of

-   The `%` character
-   Optionally a field or record name in `()`
-   Optionally flags out of the characters `*# +0-?=!`
-   Optionally an integer *width* field
-   Optionally a period character (`.`) followed by an integer
    *precision* field (input ony for most formats)
-   A conversion character
-   Additional information required by some converters

An exception is the sequence `%%` which stands for a single literal `%`.
This has been added for compatibility with the C functions *printf()*
and *scanf()*. It behaves the same as the escaped percent `\%`.

The flags `*# +0-` work like in the C functions *printf()* and
*scanf()*. The flags `?`, `=` and `!` are extensions.

The `*` flag skips data in input formats. Input is consumed and parsed,
a mismatch is an error, but the read data is dropped. This is useful if
input contains more than one value. Example: `in "%*f%f";` reads the
second floating point number.

The `#` flag may alter the format, depending on the converter (see
below).

The \'` `\' (space) and `+` flags usually print a space or a `+` sign
before positive numbers, where negative numbers would have a `-`. Some
converters may redefine the meaning of these flags (see below).

The `0` flag usually says that numbers should be left padded with `0` if
*width* is larger than required. Some converters may redefine the
meaning of this flag (see below).

The `-` flag usually specifies that output is left justified if *width*
is larger than required. Some converters may redefine the meaning of
this flag (see below).

The `?` flag makes failing input conversions succeed with a default zero
value (0, 0.0, or \"\", depending on the format type).

The `=` flag allows to compare input with current values. It is only
allowed in input formats. Instead of reading a new value from input, the
current value is formatted (like for output) and then compared to the
input.

The `!` flag demands that input is exactly *width* bytes long (normally
*width* defines the maximum number of bytes read in many formats). This
feature has been added by Klemen Vodopivec, SNS.

### Examples:

`in "%f";`

Read a float value

`out "%(HOPR)7.4f";`

Write the HOPR field as 7 char float with precision 4

`out "%#010x";`

Write a 0-padded 10 char hex integer using the alternative format (with
leading 0x)

`in "%[_a-zA-Z0-9]";`

Read a string of alphanumerical chars or underscores

`in "%*i";`

Skip over an integer number

`in "%?d";`

Read a decimal number or if that fails pretend that value was 0

`in "%=.3f";`

Assure that the input is equal to the current value formatted as a float
with precision 3

`in "%!5d";`

Expect exactly 5 decimal digits. Fewer digits are considered loss of
data and make the format fail.

`in "%d%%";`

Read a decimal number followed by a % sign

[]{#types}

## 2. Data Types and Record Fields

### Default fields

Every conversion character corresponds to one of the data types DOUBLE,
LONG, ULONG, ENUM, or STRING. In contrast to to the C functions
*printf()* and *scanf()*, it is not required to specify a variable for
the conversion. The variable is typically the `VAL` or `RVAL` field of
the record, selected automatically depending on the data type. Not all
data types make sense for all record types. Refer to the description of
[supported record types](recordtypes.html) for details.

*StreamDevice* makes no difference between `float` and `double` nor
between `short`, `int` and `long` values. Thus, data type modifiers like
`l` or `h` do not exist in *StreamDevice* formats.

[]{#redirection}

### I/O Redirection to other records or fields

To use formats with other than the default fields of a record or even
with fields of other records on the same IOC, use the syntax
`%(``record`{.variable}`.``FIEL`{.variable}`D)`. If only a field name
but no record is given, the active record is assumed. If only a record
name but no field name is given, the `VAL` field is assumed.

**Example 1:** `out "%(EGU)s";` outputs the `EGU` field of the active
record.

**Example 2:** `in "%(``otherrecord`{.variable}`.RVAL)i";` stores the
received integer value in the `RVAL` field of the other record and then
processes that record. The other record should probably use
`DTYP="Raw Soft Channel"` in order to convert `RVAL` to `VAL`.

**Example 3:** `in "%(``otherrecord`{.variable}`)f";` stores the
received floating point value in the `VAL` field of the other record and
then processes that record. The other record should probably use
`DTYP="Soft Channel"`. In the unlikely case that the name of the other
record is the same as a field of the active record (e.g. if you name a
record \"DESC\"), then use `.VAL` explicitly to refer to the record
rather than the field of the active record.

This feature is quite useful in the case that one line of input contains
more than one value that need to be stored in multiple records or if one
line of output needs to be contructed from values of multiple records.
In order to avoid using full record names in the protocol file, it is
recommended to pass the name or part of the name (e.g. the device
prefix) of the other record as a [protocol
argument](protocol.html#argvar). In that case the redirection usually
looks like this: `in "%(\$1``recordpart`{.variable}`)f"` and the record
calls the protocol like this:
`field(INP, "@``protocolfile`{.variable}` ``protocol`{.variable}`($(PREFIX)) $(PORT)")`
using a macro for the prefix part which is then used for `\$1`.

If the other record is passive and the field has the PP attribute (see
[Record Reference
Manual](http://www.aps.anl.gov/asd/controls/epics/EpicsDocumentation/AppDevManuals/RecordRef/Recordref-1.html){target="ex"}),
the record will be processed. It is your responsibility that the data
type of the record field is compatible to the the data type of the
converter. STRING formats are compatible with arrays of CHAR or UCHAR.

Be aware that using this syntax is by far not as efficient as using the
default field. At the moment it is not possible to set the other record
to an alarm state if anything fails. It will simply not be processed if
the fault happens before or while handling it and it will already have
been processed if the fault happens later.

### Pseudo-converters

Some formats are not actually converters. They format data which is not
stored in a record field, such as a [checksum](#chksum) or [regular
expression substitution](#regsub). No data type corresponds to those
*pseudo-converters* and the `%(`*`FIELD`*`)` syntax cannot be used.

[]{#stdd}

## 3. Standard DOUBLE Converters (`%f`, `%e`, `%E`, `%g`, `%G`)

**Output:** `%f` prints fixed point, `%e` prints exponential notation
and `%g` prints either fixed point or exponential depending on the
magnitude of the value. `%E` and `%G` use `E` instead of `e` to separate
the exponent.

With the `#` flag, output always contains a period character.

**Input:** All these formats are equivalent. Leading whitespaces are
skipped.

With the `#` flag additional whitespace between sign and number is
accepted.

When a maximum field width is given, leading whitespace only counts to
the field witdth when the space flag is used.

[]{#stdl}

## 4. Standard LONG and ULONG Converters (`%d`, `%i`, `%u`, `%o`, `%x`, `%X`)

**Output**: `%d` and `%i` print signed decimal, `%u` unsigned decimal,
`%o` unsigned octal, and `%x` or `%X` unsigned hexadecimal. `%X` uses
upper case letters.

With the `#` flag, octal values are prefixed with `0` and hexadecimal
values with `0x` or `0X`.

Unlike printf, `%x` and `%X` truncate the output to the the given width
(number of least significant half bytes).

**Input:** `%d` matches signed decimal, `%u` matches unsigned decimal,
`%o` unsigned octal. `%x` and `%X` both match upper or lower case
unsigned hexadecimal. Octal and hexadecimal values can optionally be
prefixed. `%i` matches any integer in decimal, or prefixed octal or
hexadecimal notation. Leading whitespaces are skipped.

With the `-` negative octal and hexadecimal values are accepted.

With the `#` flag additional whitespace between sign and number is
accepted.

When a maximum field width is given, leading whitespace only counts to
the field witdth when the space flag is used.

[]{#stds}

## 5. Standard STRING Converters (`%s`, `%c`)

**Output:** `%s` prints a string. If *precision* is specified, this is
the maximum string length. `%c` is a LONG format in output, printing one
character!

**Input:** `%s` matches a sequence of non-whitespace characters and `%c`
matches a sequence of not-null characters. The maximum string length is
given by *width*. The default *width* is infinite for `%s` and 1 for
`%c`. Leading whitespaces are skipped with `%s` except when the space
flag is used but not with `%c`. The empty string matches.

With the `#` flag `%s` matches a sequence of not-null characters instead
of non-whitespace characters.

With the `0` flag `%s` pads with 0 bytes instead of spaces.

[]{#cset}

## 6. Standard Charset STRING Converter (`%[`*`charset`*`]`)

This is an input-only format. It matches a sequence of characters from
*charset*. If *charset* starts with `^`, the format matches all
characters [not]{.underline} in *charset*. Leading whitespaces are not
skipped.

Example: `%[_a-z]` matches a string consisting entirely of `_`
(underscore) or letters from `a` to `z`.

[]{#enum}

## 7. ENUM Converter (`%{`*`string0`*`|`*`string1`*`|...}`)

This format maps an unsigned integer value on a set of strings. The
value 0 corresponds to *string0* and so on. The strings are separated by
`|`.

Example: `%{OFF|STANDBY|ON}` mapps the string `OFF` to the value 0,
`STANDBY` to 1 and `ON` to 2.

When using the `#` flag it is allowed to assign integer values to the
strings using `=`. Unassigned strings increment their values by 1 as
usual.

If one string is the initial substing of another, the substing must come
later to ensure correct matching. In particular if one string is the
emptry string, it must be the last one because it always matches. Use
`#` and `=` to renumber if necessary.

Use the assignment `=?` for the last string to make it the default value
for output formats.

Example: `%#{neg=-1|stop|pos|fast=10|rewind=-10}`.

If one of the strings contains `|` or `}` (or `=` if the `#` flag is
used) a `\` must be used to escape the character.

**Output:** Depending on the value, one of the strings is printed, or
the default if given and no value matches.

**Input:** If any of the strings matches, the value is set accordingly.

[]{#bin}

## 8. Binary LONG or ULONG Converter (`%b`, `%B`*`zo`*)

This format prints or scans an unsigned integer represented as a binary
string (one character per bit). The `%b` format uses the characters `0`
and `1`. With the `%B` format, you can choose two other characters to
represent zero and one. With the `#` flag, the bit order is changed to
*little endian*, i.e. least significant bit first.

Examples: `%B.!` or `%B\x00\xff`. `%B01` is equivalent to `%b`.

In output, if *width* is larger than the number of significant bits,
then the flag `0` means that the value should be padded with with the
chosen zero character instead of spaces. If *precision* is set, it means
the number of significant bits. Otherwise, the highest 1 bit defines the
number of significant bits.

In input, leading spaces are skipped. A maximum of *width* characters is
read. Conversion stops with the first character that is not the zero or
the one character.

[]{#raw}

## 9. Raw LONG or ULONG Converter (`%r`)

The raw converter does not really \"convert\". A signed or unsigned
integer value is written or read in the internal (usually two\'s
complement) representation of the computer. The normal byte order is
*big endian*, i.e. most significant byte first. With the `#` flag, the
byte order is changed to *little endian*, i.e. least significant byte
first. With the `0` flag, the value is unsigned, otherwise signed.

In output, the *precision* (or sizeof(long) whatever is less) least
significant bytes of the value are sign extended or zero extended
(depending on the `0` flag) to *width* bytes. The default for
*precision* is 1. Thus if you do not specify the *precision*, only the
least significant byte is written! It is common error to write
`out "%2r";` instead of `out "%.2r";`.

In input, *width* bytes are read and put into the value. If *width* is
larger than the size of a `long`, only the least significant bytes are
used. If *width* is smaller than the size of a `long`, the value is sign
extended or zero extended, depending on the `0` flag.

Examples: `out "%.2r"; in "%02r";`

[]{#rawdouble}

## 10. Raw DOUBLE Converter (`%R`)

The raw converter does not really \"convert\". A float or double value
is written or read in the internal (maybe IEEE) representation of the
computer. The normal byte order is *big endian*, i.e. most significant
byte first. With the `#` flag, the byte order is changed to *little
endian*, i.e. least significant byte first. The *width* must be 4
(float) or 8 (double). The default is 4.

[]{#bcd}

## 11. Packed BCD (Binary Coded Decimal) LONG or ULONG Converter (`%D`)

Packed BCD is a format where each byte contains two binary coded decimal
digits (`0` \... `9`). Thus a BCD byte is in the range from `0x00` to
`0x99`. The normal byte order is *big endian*, i.e. most significant
byte first. With the `#` flag, the byte order is changed to *little
endian*, i.e. least significant byte first. The `+` flag defines that
the value is signed, using the upper half of the most significant byte
for the sign. Otherwise the value is unsigned.

In output, *precision* decimal digits are printed in at least *width*
output bytes. Signed negative values have `0xF` in their most
significant half byte followed by the absolute value.

In input, *width* bytes are read. If the value is signed, a one in the
most significant bit is interpreted as a negative sign. Input stops with
the first byte (after the sign) that does not represent a BCD value,
i.e. where either the upper or the lower half byte is larger than 9.

[]{#chksum}

## 12. Checksum Pseudo-Converter (`%<`*`checksum`*`>`)

This is not a normal \"converter\", because no user data is converted.
Instead, a checksum is calculated from the input or output. The *width*
field is the byte number from which to start calculating the checksum.
Default is 0, i.e. the first byte of the input or output of the current
command. The last byte is *precision* bytes before the checksum (default
0). For example in `"abcdefg%<xor>"` the checksum is calculated from
`abcdefg`, but in `"abcdefg%2.1<xor>"` only from `cdef`.

Normally, multi-byte checksums are in *big endian* byteorder, i.e. most
significant byte first. With the `#` flag, the byte order is changed to
*little endian*, i.e. least significant byte first.

The `0` flag changes the checksum representation to hexadecimal ASCII (2
chars per checksum byte).

The `-` flag changes the checksum representation to \"poor man\'s hex\":
0x30 \... 0x3f (2 chars per checksum byte).

The `+` flag changes the checksum representation to decimal ASCII
(formatted with %d).

In output, the checksum is appended.

In input, the next byte or bytes must match the checksum.

### Implemented checksum functions

`%<sum>` or `%<sum8>`
:   One byte. The sum of all characters modulo 2^8^.

`%<sum16>`
:   Two bytes. The sum of all characters modulo 2^16^.

`%<sum32>`
:   Four bytes. The sum of all characters modulo 2^32^.

`%<negsum>`, `%<nsum>`, `%<-sum>`, `%<negsum8>`, `%<nsum8>`, or `%<-sum8>`
:   One byte. The negative of the sum of all characters modulo 2^8^.

`%<negsum16>`, `%<nsum16>`, or `%<-sum16>`
:   Two bytes. The negative of the sum of all characters modulo 2^16^.

`%<negsum32>`, `%<nsum32>`, or `%<-sum32>`
:   Four bytes. The negative of the sum of all characters modulo 2^32^.

`%<notsum>` or `%<~sum>`
:   One byte. The bitwise inverse of the sum of all characters modulo
    2^8^.

`%<xor>`
:   One byte. All characters xor\'ed.

`%<xor7>`
:   One byte. All characters xor\'ed & 0x7F.

`%<crc8>`
:   One byte. An often used 8 bit crc checksum (poly=0x07, init=0x00,
    xorout=0x00).

`%<ccitt8>`
:   One byte. The CCITT standard 8 bit crc checksum (poly=0x31,
    init=0x00, xorout=0x00, reflected).

`%<crc16>`
:   Two bytes. An often used 16 bit crc checksum (poly=0x8005,
    init=0x0000, xorout=0x0000).

`%<crc16r>`
:   Two bytes. An often used reflected 16 bit crc checksum (poly=0x8005,
    init=0x0000, xorout=0x0000, reflected).

`%<modbus>`
:   Two bytes. The modbus 16 bit crc checksum (poly=0x8005, init=0xffff,
    xorout=0x0000, reflected)

`%<ccitt16>`
:   Two bytes. The usual (but
    [wrong?](http://srecord.sourceforge.net/crc16-ccitt.html){target="ex"})
    implementation of the CCITT standard 16 bit crc checksum
    (poly=0x1021, init=0xFFFF, xorout=0x0000).

`%<ccitt16a>`
:   Two bytes. The unusual (but
    [correct?](http://srecord.sourceforge.net/crc16-ccitt.html){target="ex"})
    implementation of the CCITT standard 16 bit crc checksum with
    augment. (poly=0x1021, init=0x1D0F, xorout=0x0000).

`%<ccitt16x>` or `%<crc16c>` or `%<xmodem>`
:   Two bytes. The XMODEM checksum. (poly=0x1021, init=0x0000,
    xorout=0x0000).

`%<crc32>`
:   Four bytes. The standard 32 bit crc checksum. (poly=0x04C11DB7,
    init=0xFFFFFFFF, xorout=0xFFFFFFFF).

`%<crc32r>`
:   Four bytes. The standard reflected 32 bit crc checksum.
    (poly=0x04C11DB7, init=0xFFFFFFFF, xorout=0xFFFFFFFF, reflected).

`%<jamcrc>`
:   Four bytes. Another reflected 32 bit crc checksum. (poly=0x04C11DB7,
    init=0xFFFFFFFF, xorout=0x00000000, reflected).

`%<adler32>`
:   Four bytes. The Adler32 checksum according to [RFC
    1950](http://www.ietf.org/rfc/rfc1950.txt){target="ex"}.

`%<hexsum8>`
:   One byte. The sum of all hex digits. (Other characters are ignored.)

`%<lrc>`
:   One byte. The Longitudinal Redundancy Check according to
    [Wikipedia](https://en.wikipedia.org/wiki/Longitudinal_redundancy_check){target="ex"}.

`%<hexlrc>`
:   One byte. The LRC for the hex digits. (Other characters are
    ignored.)

`%<leybold>`
:   One byte. Used by some Leybold products. 255-bytesum%255 (+32 if
    result would be \<32)

`%<brksCryo>`
:   One byte. Used by Brooks Cryopumps.

`%<CPI>`
:   One byte. Used by TRIUMF CPI RF amplifier.

`%<bitsum>` or `%<bitsum8>`
:   One byte. Number of 1 bits in all characters.

`%<bitsum16>`
:   Two bytes. Number of 1 bits in all characters.

`%<bitsum32>`
:   Four bytes. Number of 1 bits in all characters.

[]{#regex}

## 13. Regular Expresion STRING Converter (`%/`*`regex`*`/`)

This input-only format matches [Perl compatible regular expressions
(PCRE)](http://www.pcre.org/){target="ex"}. It is only available if a
PCRE library is installed.

::: box
If PCRE is not available for your host or cross architecture, download
the sourcecode from [www.pcre.org](https://www.pcre.org/){target="ex"}
and try my EPICS compatible
[Makefile](http://epics.web.psi.ch/software/streamdevice/pcre/Makefile){target="ex"}
to compile it like a normal EPICS support module. The Makefile is known
to work with EPICS 3.14.8 and PCRE 7.2. In your RELEASE file define the
variable `PCRE` so that it points to the install location of PCRE.

If PCRE is already installed on (some of) your systems, you may add
architectures where PCRE can be found in standard include and library
locations to the variable `WITH_SYSTEM_PCRE`. If either the header file
or the library are in a non-standard place, set in your RELEASE file the
variables `PCRE_INCLUDE_`*`arch`* and/or `PCRE_LIB_`*`arch`* for the
respective architectures to the correct directories or set
`PCRE_INCLUDE` and/or `PCRE_LIB` in architecture specific
RELEASE.Common.*arch* files.
:::

If the regular expression is not anchored, i.e. does not start with `^`,
leading non-matching input is skipped. To match in multiline mode
(across newlines) add `(?m)` at the beginning of the pattern. To match
case insensitive, add `(?i)`.

A maximum of *width* bytes is matched, if specified. If *precision* is
given, it specifies the sub-expression in `()` whose match is returned.
Otherwise the complete match is returned. In any case, the complete
match is consumed from the input buffer. If the expression contains a
`/` it must be escaped like `\/`.

Example: `%.1/<title>(.*)<\/title>/` returns the title of an HTML page,
skipps anything before the `<title>` tag and leaves anything after the
`</title>` tag in the input buffer.

[]{#regsub}

## 14. Regular Expresion Substitution Pseudo-Converter (`%#/`*`regex`*`/`*`subst`*`/`)

This is a variant of the previous converter (note the `#`) but instead
of returning the matching string, it can be used as a pre-processor for
input or as a post-processor for output.

Matches of the *regex* are replaced by the string *subst* with all `&`
in *subst* replaced with the match itself and all `\1` through `\9`
replaced with the match of the corresponding sub-expression [ if such a
sub-expression exists. Occurrences of `\U`*`n`*, `\L`*`n`*, `\u`*`n`*,
or `\l`*`n`* with *`n`* being a number `0` through `9` or `&` are
replaced with the corresponding sub-expression converted to all upper
case, all lower case, first letter upper case, or first letter lower
case, respectively.]{.new}

[ Due to limitations of the parser, `\1` and `\x01` are the same which
makes it difficult to use literal bytes with values lower than 10 in
*subst*. Therefore `\0` aways means a literal byte (incompatible change
from earlier version!) and `\1` through `\9` mean literal bytes if they
are larger than the number of sub-expressions. ]{.new} To get a literal
`&` or `\` or `/` in the substitution write `\&` or `\\` or `\/`.

If *width* is specified, it limits the number of characters processed.
If the `-` flag is used (i.e. *width* looks like a negative number) only
the last *width* characters are processed, else the first. Without
*width* (or 0) all available characters are processed.

If *precision* is specified, it indicates which matches to replace. With
the `+` flag given, *precision* is the maximum number of matches to
replace. Otherwise *precision* is the index (counting from 1) of the
match to replace. Without *precision* (or 0), all matches are replaced.

When replacing multiple matches, the next match is searched directly
after the currently replaced string, so that the *subst* string itself
will never be modified recursively. [ However if an empty string is
matched, searching advances by 1 character in order to avoid matching
the same empty string again.]{.new}

In input this converter pre-processes data received from the device
before following converters read it. Converters preceding this one will
read unmodified input. Thus place this converter before those whose
input should be pre-processed.

In output it post-processes data already formatted by preceding
converters before sending it to the device. Converters following this
one will send their output unmodified. Thus place this converter after
those whose output should be post-processed.

Examples:

::: indent
`%#+-10.2/ab/X/` replaces the string `ab` with `X` maximal 2 times in
the last 10 characters. (`abcabcabcabc` becomes `abcXcXcabc`)
:::

::: indent
`%#/\\/\//` replaces all `\` with `/` (`\dir\file` becomes `/dir/file`)
:::

::: indent
`%#/..\B/&:/` inserts `:` after every second character which is not at
the end of a word. (`0b19353134` becomes `0b:19:35:31:34`)
:::

::: indent
`%#/://` removes all `:` characters. (`0b:19:35:31:34` becomes
`0b19353134`)
:::

::: indent
`%#/([^+-])*([+-])/\2\1/` moves a postfix sign to the front. (`1.23-`
becomes `-1.23`)\
:::

::: indent
`%#-2/.*/\U0/` converts the previous 2 characters to upper case.
:::

[]{#mantexp}

## 15. MantissaExponent DOUBLE converter (`%m`)

This exotic and experimental format matches numbers in the format
*\[sign\] mantissa sign exponent*, e.g `+123-4` meaning 123e-4 or
0.0123. Mantissa and exponent are decimal integers. The sign of the
mantissa is optional. Compared to the standard `%e` format, this format
does not contain the characters `.` and `e`.

Output formatting is ambigous (e.g. `123-4` versus `1230-5`). I chose
the following convention: Format *precision* defines number of digits in
mantissa. No leading \'0\' in mantissa (except for 0.0 of course).
Number of digits in exponent is at least 2. Format flags `+`, `-`, and
space are supported in the usual way (always sign, left justified, space
instead of + sign). Flags `#` and `0` are unsupported.

[]{#timestamp}

## 16. Timestamp DOUBLE converter (`%T(`*`timeformat`*`)`)

This format reads or writes timestamps and converts them to a double
number. The value represents the number of seconds since 1970 (the UNIX
epoch). The precision of a double is large enough for microseconds (but
not for nanoseconds). This format is probably used best in combination
with a redirection to the `TIME` field. In this case, the value is
converted to EPICS timestamps (seconds since 1990 and nanoseconds). The
timestamp format understands the usual converters that the C function
*strftime()* understands. In addition, fractions of a second can be
specified and the time zone can be set in the format string.

Example: `%(TIME)T(%d %b %Y %H:%M:%.3S %z)` may print something like
` 3 Sep 2010 15:45:59 +0200`.

Fractions of a second can be specified as `%.`*`n`*`S` (seconds with *n*
fractional digits), as `%0`*`n`*`f` or `%`*`n`*`f` (*n* fractional
digits) or as `%N` (nanoseconds). In input, *n* is the maximum number of
digits parsed, there may be actually less digits in the input. If *n* is
not specified (`%.S` or `%f`) it uses a default value of 6.

In input, the time zone can be specified in the format like `%+`*`hhmm`*
or `%-`*`hhmm`* for cases where the parsed time stamp does not specify
the time zone, where *hhmm* is a 4 digit number specifying the offset in
hours and minutes.

In output, the system function *strftime()* is used to format the time.
There may be differences in the implementation between operating
systems.

In input, *StreamDevice* uses its own implementation because many
systems are missing the *strptime()* function and additional formats are
supported.

Day of the week can be parsed but is ignored because the information is
redundant when used together with day, month and year and more or less
useless otherwise. No check is done for consistency.

Because of the complexity of the problem, locales are not supported.
Thus, only the English month names can be used (week day names are
ignored anyway).

[Next: Record Processing](processing.html) Dirk Zimoch, 2018
