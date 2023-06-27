# scalcout Records

**Note:** The scalcout record is part of the *calc* module of the
[*synApps*](https://www.aps.anl.gov/BCDA/synApps){target="ex"} package.
Device support for scalcout records is only available for *calc* module
release 2-4 or higher. You also need the synApps modules *genSub* and
*sscan* to build *calc*.

Up to release 2-6 (synApps release 5.1), the scalcout record needs a
fix. In sCalcout.c at the end of `init_record` add before the final
`return(0)`:

``` box
        if(pscalcoutDSET->init_record ) {
            return (*pscalcoutDSET->init_record)(pcalc);
        }
```

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
:   [Output:]{.underline} *`x`*`=OSV`\
    [Input:]{.underline} `SVAL=`*`x`*\

For scalcout records, it is probably more useful to access fields `A` to
`L` and `AA` to `LL` directly (e.g. `"%(A)f"` or `"%(BB)s"`). However,
even if `OVAL` is not used, it is calculated by the record. Thus, `CALC`
must always contain a valid expression (e.g. `"0"`).

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
