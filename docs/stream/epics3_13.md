# Using EPICS 3.13

[]{#pre}

## 1. Prerequisites

*StreamDevice* version 2.2 and higher can run on EPICS 3.13. However,
this requires some preparation, because EPICS 3.13 is missing some
libraries and header files. Also *asynDriver* needs to be modified to
compile with EPICS 3.13. Due to the limitations of EPICS 3.13, you can
build streamDevice only for vxWorks systems.

Of course, you need an installation of [EPICS
3.13](http://www.aps.anl.gov/epics/base/R3-13.php){target="ex"}. I guess
you already have that, otherwhise you would want to [install
*StreamDevice* on EPICS 3.14](setup). I have tested *StreamDevice* with
EPICS versions 3.13.7 up to 3.13.10 with vxWorks 5.3.1 and 5.5 on a
ppc604 processor.

Download my [compatibility
package](http://epics.web.psi.ch/software/streamdevice/compat-1-0.tgz),
[*asynDriver*](http://www.aps.anl.gov/epics/modules/soft/asyn/){target="ex"}
version 4-3 or higher, and my [configure
patches](http://epics.web.psi.ch/software/streamdevice/configure.tgz).

[]{#compat}

## 2. Build the Compatibility Package

Unpack [compat-1-0.tgz]{.kbd} in the [\<top\>]{.kbd} directory of your
application build area. (Please refer to the [*EPICS IOC Software
Configuration
Management*](http://www.aps.anl.gov/epics/EpicsDocumentation/AppDevManuals/iocScm-3.13.2/managingATop.html#3){target="ex"}
document.)

Change to the [compat]{.kbd} directory and run [make]{.kbd}. This
installs many EPICS 3.14-style header files and a small library
([compatLib]{.kbd}).

[]{#asyn}

## 3. Build the *asynDriver* Library

Unpack the *asynDriver* package and change to its top directory.

Unpack [configure.tgz]{.kbd} here. This will modify files in the
[configure]{.kbd} directory. Change to the [configure]{.kbd} directory
and edit [CONFIG_APP]{.kbd}. Set `COMPAT=...` to the [\<top\>]{.kbd}
directory where you have installed the compatibility package before.
(This patch might also allow you to compile other 3.14-style drivers for
3.13. It has absolutely no effect if you use EPICS 3.14.)

Edit [RELEASE]{.kbd} and comment out `IPAC=...` (unless you have the
*ipac* package and somehow made it compatible to EPICS 3.13). Set
`EPICS_BASE` to your EPICS 3.13 installation.

Run [make]{.kbd} in the [configure]{.kbd} directory.

Change to [../asyn/devGpib]{.kbd} and edit [devGpib.h]{.kbd} and
[devSupportGpib.c]{.kbd}. Change all occurrences of `static gDset` to
`gDset`.

Go one directory up (to [asyn]{.kbd}) and run [make]{.kbd} twice! (The
first run will just create [Makefile.Vx]{.kbd}.) Ignore all compiler
warnings.

Do not try to build the test applications. It will not work.

[]{#lib}

## 4. Build the *StreamDevice* Library

Go to the [\<top\>]{.kbd} directory of your application build area.

Edit [config/RELEASE]{.kbd} and add the variable `ASYN`. Set it to the
location of the *asynDriver* installation. Also set the `COMPAT`
variable to the location of the compatibility package. Run [make]{.kbd}
in the [config]{.kbd} directory.

Unpack the *StreamDevice* package in your [\<top\>]{.kbd} directory.
Change to the newly created *StreamDevice* directory and run
[make]{.kbd}.

[]{#app}

## 5. Build an Application

To use *StreamDevice*, your application must be built with the *asyn*,
*stream*, and *compat* libraries and must load [asyn.dbd]{.kbd} and
[stream.dbd]{.kbd}. Also, as the *stream* library contains C++ code, the
application must be munched. Therefore, include
[\$(TOP)/config/RULES.munch]{.kbd}. (Put your application in the same
[\<top\>]{.kbd} as the *StreamDevice* installation.)

Include the following lines in your [Makefile.Vx]{.kbd}:

    LDLIBS += $(COMPAT_BIN)/compatLib
    LDLIBS += $(ASYN_BIN)/asynLib
    LDLIBS += $(INSTALL_BIN)/streamLib

    include $(TOP)/config/RULES.munch

Include the following lines in your [xxxAppInclude.dbd]{.kbd} file to
use *stream* and *asyn* (you also need a [base.dbd]{.kbd}):

    include "base.dbd"
    include "stream.dbd"
    include "asyn.dbd"

You can find an example application in the [streamApp]{.kbd}
subdirectory.

[]{#sta}

## 6. The Startup Script

*StreamDevice* is based on [*protocol files*](protocol.html). To tell
*StreamDevice* where to search for protocol files, set the environment
variable `STREAM_PROTOCOL_PATH` to a list of directories to search.
Directories are separated by `:`. The default value is
`STREAM_PROTOCOL_PATH=.`, i.e. the current directory.

Also configure the buses (in *asynDriver* terms: ports) you want to use
with *StreamDevice*. You can give the buses any name you want, like
[COM1]{.kbd} or [socket]{.kbd}, but I recommend to use names related to
the connected device.

### Example:

A power supply with serial communication (9600 baud, 8N1) is connected
to [/dev/ttyS1]{.kbd}. The name of the power supply is `PS1`. Protocol
files are either in the current working directory or in the
[../protocols]{.kbd} directory.

Then the startup script must contain lines like this:

    ld < iocCore
    ld < streamApp.munch
    dbLoadDatabase ("streamApp.dbd")

    putenv ("STREAM_PROTOCOL_PATH=.:../protocols")

    drvAsynSerialPortConfigure ("PS1","/dev/ttyS1")
    asynSetOption ("PS1", 0, "baud", "9600")
    asynSetOption ("PS1", 0, "bits", "8")
    asynSetOption ("PS1", 0, "parity", "none")
    asynSetOption ("PS1", 0, "stop", "1")

An alternative approach is to skip step 5 (do not build an application)
and load all components explicitely in the startup script. The
`STREAM_PROTOCOL_PATH` variable can also be a vxWorks shell variable.

    ld < iocCore
    ld < compatLib
    ld < asynLib
    ld < streamLib.munch
    dbLoadDatabase ("asyn.dbd")
    dbLoadDatabase ("stream.dbd")

    STREAM_PROTOCOL_PATH=".:../protocols"

    drvAsynSerialPortConfigure ("PS1","/dev/ttyS1")
    asynSetOption ("PS1", 0, "baud", "9600")
    asynSetOption ("PS1", 0, "bits", "8")
    asynSetOption ("PS1", 0, "parity", "none")
    asynSetOption ("PS1", 0, "stop", "1")

## 7. [Continue as with EPICS 3.14.](setup.html#pro)

[aai](aai.html) [aao](aao.html) [ai](ai.html) [ao](ao.html)
[bi](bi.html) [bo](bo.html) [calcout](calcout.html)
[int64in](int64in.html) [int64out](int64out.html) [longin](longin.html)
[longout](longout.html) [lsi](lsi.html) [lso](lso.html)
[mbbiDirect](mbbiDirect.html) [mbboDirect](mbboDirect.html)
[mbbi](mbbi.html) [mbbo](mbbo.html) [scalcout](scalcout.html)
[stringin](stringin.html) [stringout](stringout.html)
[waveform](waveform.html)

Dirk Zimoch, 2018
