# calcout Records

**Note:** Device support for calcout records is only available for EPICS
base R3.14.5 or higher.

## Normal Operation

Different record fields are used for output and input. The variable
*`x`* stands for the written or read value.

DOUBLE format (e.g. `%f`):
:   [Output:]{.underline} *`x`*`=OVAL`\
    [Input:]{.underline} `VAL=`*`x`*\
    Note that the record calculates `OVAL` from `CALC` or `OCAL`
    depending on `DOPT`.

LONG format (e.g. `%i`):
:   [Output:]{.underline} *`x`*`=int(OVAL)`\
    [Input:]{.underline} `VAL=`*`x`*\

ENUM format (e.g. `%{`):
:   [Output:]{.underline} *`x`*`=int(OVAL)`\
    [Input:]{.underline} `VAL=`*`x`*\

STRING format (e.g. `%s`):
:   Not allowed.

For calcout records, it is probably more useful to access fields `A` to
`L` directly (e.g. `"%(A)f"`). However, even if `OVAL` is not used, it
is calculated by the record. Thus, `CALC` must always contain a valid
expression (e.g. `"0"`).

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
