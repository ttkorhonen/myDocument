# stringout Records

## Normal Operation

The variable *`x`* stands for the written or read value.

DOUBLE format (e.g. `%f`):
:   Not allowed.

LONG format (e.g. `%i`):
:   Not allowed.

ENUM format (e.g. `%{`):
:   Not allowed.

STRING format (e.g. `%s`):
:   [Output:]{.underline} *`x`*`=VAL`\
    [Input:]{.underline} `VAL=`*`x`*

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
