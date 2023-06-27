# EPICS *StreamDevice*

## What is *StreamDevice*?

*StreamDevice* is a generic [EPICS](https://epics.anl.gov/){target="ex"}
device support for devices with a \"byte stream\" based communication
interface. That means devices that can be controlled by sending and
receiving strings (in the broadest sense, including non-printable
characters and even null-bytes). Examples for this type of communication
interface are serial line (RS-232, RS-485, \...), IEEE-488 (also known
as GPIB or HP-IB), and telnet-like TCP/IP.

*StreamDevice* is not limited to a specific device type or manufacturer
nor is it necessary to re-compile anything to support a new device type.
Instead, it can be configured for any device type with [*protocol
files*](protocol.html) in plain ASCII text which describes the commands
a device understands and the replies it sends. If the device can be
controlled with strings like \"[RF:FREQ 499.655 MHZ]{.kbd}\"
*StreamDevice* can be used. Formatting and parsing of values is done
with [*format converters*](formats.html) similar to those known from the
C functions *printf()* and *scanf()*. To support other formats, it is
possible to [write your own converters](formatconverter.html).

Each record with *StreamDevice* support runs one protocol from the
protocol file to read or write its value. Protocols can be as simple as
just one output string or can consist of many strings sent to and read
from the device. However, a protocol is linear. That means it runs from
start to end each time the record is [processed](processing.html). It
does not provide loops or branches.

*StreamDevice* comes with an interface to
[*asynDriver*](https://www.aps.anl.gov/epics/modules/soft/asyn/){target="ex"}
but can be extended to [support other bus drivers](businterface.html).
Note that *StreamDevice* is not an alternative or replacement but a
supplement for *asynDriver*. *StreamDevice* converts record values to
and from strings but leaves it to *asynDriver* (or other bus interfaces)
to exchange these strings with the device. Thus any bus type supported
by *asynDriver* (to be exact by *asynOctet*) can automatically be used
with *StreamDevice*.

*StreamDevice* supports all [standard records](recordtypes.html) of
EPICS base which can have device support. It is also possible to [write
support for new record types](recordinterface.html).

## What is *StreamDevice* not?

It is not a programming language for a high-level application. It is,
for example, not possible to write a complete scanning program in a
protocol. Use other tools for that and use *StreamDevice* only for the
primitive commands.

It is not a block oriented device support. It is not intended for huge
binary blocks of data that contain many process variables distributed
over many records. Consider
[*regDev*](https://github.com/paulscherrerinstitute/regdev){target="ex"}
for that.

It is not a very flexible html, xml, json, etc. parser. Data needs to
come in a predictible order to be parsable by *StreamDevice*.

## Recommended Readings

IOC Application Developer\'s Guide:
[R3.14.12](https://epics.anl.gov/base/R3-14/12-docs/AppDevGuide/){target="ex"},
[R3.15.6](https://epics.anl.gov/base/R3-15/6-docs/AppDevGuide/AppDevGuide.html){target="ex"},
[R3.16.2](https://epics.anl.gov/base/R3-16/2-docs/AppDevGuide/AppDevGuide.html){target="ex"}

[EPICS Record Reference
Manual](https://wiki-ext.aps.anl.gov/epics/index.php/RRM_3-14){target="ex"}

## Color and Style Conventions

In this document, code is witten in `green fixed width font`. This marks
text you typically type in configuration files etc.

    Longer code segments are often set in a box.

## Changes in Version 2.8

-   Support standard EPICS module build system.
-   Compatible with EPICS 7.
    -   Support for new record types: int64in, int64out, lsi, lso.
    -   Support for INT64 and UINT64 in aai, aao, waveform.
-   Run \@init more often (e.g. when device re-connects or paused IOC is
    resumed).
-   Use \"COMM\" error code in .STAT when device is disconnected.
-   Allow spaces in protocol parameter list.
-   Support output redirect of all shell functions.
-   Fix building shared libraries on Windows.
-   Fix some C++11 warnings.
-   Fix several signed/unsigned problems.
-   Dropped support for cygnus-2.7.2 gcc (used by some old cygwin).
-   Several bug fixes.
-   Several documentation updates.

[Next: Setup](setup.html) Dirk Zimoch, 2018
