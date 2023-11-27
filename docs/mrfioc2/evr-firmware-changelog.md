### Firmware Version Change Log

```
FW Version Date Changes Affected HW
0200 11.06.2015 - Prototype release VME-EVR-300
0201 24.09.2015 - Added segmented data buffer block status flags
```
- Changed delay compensation FIFO depth from 2k to 4k
event cycles
- Added DCM modulation to improve jitter performance

##### VME-EVR-300

```
0203 12.01.2016 - Delay compensation amendments, non-GTX outputs
are compensated properly
```
##### VME-EVR-300

```
0204 25.01.2016 - First release for PCIe-EVR-300DC
```
- Fixed segmented data buffer flag writes

```
all
```
```
0204 03.02.2016 - Fixed initial values of GTX outputs
```
- GTX output aligment

##### VME-EVR-300

```
0205 07.04.2016 - Changed PCIe-EVR-300DC class code to 0x118000.
```
- Moved delay compensation data from first segment to
last segment.
- Fixed dual output mapping for transition board outputs.
- Added backplane signals to mTCA-EVR.
- Added delay compensation disabled mode to be able to
use DC capable EVRs with pre-DC EVG and fan-outs.

```
all
```
```
0206 12.08.2016 - Relocated segmented data buffer to new address loca-
tion.
```
- Replaced earlier data buffer in its original position
(maintaining compatibility with 230 series protocol).
- Changed segmented data buffer protocol to use K28.2
as a start symbol

```
all
```
```
0207 30.08.2016 - Added stand-alone capability: using its internal refer-
ence the EVR can now operate as a stand-alone pulse
generator without event link.
```
- EVR can operate as a simple EVG by forwarding inter-
nal events
- Added software event capability
- Added one EVG type sequencer

```
all
```

3. Event Receiver 100

```
FW Version Date Changes Affected HW
030207 23.12.2016 - Changed beacon event code from 0x7a to 0x7e.
```
- Added status bits for delay compensation path delay
value validity.
- Added register for topology ID.

```
all
```
```
040207 09.1.2017 - Repaired “trigger allways” problem with triggering se-
quencer with pulse generator 19.
```
- Added mapping 61 for sequencer software triggering.

```
all
```
```
050207 19.1.2017 - Fixed running on internal reference for VME-EVR-300.VME-EVR-300
060207 9.2.2017 - Added configurability to handling a lost event clock:
continue, stop, fallback to reference clock.
```
- Further fix to running on internal reference for VME-
EVR-300.

##### VME-EVR-300

```
070207 6.4.2017 - Fixed CML/GTX operation in stand-alone mode with-
out receiver event stream.
```
- Fixed mapping of TCLKA/TCLKB backplane clocks
on mTCA-EVR-300.

```
mTCA-EVR-300
```
```
080207 7.8.2017 - PCIe AXI to OPB bridge fix for overloapping read/write
operation during block transfers.
```
- Added pullup to MODU_SDA and MODU_DEF0.

```
PCIe-EVR-300DC
```
```
090207 27.2.2018 - Changes to get design built on Vivado 2017.4 All
```
```
0A0207 18.9.2018 - Changed number of external inputs to 16. PCIe-EVR-300DC
```
```
0D0207 20.5.2019 - Added programmable phase shift to prescalers. mTCA-EVR-300
```
```
0E0207 2.7.2019 - Fix to event FIFO.
```
- Added flip-flop outputs.

```
mTCA-EVR-300
```
