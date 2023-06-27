# Record Types

## Supported Record Types

*StreamDevice* comes with support for all standard record types in EPICS
base which can have device support.

There is a separate page for each supported record type:

[aai](aai.html) [aao](aao.html) [ai](ai.html) [ao](ao.html)
[bi](bi.html) [bo](bo.html) [calcout](calcout.html)
[int64in](int64in.html) [int64out](int64out.html) [longin](longin.html)
[longout](longout.html) [lsi](lsi.html) [lso](lso.html)
[mbbiDirect](mbbiDirect.html) [mbboDirect](mbboDirect.html)
[mbbi](mbbi.html) [mbbo](mbbo.html) [scalcout](scalcout.html)
[stringin](stringin.html) [stringout](stringout.html)
[waveform](waveform.html)

Each page describes which record fields are used in input and output for
different [format data types](formats.html#types) during [normal record
processing](processing.html#proc) and
[initialization](processing.html#init).

It is also possible to [write support for other
recordtypes](recordinterface.html).

Dirk Zimoch, 2018
