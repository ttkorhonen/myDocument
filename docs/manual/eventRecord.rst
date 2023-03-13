
Event Record (event)
====================

The normal use for this record type is to post an event and/or process a forward link.
Device support for this record can provide a hardware interrupt handler routine for I/O Event-scanned records.

Parameter Fields
----------------

The record-specific fields are described below,
grouped by functionality.

Scan Parameters

The event record has the standard fields for specifying under what circumstances it will be processed.
These fields are described in dbCommonRecord.html#Scan-Fields

Scan Fields.

.. list-table::
   :widths: 1 3 3 1 2 1 1 1
   :header-rows: 1

   * - Field
     - Summary
     - Type
     - DCT
     - Default
     - Read
     - Write
     - CA PP
   * - SCAN
     - Scan Mechanism
     - MENU menuScan.html menuScan
     - Yes
     -  
     - Yes
     - Yes
     - No
   * - PHAS
     - Scan Phase
     - SHORT
     - Yes
     - 
     - Yes
     - Yes
     - No
   * - EVNT
     - Event Name
     - STRING [40]
     - Yes
     - 
     - Yes
     - Yes
     - No
   * - PRIO
     - Scheduling Priority
     - MENU menuPriority.html menuPriority
     - Yes
     -  
     - Yes
     - Yes
     - No
   * - PINI
     - Process at iocInit
     - MENU menuPini.html menuPini
     - Yes
     -  
     - Yes
     - Yes
     - No


Event Number Parameters

The VAL field contains the event number read by the device support routines. It is this number which is posted. For records that use ``Soft Channel`` device support, it can be configured before run-time or set via dbPuts.

.. list-table::
  :widths: 1 3 3 1 2 1 1 1
  :header-rows: 1

  * - Field
    - Summary
    - Type
    - DCT
    - Default
    - Read
    - Write
    - CA PP
  * - VAL
    - Event Name To Post
    - STRING [40]
    - Yes
    -  
    - Yes
    - Yes
    - No

Input Specification

The device support routines use the address in this record to obtain input. For records that provide an interrupt handler, the INP field should specify the address of the I/O card, and the DTYP field should specify a valid device support module. Be aware that the address format differs according to the card type used. See "https://docs.epics-controls.org/en/latest/guides/EPICS_Process_Database_Concepts.html#address-specification" Address Specification for information on the format of hardware addresses and specifying links.

For soft records, the INP field can be a constant, a database link, or a channel access link. For soft records, the DTYP field should specify ``Soft Channel``.

.. list-table::
  :widths: 1 3 3 1 2 1 1 1
  :header-rows: 1
  
  * - Field
    - Summary
    - Type
    - DCT
    - Default
    - Read
    - Write
    - CA PP
  * - INP
    - Input Specification
    - INLINK
    - Yes
    -  
    - Yes
    - Yes
    - No
  * - DTYP
    - Device Type
    - DEVICE
    - Yes
    - 
    - Yes
    - Yes
    - No


Operator Display Parameters

See  href="dbCommonRecord.html#Operator-Display-Parameters" Fields Common to All Record Types for more on the record name (NAME) and description (DESC) fields.

.. list-table::
  :widths: 1 3 3 1 2 1 1 1
  :header-rows: 1
 
  * - Field
    - Summary
    - Type
    - DCT
    - Default
    - Read
    - Write
    - CA PP
  * - NAME
    - Record Name
    - STRING [61]
    - No
    -  
    - Yes
    - No
    - No
  * - DESC
    - Descriptor
    - STRING [41]
    - Yes
    -  
    - Yes
    - Yes
    - No

Alarm Parameters
++++++++++++++++

The Event record has the alarm parameters common to all record types.  "Alarm-Fields" lists other fields related to alarms that are common to all record types.

Simulation Mode Parameters
++++++++++++++++++++++++++

The following fields are used to operate the event record in the simulation mode. See "Fields-Common-to-Many-Record-Types" for more information on these fields.

