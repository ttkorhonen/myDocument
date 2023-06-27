# mbbo Records

## Normal Operation

Depending on the format type, different record fields are used for
output and input. The variable *`x`* stands for the written or read
value.

DOUBLE format (e.g. `%f`):
:   Not allowed.

LONG [or ENUM]{.new} format (e.g. `%i`):

:   

    If any of `ZRVL` \... `FFVL` is set (is not `0`):
    :   [Output:]{.underline} *`x`*`=RVAL&MASK`\
        Note that the record calculates `RVAL` by choosing one of `ZRVL`
        \... `FFVL` depending on `VAL` and by shifting it left by `SHFT`
        bits.\
        [Input:]{.underline} `RBV=RVAL=`*`x`*`&MASK`\
        `MASK` is initialized to `NOBT` 1-bits shifted left by `SHFT`.
        If `MASK==0` (because `NOBT` was not set) it is ignored, i.e.
        *`x`*`=RVAL` and `RBV=RVAL=`*`x`*.

    If none of `ZRVL` \... `FFVL` is set (all are `0`):
    :   [Output:]{.underline} *`x`*`=(VAL<<SHFT)&MASK`\
        [Input:]{.underline} `VAL=(RBV=(`*`x`*`&MASK))>>SHFT`\

STRING format (e.g. `%s`):
:   [Output:]{.underline} Depending on `VAL`, one of `ZRST` \... `FFST`
    is written. `VAL` must be in the range 0 \... 15.\
    [Input:]{.underline} If input is equal one of `ZRST` \... `FFST`,
    `VAL` is set accordingly. Other input strings are not accepted.

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
