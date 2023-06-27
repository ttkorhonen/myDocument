# User\'s Guide

<div>

[Intro](index.html){target="_parent"}

</div>

<div>

[Setup](setup.html){target="_parent"}
[](javascript:show('setup')){#setupButton}

<div>

[Prerequisites](setup.html#pre){target="_parent"}

<div>

[Using EPICS 3.13](epics3_13.html){target="_parent"}

</div>

[Build Library](setup.html#lib){target="_parent"} [Build
Application](setup.html#app){target="_parent"} [Startup
Script](setup.html#sta){target="_parent"} [Protocol
File](setup.html#pro){target="_parent"}

<div>

[Reloading](setup.html#reload){target="_parent"}

</div>

[Debugging](setup.html#debug){target="_parent"}
[Records](setup.html#rec){target="_parent"}

</div>

</div>

<div>

[Protocol Files](protocol.html){target="_parent"}
[](javascript:show('protocol')){#protocolButton}

<div>

[General](protocol.html#gen){target="_parent"}
[Protocols](protocol.html#proto){target="_parent"}
[Commands](protocol.html#cmd){target="_parent"}
[Strings](protocol.html#str){target="_parent"}
[Variables](protocol.html#var){target="_parent"}

<div>

[System variables](protocol.html#sysvar){target="_parent"} [Protocol
Arguments](protocol.html#argvar){target="_parent"} [User
variables](protocol.html#usrvar){target="_parent"}

</div>

[Exception Handlers](protocol.html#except){target="_parent"}

</div>

</div>

<div>

[Format Converters](formats.html){target="_parent"}
[](javascript:show('formats')){#formatsButton}

<div>

[Syntax](formats.html#syntax){target="_parent"} [Types &
Fields](formats.html#types){target="_parent"} [%f %e
%g](formats.html#stdd "Standard DOUBLE converters"){target="_parent"}
[%i %d %u %o
%x](formats.html#stdl "Standard LONG converters"){target="_parent"} [%s
%c](formats.html#stds "Standard STRING converters"){target="_parent"}
[%\[*charset*\]](formats.html#cset "Character set STRING converter"){target="_parent"}
[%{*s0*\|*s1*\|\...}](formats.html#enum "Enumeration LONG converter"){target="_parent"}
[%b %B](formats.html#bin "Binary LONG converter"){target="_parent"}
[%r](formats.html#raw "Raw LONG converter"){target="_parent"}
[%R](formats.html#rawdouble "Raw DOUBLE converter"){target="_parent"}
[%D](formats.html#bcd "Binary coded decimal LONG converter"){target="_parent"}
[%\<*checksum*\>](formats.html#chksum "Checksum pseudo converter"){target="_parent"}
[%/*regex*/](formats.html#regex "Perl regular expression STRING converter"){target="_parent"}
[%#/*regex*/*subst*/](formats.html#regsub "Perl regular expression substitution pseudo converter"){target="_parent"}
[%m](formats.html#mantexp "MantissaExponent DOUBLE converter"){target="_parent"}
[%T](formats.html#timestamp "Timestamp DOUBLE converter"){target="_parent"}

</div>

</div>

<div>

[Record Processing](processing.html){target="_parent"}
[](javascript:show('proc')){#procButton}

<div>

[Normal Processing](processing.html#proc){target="_parent"}
[Initialization](processing.html#init){target="_parent"} [I/O
Intr](processing.html#iointr){target="_parent"}

</div>

</div>

<div>

[Record Types](recordtypes.html){target="_parent"}
[](javascript:show('records')){#recordsButton}

<div>

[aai](aai.html){target="_parent"} [aao](aao.html){target="_parent"}
[ai](ai.html){target="_parent"} [ao](ao.html){target="_parent"}
[bi](bi.html){target="_parent"} [bo](bo.html){target="_parent"}
[calcout](calcout.html){target="_parent"}
[int64in](int64in.html){target="_parent"}
[int64out](int64out.html){target="_parent"}
[longin](longin.html){target="_parent"}
[longout](longout.html){target="_parent"}
[lsi](lsi.html){target="_parent"} [lso](lso.html){target="_parent"}
[mbbiDirect](mbbiDirect.html){target="_parent"}
[mbboDirect](mbboDirect.html){target="_parent"}
[mbbi](mbbi.html){target="_parent"} [mbbo](mbbo.html){target="_parent"}
[scalcout](scalcout.html){target="_parent"}
[stringin](stringin.html){target="_parent"}
[stringout](stringout.html){target="_parent"}
[waveform](waveform.html){target="_parent"}

</div>

</div>

<div>

[Tips & Tricks](tipsandtricks.html){target="_parent"}
[](javascript:show('tipsandtricks')){#tipsandtricksButton}

<div>

[Many almost identical
protocols](tipsandtricks.html#argvar){target="_parent"} [Read
unsolicited input](tipsandtricks.html#iointr){target="_parent"} [Read
multi-line messages](tipsandtricks.html#multiline){target="_parent"}
[Write more than one value in one
message](tipsandtricks.html#writemany){target="_parent"} [Read more than
one value from one
message](tipsandtricks.html#readmany){target="_parent"} [Read values of
mixed data type](tipsandtricks.html#mixed){target="_parent"} [Read a web
page](tipsandtricks.html#web){target="_parent"}

</div>

</div>

# Programmer\'s Guide

<div>

[Record API](recordinterface.html){target="_parent"}

</div>

<div>

[Bus API](businterface.html){target="_parent"}
[](javascript:show('bus')){#busButton}

<div>

[Interface Class](businterface.html#class){target="_parent"} [Theory of
Operation](businterface.html#theory){target="_parent"}

<div>

[Registration](businterface.html#registration){target="_parent"}
[Creation & deletion](businterface.html#create){target="_parent"}
[Connecting](businterface.html#connect){target="_parent"} [Bus
locking](businterface.html#lock){target="_parent"} [Writing
output](businterface.html#write){target="_parent"} [Reading
input](businterface.html#read){target="_parent"} [Handling
events](businterface.html#event){target="_parent"}

</div>

</div>

</div>

<div>

[Format Converter API](formatconverter.html){target="_parent"}

<div>

[Converter Class](formatconverter.html#class){target="_parent"} [Theory
of Operation](formatconverter.html#theory){target="_parent"}

<div>

[Registration](formatconverter.html#registration){target="_parent"}
[Parsing](formatconverter.html#parsing){target="_parent"} [Printing and
Scanning](formatconverter.html#printing_scanning){target="_parent"}

</div>

</div>

</div>

<div>

[Operating System API](osinterface.html){target="_parent"}

</div>
