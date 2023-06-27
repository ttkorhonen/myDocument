# bo Records

## Normal Operation

Depending on the format type, different record fields are used for
output and input. The variable *`x`* stands for the written or read
value.

DOUBLE format (e.g. `%f`):
:   Not allowed.

LONG format (e.g. `%i`):
:   [Output:]{.underline} *`x`*`=RVAL`\
    [Input:]{.underline} `RBV=`*`x`*`&MASK`\
    `MASK` can be set be set in the record definition. Stream Device
    does not set it. If `MASK==0`, it is ignored (i.e. `RBV=`*`x`*).

ENUM format (e.g. `%{`):
:   [Output:]{.underline} *`x`*`=VAL`\
    [Input:]{.underline} `VAL=(`*`x`*`!=0)`\

STRING format (e.g. `%s`):
:   [Output:]{.underline} Depending on `VAL`, `ZNAM` or `ONAM` is
    written, i.e. *`x`*`=VAL?ONAM:ZNAM`.\
    [Input:]{.underline} If input is equal to `ZNAM` or `ONAM`, `VAL` is
    set accordingly. Other input strings are not accepted.

## Initialization

During [initialization](processing.html#init), the `@init` handler is
executed, if present. In contrast to normal operation, LONG input is put
to `RVAL` as well as to `RBV` and converted by the record.

[aai](aai.html) [aao](aao.html) [ai](ai.html) [ao](ao.html)
[bi](bi.html) [bo](bo.html) [calcout](calcout.html)
[int64in](int64in.html) [int64out](int64out.html) [longin](longin.html)
[longout](longout.html) [lsi](lsi.html) [lso](lso.html)
[mbbiDirect](mbbiDirect.html) [mbboDirect](mbboDirect.html)
[mbbi](mbbi.html) [mbbo](mbbo.html) [scalcout](scalcout.html)
[stringin](stringin.html) [stringout](stringout.html)
[waveform](waveform.html)

Dirk Zimoch, 2018