.. list-table::
 :widths: 1 3 3 1 2 1 1 1
 :header-rows: 1
 
 * - Field
   - Summary
   - Type
   - DCT
   - Default
   - Read
   - Write
   - CA PP
 * - SIOL
   - Sim Input Specifctn
   - INLINK
   - Yes
   -  
   - Yes
   - Yes
   - No
 * - SVAL
   - Simulation Value
   - STRING [40]
   - No
   -  
   - Yes
   - Yes
   - No
 * - SIML
   - Sim Mode Location
   - INLINK
   - Yes
   -  
   - Yes
   - Yes
   - No
 * - SIMM
   - Simulation Mode
   - MENU menuYesNo.html menuYesNo
   - No
   -  
   - Yes
   - Yes
   - No
 * - SIMS
   - Sim mode Alarm Svrty
   - MENU menuAlarmSevr.html menuAlarmSevr
   - Yes
   -  
   - Yes
   - Yes
   - No

Record Support
--------------

Record Support Routines
+++++++++++++++++++++++

init_record

This routine initializes SIMM with the value of SIML if SIML type is a CONSTANT link or creates a channel access link if SIML type is PV_LINK. SVAL is likewise initialized if SIOL is CONSTANT or PV_LINK.

If device support includes <code>init_record()</code>, it is called.

process

See next section.

Record Processing

Routine process implements the following algorithm:


readValue is called. See  href="#Input-Records" class="podlinkpod"
>&#34;Input Records&#34; for more information.

If PACT has been changed to TRUE, the device support read routine has started but has not completed reading a new input value. In this case, the processing routine merely returns, leaving PACT TRUE.

If VAL &#62; 0, post event number VAL.

Check to see if monitors should be invoked. Alarm monitors are invoked if the alarm status or severity has chanet to 0.

Scan forward link if necessary, set PACT FALSE, and return.


Device Support

Fields of Interest To Device Support

Each record must have an associated set of device support routines. The device support routines are primarily interested in the following fields:

.. list-table::
 :widths: 1 3 3 1 2 1 1 1
 :header-rows: 1
  * - Field
    - Summary
    - Type
    - DCT
    - Default
    - Read
    - Write
    - CA PP
  * - PACT
    - Record active
    - UCHAR
    - No
    -  
    - Yes
    - No
    - No
  * - DPVT
    - Device Private
    - NOACCESS
    - No
    -  
    - No
    - No
    - No
  * - UDF
    - Undefined
    - UCHAR
    - Yes
    - 1
    - Yes
    - Yes
    - Yes
  * - NSEV
    - New Alarm Severity
    - MENU menuAlarmSevr.html menuAlarmSevr
    - No
    -  
    - Yes
    - No
    - No
  * - NSTA
    - New Alarm Status
    - MENU menuAlarmStat.html menuAlarmStat
    - No
    -  
    - Yes
    - No
    - No
  * - INP
    - Input Specification
    - INLINK
    - Yes
    -  
    - Yes
    - Yes
    - No
  * - PRIO
    - Scheduling Priority
    - MENU menuPriority.html menuPriority
    - Yes
    -  
    - Yes
    - Yes
    - No


Device Support Routines

Device support consists of the following routines:

long report(int level)

This optional routine is called by the IOC command <code>dbior</code> and is passed the report level that was requested by the user. It should print a report on the state of the device support to stdout. The <code>level</code> parameter may be used to output increasingly more detailed information at higher levels, or to select different types of information with different levels. Level zero should print no more than a small summary.

long init(int after)

This optional routine is called twice at IOC initialization time. The first call happens before any of the <code>init_record()</code> calls are made, with the integer parameter <code>after</code> set to 0. The second call happens after all of the <code>init_record()</code> calls have been made, with <code>after</code> set to 1.

init_record

  init_record(precord)

This routine is optional. If provided, it is called by the record support <code>init_record()</code> routine.

get_ioint_info

  get_ioint_info(int cmd, struct dbCommon *precord, IOSCANPVT *ppvt)

This routine is called by the ioEventScan system each time the record is added or deleted from an I/O event scan list. <code>cmd</code> has the value (0,1) if the record is being (added to, deleted from) an I/O event list. It must be provided for any device type that can use the ioEvent scanner.

read_event

  read_event(precord)

This routine returns the following values:


0: Success.

Other: Error.


Device Support For Soft Records

The <code>Soft Channel</code> device support module is available. The INP link type must be either CONSTANT, DB_LINK, or CA_LINK.

If the INP link type is CONSTANT, then the constant value is stored into VAL by <code>init_record()</code>, and UDF is set to FALSE. If the INP link type is PV_LINK, then dbCaAddInlink is called by <code>init_record()</code>.

<code>read_event</code> calls recGblGetLinkValue to read the current value of VAL. See  href="#Input-Records" class="podlinkpod"
>&#34;Input Records&#34; for details on soft input.

