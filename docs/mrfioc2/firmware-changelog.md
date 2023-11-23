# Firmware Version Change Log

| FW Version | Date | Changes | Affected HW |
| ---------- | ---- | ------- | ------------|
| 0200 | 11.06.2015 | - Prototype release | VME-EVM-300
| 0201 | 24.09.2015 | - Added segmented data buffer | VME-EVM-300
|      |            |   Fixed Port 1 TX polarity 
| 010202 | 01.10.2015 | - Changed receive FIFO delay target to 00060000 | VME-EVM-300
|        |            |   Added LED test mode (production testing)
|        |            |   Removed test signals from TBOUT
| 010203 | 23.11.2015 | - Added changes for running with a slower clock on fan-out. | VME-EVM-300
| 020203 | 18.12.2015 | - Changes to data buffer forwarding | VME-EVM-300
| | |     Changes for rate conversion forwarding, using internal div/2.
| 0204   | 12.01.2016 | - /2 rate conversion working on events, dbuf and dbits. | VME-EVM-300
| | |     Improvements to delay measurement system.
| 0205   | 13.04.2016 | - Moved delay compensation segment from segment 0 to | VME-EVM-300
| | |     last segment in memory.
| | |     Fixed front panel TTL input order.
| | |     Fixed race condition in segmented memory buffer trans-
| | |     mission that caused dropped software buffers.
| FB0206 | 23.12.2016 | - Added upstream and downstream event receivers. |  VME-EVM-300
| | |     Changed beacon event from 0x7A to 0x7E.
| | |     Added topology ID
| | |     Added delay measurement validity information to delay VME-EVM-300
| | |     compensation data
| 000207 | 19.01.2017 | - Added front panel input phase monitoring and phase | VME-EVM-300
| | | select features.
| | | Added external AC input synhronisation features.
| 010207 | 09.02.2017 | - Fixed occasional dropped out downstream and upstream VME-EVM-300
data buffers/segmented data buffers.
| 030207 | 03.05.2017 | - Added RF input monitoring logic to automatically recover |   VME-EVM-300
| | |      from lost RF signal.
| | |     Added a way to toggle distributed bus transmission
| | |     phase when an external AC synchronisation clock is used.
| 040207 | 23.05.2017 | - Fixed readout of diagnostics information on single | VME-EVM-300
| | | mode transceivers.
| 050207 | 26.06.2017 | - Fixed transceiver_channel to turn off receiver on first | VME-EVM-300
| | | error to prevent propagation of errors up stream. |