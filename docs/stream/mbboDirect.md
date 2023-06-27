# mbboDirect Records

## Normal Operation

Depending on the format type, different record fields are used for
output and input. The variable *`x`* stands for the written or read
value.

DOUBLE format (e.g. `%f`):
:   Not allowed.

LONG or ENUM format (e.g. `%i`):

:   

    If `MASK==0` (because `NOBT` is not set):
    :   [Output:]{.underline} *`x`*`=RVAL`\
        [Input:]{.underline} `RAL=`*`x`*, `VAL=RVAL>>SHFT`\

    If `MASK!=0`:
    :   [Output:]{.underline} *`x`*`=RVAL&MASK`\
        [Input:]{.underline} `RBV=RVAL=`*`x`*`&MASK`, `VAL=RVAL>>SHFT`\

    `MASK` is initialized to `NOBT` 1-bits shifted left by `SHFT`
    (`((2^NOBT)-1)<<SHFT`). The record calculates `RVAL=VAL<<SHFT`.

STRING format (e.g. `%s`):
:   Not allowed.

## Initialization

During [initialization](processing.html#init), the `@init` handler is
executed, if present.

[aai](aai.html) [aao](aao.html) [ai](ai.html) [ao](ao.html)
[bi](bi.html) [bo](bo.html) [calcout](calcout.html)
[int64in](int64in.html) [int64out](int64out.html) [longin](longin.html)
[longout](longout.html) [lsi](lsi.html) [lso](lso.html)
[mbbiDirect](mbbiDirect.html) [mbboDirect](mbboDirect.html)
[mbbi](mbbi.html) [mbbo](mbbo.html) [scalcout](scalcout.html)
[stringin](stringin.html) [stringout](stringout.html)
[waveform](waveform.html)

Dirk Zimoch, 2018
