Channel Access Security Requirements
====================================

Ned D. Arnold

--------------

Table of Contents
-----------------

`1.0 Abstract <casecsp.html#HDR1.0%20%20%20%202%207>`__
 
`2.0 Introduction <casecsp.html#HDR2.0%20%20%20%202%209>`__

`3.0 IOC Access Control Requirements Overview <casecsp.html#HDR3.0%20%20%20%202%2010>`__

`4.0 Functional Requirements <casecsp.html#HDR4.0%20%20%20%202%2012>`__

--------------

1.0 Abstract
------------

The Advanced Photon Source Control System is based on EPICS, the
Experimental Physics and Industrial Control System co-developed by Los
Alamos National Lab and Argonne National Lab. The basic architecture of
EPICS allows for intelligent VME-based computers (referred to as
Input/Output Controllers or IOCs) to be placed throughout the facility
close to the APS equipment to be monitored and controlled. These IOCs
are all interconnected to each other and to Unix-based workstations to
allow physicists, engineers and technicians to monitor the operation of
APS and to make changes to operating parameters from workstations in the
control rooms or even their offices. The interconnection of IOCs and
workstations is accomplished by widely accepted standards, namely
ethernet and TCP/IP.

Extreme flexibility is provided by this "standards-based"
interconnection mechanism, allowing users from all over the world to
have access to APS data. However, significant security issues arise when
it is realized that access to APS data also implies (currently) access
to APS parameters that can effect the operation of the machine. This
document discusses those security issues and then presents specific
requirements for securing the APS Control System from unauthorized
access.

A thorough Access Control System must accommodate the following
observations:

-  Certain individuals may be authorized to control some parameters but
   not others (e.g. a LINAC technician should not be permitted to adjust
   quadrupole currents in the Storage Ring)
-  Many individuals may have permission to monitor (or read) machine
   parameters while only a few individuals will be authorized to modify
   (or write) them.
-  Certain parameters must be altered only from specific locations (e.g.
   if someone is doing maintenance on the LINAC from an Operator
   Interface workstation in the klystron gallery, it would be quite
   inconvenient for someone in the Control Room to adjust the same
   equipment)
-  The status of the Advanced Photon Source should be utilized in
   determining access authorization to a machine parameter. Certain
   modes of APS will require extreme control over what parameters may be
   adjusted (e.g. stored beam mode, storage ring orbit studies).

Therefore, the requirements for access control described in this
document allow access to APS data and machine parameters based on four
criteria: originator of the request (who); type of access, e.g. read or
write (what); source (location) from which the request originated
(where); machine status at the time of the request (when). Access rules
predefined by qualified APS Operations Personnel will limit any access
to the APS Control System to those specifically authorized. Machine
parameters can be grouped together and different rules defined for each
parameter group (allowing LINAC parameters to have different rules than
Storage Ring parameters). Four access levels are used to grant
increasingly more access to those that are appropriately authorized.

2.0 Introduction
----------------

The Experimental Physics and Industrial Control System (EPICS) allows
for distributed control of very large facilities via software based on
standard network protocols and interfaces. Input/Output Controllers
(IOCs) attached to the network respond to commands and provide monitor
data to "clients" that are also on the network. This distributed
architecture has numerous advantages compared to a centralized topology,
including modularity, expandability, low vulnerability to a single
failure, etc. Security, however, must be specifically addressed to
ensure that "unauthorized clients" do not unexpectedly alter critical
setpoints or parameters during machine operation. This challenge is a
bit more formidable in an open distributed system than in a closed
centralized system.

Fortunately, there are only three conceivable paths by which one can
alter the pre-programmed functionality within an IOC: by gaining access
to the IOC operating system (vxWorks) shell using telnet via ethernet;
by gaining access to the IOC operating system shell via the RS232 port
on the CPU board; or by communicating with the EPICS software via it\qs
unique application layer network communication protocol called Channel
Access.

This document specifies the requirements for ensuring that only
"authorized individuals" can effect changes in the control system via
the Channel Access path. The other vulnerabilities (access to the IOC
operating system) are briefly discussed in this document to provide a
unified presentation of the IOC security issue, but detailed
requirements are presented in referenced documents.

3.0 IOC Access Control Requirements Overview
--------------------------------------------

This section will introduce the requirements for the IOC Access Control
implementation. The following discussion is not intended to present
detailed functional requirements, but to present the general
expectations of IOC Access Control.

3.1 Restrict Access to the IOC Operating System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Access to the IOC operating system must be restricted to authorized
individuals who are trained in vxWorks and have a legitimate need to be
working on the system at that level. Authorized individuals would
include the application engineers (and trained technicians) responsible
for that system or system software engineers that may be trouble
shooting a software problem.

