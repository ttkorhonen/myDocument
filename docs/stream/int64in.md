# int64in Records

**Note:** The int64in (integer 64 bit input) record is only available
from EPICS base R3.16 on.

## Normal Operation

The variable *`x`* stands for the written or read value.

DOUBLE format (e.g. `%f`):
:   Not allowed.

LONG format (e.g. `%i`):
:   [Output:]{.underline} *`x`*`=VAL`\
    [Input:]{.underline} `VAL=`*`x`*

ENUM format (e.g. `%{`):
:   [Output:]{.underline} *`x`*`=VAL`\
    [Input:]{.underline} `VAL=`*`x`*

STRING format (e.g. `%s`):
:   Not allowed.

## Initialization

During [initialization](processing.html#init), the `@init` handler is
executed, if present. All format converters work like in normal
operation.

[aai](aai.html) [aao](aao.html) [ai](ai.html) [ao](ao.html)
[bi](bi.html) [bo](bo.html) [calcout](calcout.html)
[int64in](int64in.html) [int64out](int64out.html) [longin](longin.html)
[longout](longout.html) [lsi](lsi.html) [lso](lso.html)
[mbbiDirect](mbbiDirect.html) [mbboDirect](mbboDirect.html)
[mbbi](mbbi.html) [mbbo](mbbo.html) [scalcout](scalcout.html)
[stringin](stringin.html) [stringout](stringout.html)
[waveform](waveform.html)

Dirk Zimoch, 2018
