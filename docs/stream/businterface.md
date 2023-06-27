# Bus API

[]{#class}

## Bus Interface Class

*StreamDevice* already comes with an interface to
[*asynDriver*](http://www.aps.anl.gov/epics/modules/soft/asyn/){target="ex"}.
You should first try to implement your bus driver compatible to
*asynOctet*. Then it can be used by *StreamDevice* automatically. Only
if that does not work, write your own bus interface.

A bus interface is a C++ class that inherits from *StreamBusInterface*.
Its purpose is to provide an interface to *StreamDevice* for a low-level
I/O bus driver. *StreamDevice* acts as a client of the interface,
calling interface methods and receiving replies via callbacks. Since the
internal details of *StreamDevice* are not of interest to a bus
interface, I will reference it simply as *client* in this chapter. The
interface class must be registered via a call to
` `[`RegisterStreamBusInterface`](#registration)`()` in the global
context of the C++ file (not in a header file).

Interface methods called by the client must not block for arbitrary long
times. That means the interface is allowed to take mutex semaphores to
protect its internal data structures but it must not take event
semaphores to wait for external I/O or similar.

It is assumed that the interface creates a separate thread to handle
blocking I/O and to call the callback methods in the context of that
thread when I/O has completed or timed out. The callback methods don\'t
block but may in turn call interface methods. Much of the actual work
will be done in the context of those callbacks, i.e. in the interface
thread, thus be generous with stack.

### Example bus interface class declaration

    #include <StreamBusInterface.h>

    class MyInterface : StreamBusInterface
    {
        // ... (internally used attributes and methods)

        MyInterface(Client* client);
        ~MyInterface();

        // StreamBusInterface virtual methods
        bool lockRequest(unsigned long lockTimeout_ms);
        bool unlock();
        bool writeRequest(const void* output, size_t size, unsigned long writeTimeout_ms);
        bool readRequest(unsigned long replyTimeout_ms, unsigned long readTimeout_ms, ssize_t expectedLength, bool async);
        bool supportsAsyncRead();
        bool supportsEvent();
        bool acceptEvent(unsigned long mask, unsigned long timeout_ms);
        bool connectRequest(unsigned long timeout_ms);
        bool disconnectRequest();
        void finish();

    public:
        // creator method
        static StreamBusInterface* getBusInterface(
            Client* client, const char* busname,
            int addr, const char* param);
    };

    RegisterStreamBusInterface(MyInterface);

    // ... (implementation)

### Methods to implement

The interface class must implement a public static creator method:

::: indent
` static StreamBusInterface* `[`getBusInterface`](#create)`(Client* client, const char* busname, int addr, const char* param); `
:::

And it must implement the following pure virtual methods:

::: indent
` bool `[`lockRequest`](#lock)`(unsigned long lockTimeout_ms); `
:::

::: indent
` bool `[`unlock`](#lock)`(); `
:::

It may implement additional virtual methods if the bus supports it:

::: indent
` bool `[`writeRequest`](#write)`(const void* output, size_t size, unsigned long writeTimeout_ms); `
:::

::: indent
` bool `[`readRequest`](#read)`(unsigned long replyTimeout_ms, unsigned long readTimeout_ms, ssize_t expectedLength, bool async); `
:::

::: indent
` bool `[`supportsAsyncRead`](#read)`(); `
:::

::: indent
` bool `[`supportsEvent`](#event)`(); `
:::

::: indent
` bool `[`acceptEvent`](#event)`(unsigned long mask, unsigned long timeout_ms); `
:::

::: indent
` bool `[`connectRequest`](#connect)`(unsigned long timeout_ms); `
:::

::: indent
` bool `[`disconnectRequest`](#connect)`(); `
:::

::: indent
` void `[`finish`](#lock)`(); `
:::

It also may override the following virtual method:

::: indent
` void `[`release`](#create)`(); `
:::

### Callback methods provided

The base class *StreamBusInterface* implements a set of protected
callback methods which must be called in response to the above request
methods (most probably from another thread):

::: indent
` void `[`lockCallback`](#lock)`(StreamIoStatus status = StreamIoSuccess); `
:::

::: indent
` void `[`writeCallback`](#write)`(StreamIoStatus status = StreamIoSuccess); `
:::

::: indent
` ssize_t `[`readCallback`](#read)`(StreamIoStatus status, const void* buffer = NULL, size_t size = 0); `
:::

::: indent
` void `[`eventCallback`](#event)`(StreamIoStatus status = StreamIoSuccess); `
:::

::: indent
` void `[`connectCallback`](#connect)`(StreamIoStatus status = StreamIoSuccess); `
:::

::: indent
` void `[`disconnectCallback`](#connect)`(StreamIoStatus status = StreamIoSuccess); `
:::

### Other provided methods, attibutes, and types

::: indent
` `[`StreamBusInterface`](#create)`(Client* client); `
:::

::: indent
` long `[`priority`](#lock)`(); `
:::

::: indent
` const char* `[`clientName`](#create)`(); `
:::

::: indent
` const char* `[`getOutTerminator`](#write)`(size_t& length); `
:::

::: indent
` const char* `[`getInTerminator`](#read)`(size_t& length); `
:::

::: indent
` enum StreamIoStatus {StreamIoSuccess, StreamIoTimeout, StreamIoNoReply, StreamIoEnd, StreamIoFault}; `
:::

::: indent
` const char* ::toStr(StreamIoStatus); `
:::

[]{#theory}

## Theory of Operation

[]{#registration}

### Registration

::: indent
` RegisterStreamBusInterface(`*`interfaceClass`*`); `
:::

During initialization, the macro `RegisterStreamBusInterface()`
registers the bus interface. It must be called exactly once for each bus
interface class in global file context.

[]{#create}

### Creation and deletion

::: indent
` static StreamBusInterface* getBusInterface(Client* client, const char* busname, int addr, const char* param); `
:::

::: indent
` StreamBusInterface(Client* client); `
:::

::: indent
` void release(); `
:::

::: indent
` const char* clientName(); `
:::

During startup, each client instance searches for its bus interface by
name. It does so by calling the static `getBusInterface()` method of
every registered interface class. This method should check by `busname`
if its interface class is responsible for that bus. If yes, it should
check if the address `addr` is valid and associate a *device* with
`busname`/`addr`. Some busses do not have addresses and allow only one
device (e.g. RS232). Interfaces to such busses can ignore `addr`. The
bus interface may then try to connect to the device, but it should allow
it to be disconnected or switched off at that time. If the bus interface
requires additional parameters, parse the `param` string. Your
constructor should pass `client` to the base class constructor
`StreamBusInterface(Client* client)`.

On success, `getBusInterface` should then return a pointer to a bus
interface instance. Note that many client instances may want to connect
to the same device. Each needs its own bus interface instance. The bus
interface can get a string containing the name of the client instance
from `clientName()`. This name is for use in error and log messages.

On failure, or if this interface class is not responsible for that bus,
`getBusInterface` should return `NULL`. The client will then try other
bus interface classes.

When the client does not need the interface any more, it calls
`release()`. The default implementation of `release()` assumes that
`getBusInterface()` has allocated a new bus interface and just calls
`delete`. You should change `release()` if that assumption is not
correct.

[]{#connect}

### Connecting and disconnecting

::: indent
` bool connectRequest(unsigned long timeout_ms); `
:::

::: indent
` bool disconnectRequest(); `
:::

::: indent
` void connectCallback(IoStatus status = StreamIoSuccess); `
:::

::: indent
` void disconnectCallback(IoStatus status = StreamIoSuccess); `
:::

Whenever possible connection should be handled automatically. The
interface should call `connectCallback()` when the device has connected
and `disconnectCallback()` when the device has disconnected. These
callbacks can be called asynchronously at any time.

If the device is disconnected, an attempt to access the device should
try to reconnect. Normally, the interface should not try to disconnect
unless the device does so automatically.

However, sometimes the client wants to connect or disconnect explicitly.
To connect, the client calls `connectRequest()`. This function should
set up things to reconnect but should not block waiting. Instead it
should immediately return `true` if it expects that connection can be
established soon, or `false` if the request cannot be accepted or
connection handling is not supported. The interface should call
`connectCallback()` once the bus could be connected. If the device can
connect immediately without waiting, it may also call
`connectCallback()` directly from `connectRequest()`.

If the bus cannot be connected within `timeout_ms` milliseconds, the bus
interface should call `connectCallback(StreamIoTimeout)`.

If a device cannot be connected, for example because there is something
wrong with the I/O hardware, `connectCallback(StreamIoFault)` may be
called.

To disconnect explicitly, the client calls `disconnectRequest()`; This
function should return `true` immediately or `false` if the request
cannot be accepted or connection handling is not supported. The
interface should call `connectCallback()` once the bus is disconnected.
There is no timeout for this operation. If disconnecting is impossible,
the interface should call `connectCallback(StreamIoFault)`.

[]{#lock}

### Bus locking

::: indent
` bool lockRequest(unsigned long timeout_ms); `
:::

::: indent
` void lockCallback(IoStatus status = StreamIoSuccess); `
:::

::: indent
` bool unlock(); `
:::

::: indent
` long priority(); `
:::

::: indent
` void finish(); `
:::

Before doing output, the client calls `lockRequest()` to get exclusive
access to the device. This function should return `true` immediately or
`false` if the request cannot be accepted. If the device is already
locked, the bus interface should add itself to a queue, sorted by
`priority()`. As soon as the device is available, the bus interface
should call `lockCallback()`. If the bus cannot be locked within
`lockTimeout_ms` milliseconds, the bus interface should call
`lockCallback(StreamIoTimeout)`.

If a device cannot be locked, for example because there is something
wrong with the I/O hardware, `lockCallback(StreamIoFault)` may be
called.

Normally, it is not necessary to lock the complete bus but only one
device (i.e. one address). Other clients should still be able to talk to
other devices on the same bus.

The client may perform several read and write operations when it has
locked the device. When the protocol ends and the device is locked, the
client calls `unlock()`. If other bus interfaces are in the lock queue,
the next one should call `lockCallback()` now.

The client calls `finish()` when the protocol ends. This allows the bus
interface to clean up. The bus interface should also cancel any
outstanding requests of this client.

[]{#write}

### Writing output

::: indent
` bool writeRequest(const void* output, size_t size, unsigned long writeTimeout_ms); `
:::

::: indent
` void writeCallback(IoStatus status = StreamIoSuccess); `
:::

::: indent
` const char* getOutTerminator(size_t& length); `
:::

To start output, the client calls `writeRequest()`. You can safely
assume that the device has already been locked at this time. That means,
no other client will call `writeRequest()` for this device and no other
output is currently active for this device until it has been unlocked.

The function should arrange transmission of `size` bytes of `output` but
return `true` immediately or `false` if the request cannot be accepted.
It must not block until output has completed. After all output has been
successfully transmitted, but not earlier, the interface should call
`writeCallback()`.

If output blocks for `writeTimeout_ms` milliseconds, the interface
should abort the transmision and call `writeCallback(StreamIoTimeout)`.

If output is impossible, for example because there is something wrong
with the I/O hardware, `writeCallback(StreamIoFault)` may be called.

The interface must send excactly the `size` bytes from `output`, not
less. It should not change anything unless the bus needs some special
formatting (e.g. added header, escaped bytes) and it should not assume
that any bytes have a special meaning. In particular, a null byte does
not terminate `output`.

A call to `getOutTerminator()` tells the interface which terminator has
already been added to the output. If `NULL` was returned, the client is
not aware of a terminator (no outTerminator was defined in the
protocol). In this case, the interface may add a terminator which it
knows from other sources. An interface is not required to support `NULL`
results and may not add any terminator in this case.

The buffer referenced by `output` stays valid until `writeCallback()` is
called.

The client may request more I/O or call `unlock()` after
`writeCallback()` has been called.

[]{#read}

### Reading input

::: indent
` bool readRequest(unsigned long replyTimeout_ms, unsigned long readTimeout_ms, ssize_t expectedLength, bool async); `
:::

::: indent
` ssize_t readCallback(IoStatus status, const void* buffer = NULL, size_t size = 0); `
:::

::: indent
` const char* getInTerminator(size_t& length); `
:::

::: indent
` bool supportsAsyncRead(); `
:::

The client calls `readRequest()` to tell the bus interface that it
expects input. Depending on the bus, this function might have to set the
bus hardware into receive mode. If `expectedLength>0`, the the bus
interface should stop input after this number of bytes have been
received. In opposite to writing, the device may be in a non-locked
status when `readRequest()` is called.

This function must not block until input is available. Instead, it
should arrange for `readCallback(StreamIoSuccess, buffer, size)` to be
called when input has been received and return `true` immediately or
`false` if the request cannot be accepted.

Here, `buffer` is a pointer to `size` input bytes. The bus interface is
responsible for the buffer. The client copies its contents. It does not
modify or free it.

It is not necessary to wait until all data has been received. The bus
interface can call `n=readCallback()` after any amount of input has been
received. If the client expects more input, `readCallback()` returns a
non-zero value. A positive `n` means, the client expects another `n`
bytes of input. A negative `n` means, the client expects an unspecified
amount of additional input.

With some bus interfaces, `readRequest()` might not have to do anything
because the bus is always receiving. It might also be that the bus has
no local buffer associated to store input before it is fetched with some
`read()` call. In this case, a race condition between device and client
can occure. To avoid loss of data,
`readCallback(StreamIoSuccess, buffer, size)` may be called in this case
even before `readRequest()`. If the client is expecting input in the
next future, it will store it. Otherwise the input is dropped.

The `replyTimeout_ms` parameter defines how many milliseconds to wait
for the first byte of a reply before the device is considered offline.
If no input has been received after `replyTimeout_ms` milliseconds, the
bus interface should call `readCallback(StreamIoNoReply)`.

The `readTimeout_ms` parameter is the maximum time to wait for further
input. If input stops for longer than `readTimeout_ms` milliseconds the
bus interface should call `readCallback(StreamIoTimeout,buffer,size)`.
The client decides if this timeout is an error or a legal termination.
Thus, pass all input received so far.

A call to `getInTerminator(length)` tells the interface which terminator
is expected for input and `length` is set to the number of bytes of the
terminator. The result is a hint to the bus interface to recognize the
end of an input. Once the terminator string is found, the bus interface
should stop receiving input and call
`readCallback(StreamIoSuccess, buffer, size)`. It is not necessary to
remove the terminator string from the received input. An empty
terminator string (`length==0`) means: Don\'t look for terminators.

If `NULL` was returned, the client is not aware of a terminator (no
inTerminator was defined in the protocol). In this case, the interface
may look for a terminator which it knows from other sources, reduce size
by the terminator length and call
`readCallback(StreamIoEnd, buffer, size)`. A bus interface is not
required to support `NULL` results and may treat them as empty
terminator (see above).

Some busses (e.g. GPIB) support special \"end of message\" signals. If
such a signal is received, the bus interface should call
`readCallback(StreamIoEnd, buffer, size)`. Use it to indicate a special
\"end of message\" signal which is not visible in the normal byte data
stream. If `getInTerminator()` has not returned `NULL` it it not
necessary to remove a terminator which may come in addition to the \"end
of message\" signal.

If input is impossible, for example because there is something wrong
with the I/O hardware, `readCallback(StreamIoFault)` may be called.

Sometimes a client wishes to get any input received at any time, even
when requested by another client. If a client wishes to receive such
asynchronous input, it first calls `supportsAsyncRead()`. The default
implementation of this method always returns `false`. If a bus interface
supports asynchronous input, it should overwrite this method to set up
everything needed to receive asynchronous input and then return `true`.
The client is then allowed to call `readRequest()` with the
`async==true`. This means that the client is now interested in
asynchronous input. It should receive a `readCallback()` of all input
which came in response to any synchonous (`async==false`) request from
another client (which should receive the input, too). The interface
should also receive asynchronous input when no synchonous client is
active at the moment. Many asynchronous `readRequest()` calls from
different clients may be active at the same time. All of them should
receive the same input.

For asynchronous requests, `replyTimeout_ms` has a different meaning: If
the bus interface has to poll the bus for input, it may take
`replyTimeout_ms` as a hint for the poll period. If many asynchronous
requests are active at the same time, it should poll with the shortest
period of all clients. An asynchronous request does not time out. It
stays active until the next input arrives. The client may reissue the
asynchronous `readRequest()` from within the `readCallback()` if it
wants to continue receiving asynchronous input.

If the client calls `finish()` at any time, the bus interface should
cancel all outstanding requests, including asynchronous read requests.

[]{#event}

### Handling events

::: indent
` bool supportsEvent(); `
:::

::: indent
` bool acceptEvent(unsigned long mask, unsigned long timeout_ms); `
:::

::: indent
` void eventCallback(StreamIoStatus status = StreamIoSuccess); `
:::

An event is a sort of input from a device which is not part of the
normal byte stream. One example is the SRQ line of GPIB. Not all bus
types have events. To support events, the bus interface must overwrite
`supportsEvent()` to return `true`. The default implementation always
returns `false`.

If `true` is returned, the client is allowed to call `acceptEvent()`,
where `mask` defines the (bus dependent) type of event or events to wait
for. If `mask` is illegal, `acceptEvent()` should return `false`. The
call to `acceptEvent()` must not block. It should arrange to call
`eventCallback()` when the event matching `mask` arrives within
`timeout_ms` milliseconds. If no such event arrives within this time,
the bus interface should call `eventCallback(StreamIoTimeout)`.

To avoid race conditions, the bus interface should buffer events and
also report a matching event which occured before the actual call to
`acceptEvent()` but after any previous call of any other request method
like `writeRequest()`.

Dirk Zimoch, 2018