In addition, some mechanism must be provided to give authorized
individuals access to the appropriate IOC independent of location. It is
unacceptable to require the individual to be next to the IOC that
requires attention.

If access to the IOC operating systems is securely limited to trained,
cognizant, and authorized individuals, there is no need to make this
access dependent on machine operating status. This authority level is
comparable to a "super-user", and such classification requires
responsible use of the authority allowed.

Preventing access to the IOC operating system is a system design
challenge. Detailed requirements of the security requirements are <will
be> discussed in the Functional Requirement "Access to The IOC Operating
System".

3.2 Prevent IOC Access from Outside the APS Control System Subnet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since the Channel Access protocol is built upon the popular TCP/IP suite
of protocols, the possibility exists for Channel Access clients to
reside anywhere in the world. This, of course, must be precluded.

Design of the control system communication network must restrict outside
clients from direct access to the IOC\qs. Several approaches are
available and will be further discussed in other design documents.

The design should not absolutely preclude access to control system data
from outside the control system "subnet". It should limit the who, what
and how this data is obtained from the control system. For example, an
authorized individual could telnet to the host computer on the control
system subnet, start an authorized Channel Access client to collect
data, and have that data returned to him.

This security issue is a combination of system design (network layout)
and software utilities. Further details of the specific requirements are
<will be> provided in the Functional Requirement "Channel Access Gateway
to the Outside World".

3.3 Restrict Channel Access Requests to "Authorized" Clients
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Channel access must restrict access to the IOC database parameters from
all channel access clients except those specifically authorized to
monitor or control that parameter. Authorized monitoring of database
parameters should be quite lenient, but should be restricted when IOC
performance is threatened. Authorized control or modification of a
particular parameter is dependent on several factors.

A thorough IOC access control system would determine authorization to a
particular database parameter based on four criteria: originator of the
request (who); type of access, e.g. read or write (what); source
(location) from which the request originated (where); machine status at
the time of the request (when). The IOC Access Control implementation
must balance the desired flexibility obtainable from these four
parameters versus complexity of implementation and operation of the
system.

-  WHO: The first consideration for permitting control of database
   parameters is who is making the request. Clearly not all APS
   employees are qualified to adjust APS equipment via the control
   system. In addition, certain employees may be authorized to control
   some parameters but not others (e.g. a LINAC technician should not be
   permitted to adjust quadrupole currents in the Storage Ring). A
   mechanism must be provided to group authorized employees into
   authorization levels which Channel Access can use to allow or
   disallow a modification request. This also implies that the Channel
   Access client is able to determine who is initiating the requests.
-  WHAT: Another consideration in allowing access to IOC database
   parameters is the type of access requested, e.g. read or write. In a
   typical control system environment, many individuals are likely to
   have permission to monitor (or read) database parameters while only a
   few individuals will be authorized to modify (or write) them. This
   flexibility must be provided in the Channel Access Security
   implementation.
-  WHERE: Another consideration for permitting control of database
   parameters is where the request is from. An earlier requirement was
   to restrict "authorized clients" to those that are directly connected
   to the Control System Subnet, but additional flexibility in this
   respect is extremely advantageous. For example, if someone is doing
   maintenance on the LINAC from an Operator Interface workstation in
   the klystron gallery, it would be quite inconvenient for someone in
   the Control Room to adjust the same equipment. The location from
   where the request originates can generally be based on the IP number
   of the computer on which the Channel Access client is running, but
   the issue of "portable consoles" must be addressed as well.
-  WHEN: Consideration of the status of the Advanced Photon Source must
   also be included in determining authorization into the IOC database.
   Certain modes of APS will require extreme control over what
   parameters may be adjusted (e.g. stored beam mode, storage ring orbit
   studies).

The consideration of the above criteria to determine access to the IOC
database must be dynamically alterable by some appropriate
administrative procedure. Ultimately, APS Operations will have overall
control of the who, what, where, and when of IOC Access.

3.4 Discourage a Sophisticated Saboteur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The above requirements, if properly implemented, will discourage any
inadvertent and/or direct attempt to interfere with normal APS
operations. However, it is likely that the implementation will rely on
existing security features in commercial hardware and software. It is
beyond the scope of this effort to absolutely guarantee that no one can
penetrate the access control scheme implemented to fulfill the above
goals. There are no personnel safety issues involved, so the monumental
task of implementing a system that can be guaranteed against even
sophisticated saboteurs is not required for this application.

4.0 Functional Requirements
---------------------------

