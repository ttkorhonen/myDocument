# Setup

[]{#pre}

## 1. Prerequisites

*StreamDevice* works with [EPICS
base](https://epics.anl.gov/base/index.php) versions from R3.14.6 on,
tested up to 7.0.3. It also works (with limitations) with older
[R3.13](https://epics.anl.gov/base/R3-13.php) versions from R3.13.7 on.
How to use *StreamDevice* with EPICS R3.13 is described on a [separate
page](epics3_13.html).

Download and build the EPICS version of your choice first before
continuing.

### Fix required for base R3.14.8.2 and earlier on Windows

Up to release R3.14.8.2, a fix in EPICS base is required to build
*StreamDevice* on Windows (not cygwin). Add the following line to
[src/iocsh/iocsh.h]{.kbd} and rebuild base.

    epicsShareFunc int epicsShareAPI iocshCmd(const char *command);

### Downloading *StreamDevice*

The latest version of StreamDevice can be found on github:
<https://github.com/paulscherrerinstitute/StreamDevice>. Either download
a [zip
file](https://github.com/paulscherrerinstitute/StreamDevice/archive/master.zip%0A)
or clone the git repo:

    git clone https://github.com/paulscherrerinstitute/StreamDevice.git

### Configuration

*StreamDevice* now comes with a standard [configure]{.kbd} directory.
~~But it can still be built in an external *\<top\>* directory as in
previous versions. It will automatically detect *\<top\>* locations from
the presence of [../configure]{.kbd} or [../config]{.kbd} directories.~~
Using an upper level [../configure]{.kbd} is no longer supported due to
compatibility issues with *SynApps*.

Edit the [configure/RELEASE]{.kbd} file to specify the install location
of EPICS base and of additional software modules or add a
[configure/RELEASE.local]{.kbd} file to overwrite, for example:

    EPICS_BASE=/home/epics/base-3.16.1

#### Support for *asynDriver*

You most probably want to have *asynDriver* support included, because
that is the standard way for *StreamDevice* to talk to hardware. First
get and install
[*asynDriver*](https://www.aps.anl.gov/epics/modules/soft/asyn/) version
4-3 or higher before you build *StreamDevice*. I have tested
*StreamDevice* with *asynDriver* versions up to 4-30. Make sure that the
*asyn* library can be found by adding the path to the *\<top\>*
directory of your *asyn* installation to the [configure/RELEASE]{.kbd}
file:

    ASYN=/home/epics/asyn4-30

#### Support for *sCalcout* record

The
[*sCalcout*](https://htmlpreview.github.io/?https://raw.githubusercontent.com/epics-modules/calc/R3-6-1/documentation/sCalcoutRecord.html)
record is part of [*synApps*](https://www.aps.anl.gov/BCDA/synApps). If
*streamDevice* should be built with support for this record, you have to
install at least the [*calc*
module](https://epics.anl.gov/bcda/synApps/calc/calc.html) from
*SynApps* first. Add references to the [RELEASE]{.kbd} file as shown
here:

    CALC=/home/epics/synApps/calc-R3-6-1

Up to *calc* release R2-6 (*synApps* release R5_1), the *sCalcout*
record needs a fix. (See separate [*scalcout* page](scalcout.html).) And
the *calc* module had dependencies on other *SynApps* modules. Release
R2-8 or newer is recommended.

Support for the *sCalcout* is optional. *StreamDevice* works as well
without *sCalcout* or *SynApps*.

#### Support for regular expression matching

If you want to enable regular expression matching, you need the *PCRE*
package. For most Linux systems, it is already installed. In that case
tell *StreamDevice* the locations of the *PCRE* header file and library.
However, the pre-installed package can only by used for the host
architecture. Thus, add them not to [RELEASE]{.kbd} but to
[RELEASE.Common.linux-x86]{.kbd} (if linux-x86 is your EPICS_HOST_ARCH).
Be aware that different Linux distributions may locate the files in
different directories.

    PCRE_INCLUDE=/usr/include/pcre
    PCRE_LIB=/usr/lib

For 64 bit installations, the path to the library may be different:

    PCRE_INCLUDE=/usr/include/pcre
    PCRE_LIB=/usr/lib64

A pre-compiled Windows version of *PCRE* is available at
[sourceforge](https://sourceforge.net/projects/gnuwin32/files/pcre/7.0/pcre-7.0.exe/download)

If you want to have *PCRE* support on platforms that don\'t support it
natively, e.g. vxWorks, it is probably the easiest to build *PCRE* as an
EPICS module.

#### Building the *PCRE* package as an EPICS module

1.  Download the *PCRE* package from
    [www.pcre.org](https://www.pcre.org).
2.  Extract the *PCRE* package in the [\<top\>]{.kbd} directory of
    *StreamDevice* or create a separate [\<top\>]{.kbd} location using
    `makeBaseApp.pl`.
3.  Download this
    [Makefile](http://epics.web.psi.ch/software/streamdevice/pcre/Makefile)
    and this
    [fixforvxworks.pl](http://epics.web.psi.ch/software/streamdevice/pcre/fixforvxworks.pl)
    script and save them to the extracted pcre directory.
4.  Change into the pcre direcrory and run `perl fixforvxworks.pl`
5.  Run `make` (or `gmake`)

Define the location of the pcre [\<top\>]{.kbd} in the RELEASE file for
*StreamDevice*.

    PCRE=/home/epics/pcre

Regular expressions are optional. If you don\'t want them, you don\'t
need this.

[]{#lib}

## 2. Building *StreamDevice*

Go to the *StreamDevice* directory and run `make` (or `gmake`). This
will create and install the *stream* library and the [stream.dbd]{.kbd}
file and an example IOC application.

To use *StreamDevice*, your own application must be built with the
*stream* and *asyn* (and optionally *pcre*) libraries and must load
[asyn.dbd]{.kbd} and [stream.dbd]{.kbd}.

Include the following lines in your application [Makefile]{.kbd}:

    PROD_LIBS += stream
    PROD_LIBS += asyn
    PROD_LIBS += pcre

Include the following lines in your [xxxAppInclude.dbd]{.kbd} file to
use *stream* and *asyn* with serial lines, IP sockets, and vxi11 (\"GPIB
over ethernet\") support.

    include "base.dbd"
    include "stream.dbd"
    include "asyn.dbd"
    registrar(drvAsynIPPortRegisterCommands)
    registrar(drvAsynSerialPortRegisterCommands)
    registrar(vxi11RegisterCommands)

You can find an example application in the [streamApp]{.kbd}
subdirectory.

[]{#sta}

## 3. The Startup Script

*StreamDevice* is based on [*protocol files*](protocol.html). To tell
*StreamDevice* where to search for protocol files, set the environment
variable `STREAM_PROTOCOL_PATH` to a list of directories to search. On
Unix and vxWorks systems, directories are separated by `:`, on Windows
systems by `;`. The default value is `STREAM_PROTOCOL_PATH=.`, i.e. the
current directory.

Also configure the buses (in *asynDriver* terms: ports) you want to use
with *StreamDevice*. You can give the buses any name you want, like
[COM1]{.kbd} or [socket]{.kbd}, but I recommend to use names related to
the connected device.

### Example:

A device with serial communication (9600 baud, 8N1, no flow control) is
connected to [/dev/ttyS1]{.kbd}. The name of the device shall be `PS1`.
Protocol files are either in the current working directory or in the
[../protocols]{.kbd} directory.

Then the startup script may look like this:

    epicsEnvSet ("STREAM_PROTOCOL_PATH", ".:../protocols")

    drvAsynSerialPortConfigure ("PS1","/dev/ttyS1")
    asynSetOption ("PS1", 0, "baud", "9600")
    asynSetOption ("PS1", 0, "bits", "8")
    asynSetOption ("PS1", 0, "parity", "none")
    asynSetOption ("PS1", 0, "stop", "1")
    asynSetOption ("PS1", 0, "clocal", "Y")
    asynSetOption ("PS1", 0, "crtscts", "N")

All above options are the defaults. Thus their usage in optional in this
case.

If the device uses hardware flow control, change the last two lines to:

    asynSetOption ("PS1", 0, "clocal", "N")
    asynSetOption ("PS1", 0, "crtscts", "Y")

Newer versions of *asyn* also support software flow control
(CTRL-S,CTRL-Q). If the device uses this, you may want to set:

    asynSetOption ("PS1", 0, "ixon", "Y")
    asynSetOption ("PS1", 0, "ixany", "Y")

If the device was instead connected via telnet-style TCP/IP at address
192.168.164.10 on port 23, the startup script would contain:

    epicsEnvSet ("STREAM_PROTOCOL_PATH", ".:../protocols")

    drvAsynIPPortConfigure ("PS1", "192.168.164.10:23")

With a VXI11 (GPIB via TCP/IP) connection, e.g. a HP E2050A on IP
address 192.168.164.10, it would look like this:

    epicsEnvSet ("STREAM_PROTOCOL_PATH", ".:../protocols")

    vxi11Configure ("PS1","192.168.164.10",1,1000,"hpib")

[]{#pro}

## 4. The Protocol File

For each different type of hardware, create a protocol file which
defines protocols for all needed functions of the device. The file name
is arbitrary, but I recommend that it contains the device type. It must
not contain spaces and should be short. During `iocInit`, *streamDevice*
loads and parses the required protocol files. If the files contain
errors, they are printed on the IOC shell. Put the protocol file in one
of the directories listed in `STREAM_PROTOCOL_PATH`.

### Example:

`PS1` is an *ExamplePS* power supply. It communicates via ASCII strings
which are terminated by \<carriage return\> \<line feed\> (ASCII codes
13, 10). The output current can be set by sending a string like
`"CURRENT 5.13"`. When asked with the string `"CURRENT?"`, the device
returns the last set value in a string like `"CURRENT 5.13 A"`.

Normally, an analog output record should write its value to the device.
But during startup, the record should be initialized from the the
device. The protocol file [ExamplePS.proto]{.kbd} defines the protocols
`getCurrent` and `setCurrent`.

    Terminator = CR LF;

    getCurent {
            out "CURRENT?";
            in "CURRENT %f A";
        }

    setCurrent {
        out "CURRENT %.2f";
        @init {
            getCurent;
        }
    }

[]{#reload}

### Reloading the Protocol File

During development, the protocol files might change frequently. To
prevent restarting the IOC all the time, it is possible to reload the
protocol file of one or all records with the shell function
`streamReload("``record`{.variable}`")`. If `"``record`{.variable}`"` is
not given [or empty]{.new}, all records using *StreamDevice* reload
their protocols. [In EPICS 3.14 or higher, `record`{.variable} can be a
glob pattern.]{.new}

Furthermore, the `streamReloadSub` function can be used with a
subroutine record to reload all protocols.

Reloading the protocol file aborts currently running protocols. This
might set `SEVR=INVALID` and `STAT=UDF`. If a record can\'t reload its
protocol file (e.g. because of a syntax error), it stays `INVALID`/`UDF`
until a valid protocol is loaded.

[Reloading triggers an `@init` [handler](protocol.html#except).]{.new}
See the [next chapter](protocol.html) for protocol files in depth.

[]{#debug}

## 5. Debug and Error Messages

Generation of debug and error messages is controlled with two shell
variables, `streamDebug` and `streamError`. Setting those variables to 1
(actually to any number but 0) enables the messages. Per default debug
messages are switched off and error messages are switched on. Errors
occuring while loading protocol files are always shown.

Warning: Enabling debug messages can create a lot of output! At the
moment, there is no way to set filters on debug or error messages.

Debug output can be redirected to a file with the command
`streamSetLogfile("``filename`{.variable}`")`. When called without a
filename, debug output is directed back to the console.

By default the debug/error output is set to be colored if the terminal
allows it but this can be set to always colored or never colored by
setting `streamDebugColored` to 1 or 0 respectively.

Error and debug messages are prefixed with a time stamp unless the
variable `streamMsgTimeStamped` is set to 0.

When a device is disconnected StreamDevice can produce many repeated
timeout messages. To reduce this logging you can set
`streamErrorDeadTime` to an integer number of seconds. When this is set
repeated timeout messages will not be printed in the specified dead time
after the last message. The default dead time is 0, resulting in every
message being printed.

### Example (vxWorks):

    streamError=1
    streamDebug=1
    streamDebugColored=1
    streamErrorDeadTime=30
    streamMsgTimeStamped=1
    streamSetLogfile("logfile.txt")

### Example (iocsh):

    var streamError 1
    var streamDebug 1
    var streamDebugColored 1
    var streamErrorDeadTime 30
    var streamMsgTimeStamped 1
    streamSetLogfile("logfile.txt")

[]{#rec}

## 6. Configuring the Records

To tell a record to use *StreamDevice*, set its `DTYP` field to
`"stream"`.

The `INP` or `OUT` link has the form
`"@``filename protocol`{.variable}`[(``arg1`{.variable}`,``arg2`{.variable}`,...)] bus [``address`{.variable}` [``parameters`{.variable}`]]"`.

(Elements in `[]` are optional. Do not type the `[]`).

Here, `filename`{.variable} is the name of the protocol file and
`protocol`{.variable} is the name of a protocol defined in this file.
(See the [next chapter](protocol.html).)

If the protocol requires [arguments](protocol.html#argvar), specify them
enclosed in parentheses:
`protocol`{.variable}`(``arg1,arg2,...`{.variable}`)`. [Spaces in the
argument list are now allowed. The first space before and after an
argument is ignored. Further spaces are considered part of the
argument.]{.new}

The communication channel is specified with `bus`{.variable} (aka
*asynDriver* \"port\") and `addr`{.variable}. If the bus does not have
addresses, `addr`{.variable} may be skipped. Optional
`parameters`{.variable} are passed to the bus driver. (At the moment, no
bus driver supports parameters.)

### Example:

Create an input record to read and an output record to set the current
of `PS1`. Use protocols *getCurrent* and *setCurrent* from file
*ExamplePS.proto*. The bus is called *PS1* like the device.

    record (ai, "PS1:I-get")
    {
        field (DESC, "Read current of PS1")
        field (DTYP, "stream")
        field (INP,  "@ExamplePS.proto getCurrent PS1")
        field (EGU,  "A")
        field (PREC, "2")
        field (LOPR, "0")
        field (HOPR, "60")
        field (PINI, "YES")
        field (SCAN, "10 second")
    }
    record (ao, "PS1:I-set")
    {
        field (DESC, "Set current of PS1")
        field (DTYP, "stream")
        field (OUT,  "@ExamplePS.proto setCurrent PS1")
        field (EGU,  "A")
        field (PREC, "2")
        field (DRVL, "0")
        field (DRVH, "60")
        field (LOPR, "0")
        field (HOPR, "60")
    }

[Next: Protocol Files](protocol.html) Dirk Zimoch, 2018
