# ai Records

## Normal Operation

Depending on the format type, different record fields are used for
output and input. The variable *`x`* stands for the written or read
value.

DOUBLE format (e.g. `%f`):
:   [Output:]{.underline} *`x`*`=(VAL-AOFF)/ASLO`\
    [Input:]{.underline} `VAL=(`*`x`*`*ASLO+AOFF)*(1.0-SMOO)+VAL*SMOO`\
    In both cases, if `ASLO==0.0`, it is treated as `1.0`. Default
    values are `ASLO=1.0`, `AOFF=0.0`, `SMOO=0.0`.\
    If input is successful, `UDF` is cleared.

LONG format (e.g. `%i`):

:   [Output:]{.underline} *`x`*`=RVAL`\
    [Input:]{.underline} `RVAL=`*`x`*\
    Note that the record calculates
    `VAL=(((RVAL+ROFF)*ASLO+AOFF)*ESLO+EOFF)*(1.0-SMOO)+VAL*SMOO` if
    `LINR=="LINEAR"`. `ESLO` and `EOFF` might be set in the record
    definition. *StreamDevice* does not set it. For example, `EOFF=-10`
    and `ESLO=0.000305180437934` (=20.0/0xFFFF) maps 0x0000 to -10.0,
    0x7FFF to 0.0 and 0xFFFF to 10.0. Using unsigned formats with values
    ≥ 0x800000 gives different results on 64 bit machines.

    If `LINR=="NO CONVERSION"` (the default), `VAL` is directly
    converted from and to `long` without going through `RVAL`. This
    allows for more bits on 64 bit machines. To get the old behavior,
    use `LINR=="LINEAR"`.

ENUM format (e.g. `%{`):
:   Not allowed.

STRING format (e.g. `%s`):
:   Not allowed.

## Initialization

During [initialization](processing.html#init), the `@init` handler is
executed, if present. In contrast to normal operation, in DOUBLE input
`SMOO` is ignored (treated as `0.0`).

[aai](aai.html) [aao](aao.html) [ai](ai.html) [ao](ao.html)
[bi](bi.html) [bo](bo.html) [calcout](calcout.html)
[int64in](int64in.html) [int64out](int64out.html) [longin](longin.html)
[longout](longout.html) [lsi](lsi.html) [lso](lso.html)
[mbbiDirect](mbbiDirect.html) [mbboDirect](mbboDirect.html)
[mbbi](mbbi.html) [mbbo](mbbo.html) [scalcout](scalcout.html)
[stringin](stringin.html) [stringout](stringout.html)
[waveform](waveform.html)

Dirk Zimoch, 2018