This section presents detailed requirements for Channel Access Security.
Any discussions that imply a specific implementation are only
suggestions used to clarify the requirement and are not binding on the
implementer as long as the requirement is met. Refer to Figure 2 for an
illustration of the requirements being discussed.

4.1 Enforcement of Channel Access Security
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All requests between a "channel access client" and a "channel access
server" must be dependent on pre-defined security restrictions described
in the following paragraphs. This includes workstation-to-IOC
communication as well as IOC-to-IOC communication (that uses Channel
Access). Process Variable "links" within an IOC that do not use Channel
Access are not subject to these pre-defined access rules (e.g. dbget,
dbput, etc).

4.2 Database Field Access Level
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each field of a record type will have an "access level" defined to it at
the time that the record type is defined (in xxxxRecord.ascii). "Access
level" is an entry from 1 to 4 representing different restraints that
must be satisfied prior to allowing access to that field (i.e. each
level can be assigned different \\qaccess rules\q for granting
permission to read or write from/to that particular field). Typically,
higher access levels are more restrictive than lower access levels, but
this is more of a convention than restraint, as will be seen later.

4.3 Process Variable Groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Process variables (unique instances of any record type) will be grouped
into PV Groups where each process variable in that group requires
identical rules for each of the four access levels. There is no
constraint on the number of PV Groups nor the number of process
variables within a group. Any process variable can only be a member of
one group.

4.4 PV Group Access Rules
~~~~~~~~~~~~~~~~~~~~~~~~~

Each PV Group will have a set of rules for each access level. The rules
will define the prerequisite conditions (who, what, when, from where)
that must be fulfilled prior to access being granted. The rules will be
entered in the form of logical expressions that must evaluate to be true
in order for the requested access to be granted. The right hand of the
expression may contain logical operands, User Access Group names (UAGs),
Location Access Group names (LAG\qs), or Process Variables (PV\qs).
Examples are provided below:

::

   Level 1 :  READ = *  /* all allowed to read fields with this access level */
   WRITE = *  /* all allowed to write fields with this access level */
   Level 2 :  READ = *
   WRITE = UAG[linac]   /* linac group allowed at any time */
   Level 3 :  READ = (PV[LI:IOCLTSC:caConnectionsSR] < 100)
   WRITE = NONE  /* example for a video image */
   Level 4 :  READ = *
   WRITE = (UAG[linac] && (PV[LI:OP:stateCC] !=RUNNING) &&
                 LAG[ICR])
   A complete list of possible operands and operations follows:
   OPERANDS :
   UAG[example_1] : A predefined User Access Group named example_1. Refer to Section 4.5 .
   LAG[example_2] : A predefined Location Access Group named example_2. Refer to Section 4.6 .
   PV[example_3] : A process variable named example_3. Refer to Section 4.7 .
   * : Wild card or don\qt care condition. Access always allowed.

   OPERATIONS : 
   The following standard C operators must be supported:

   ||, &&, !=, <, >, >=, <=, == , !

4.5 User Access Groups [UAG]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Groups of individual users can be defined and then referred to by a UAG
name. For example, all authorized linac operators could be defined in a
group and then referred to by UAG[linac]. There is no constraint on the
number of User Access Groups nor the number of users within a group. An
individual can be included in multiple UAGs. To indicate a particular
user (instead of a group), that user\qs name can be used instead of the
UAG name (e.g. UAG[mrk] refers to an individual who\qs user name is
mrk). For interactive channel access clients, provisions must be made to
alter the current user (e.g. su nda) without requiring the client
program to restart.

4.6 Location Access Groups [LAG]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Location Access Groups define particular workstations (using the name of
the workstation) which are allowed access, based on the access rules.
Groups of workstations can be defined and then referred to by a LAG name
(e.g. UAG[InjectionControlRoom] or UAG[ICR]) . There is no constraint on
the number of Location Access Groups nor the number of workstations
within a group. If a particular workstation is not included in any LAG,
that workstation can only access database fields that have no LAG entry
in its PV Group Access Rule.

4.7 Process Variable [PV]
~~~~~~~~~~~~~~~~~~~~~~~~~

Process variables can be included in the PV Group Access Rules to
implement access that is dependent on \\qreal-time\q status of the
machine. Should a change in a process variable occur such that access to
a particular database field is inhibited, this change must must take
effect within five seconds of the process variable changing to the new
value. It is unacceptable to evaluate rules using process variables only
at connection time.

4.8 Configuration Changes
~~~~~~~~~~~~~~~~~~~~~~~~~

Configuration changes in the Channel Access Security System will only be
done by authorized "Operations" personnel. A mechanism for altering the
rules, defining new Location Access Groups or User Access Groups, and
forcing these changes to become immediately effective must be provided.
