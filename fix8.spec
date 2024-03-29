Summary: C++ Development Library and Engine for the FIX protocol
Name: fix8
%define fullversion 1.4.0
Prefix: %{_prefix}
Version: 1.4.0
Release: 300322
License: LGPL
Group: Development/Libraries
URL: http://www.fix8.org
Vendor: David L. Dight
Source: https://github.com/fix8/fix8/archive/%{name}-%{fullversion}.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root

Requires: poco-net >= 1.4
Requires: poco-foundation >= 1.4
BuildRequires: poco-devel >= 1.4
BuildRequires: perl-XML-Parser
#ExcludeArch: %{arm}

%description
A modern open source C++ FIX framework featuring complete schema driven customisation, high
performance and fast application development.

Fix8 helps you get your FIX protocol client or server up and running quickly. Using one of the standard FIX schemas you
can have a FIX client or server up and running in next to no time.
Statically compile your FIX xml schema and quickly build your FIX application on top. If you need to add customised
messages or fields, simply update the schema and recompile.
Fix8 is the fastest C++ Open Source FIX framework. Our testing shows that Fix8 is on average 68% faster encoding/decoding
the same message than Quickfix.
Fix8 supports standard `FIX4.X` to `FIX5.X` and `FIXT1.X`. If you have a custom FIX variant Fix8 can use that too.
New FIX versions will be supported.
Fix8 offers message recycling and a meta-data aware test harness. Incorporates lock free queues, atomics and many
other modern techniques.
Fix8 contains a built-in unit test framework that's being continually revised and extended. Fix8 also has a metadata
driven test harness that can be scripted to support captured or canned data playback.
Fix8 is a complete C++ FIX framework, with client/server session and connection classes (including SSL); support for
the standard FIX field types; FIX printer, async logger, async message persister and XML configuration classes.
Fix8 statically supports nested components and groups to any depth. The Fix8 compiler and runtime library takes the
pain out of using repeating groups.
Leverage standard components. Fix8 optionally uses industry recognised components for many important functions,
including Poco, TBB, Redis, Memcached, BerkeleyDB, Fastflow, Google Test, Google Performance Tools, Doxygen
and more. We didn't reinvent the wheel.
Fix8 applications are fast. On production level hardware, client NewOrderSingle encode latency is now 2.1us, and
ExecutionReport decode 3.2us. Without the framework overhead, NewOrderSingle encode latency is 1.4us. This is being continually improved.
Fix8 has been designed to be extended, customised or enhanced. If you have special requirements, Fix8 provides a
flexible platform to develop your application on.
Fix8 supports field and value domain validation, mandatory/optional field assertion, field ordering, well-formedness
testing, retransmission and standard session semantics.
Fix8 runs under industry standard Linux on IA32, x86-64, Itanium, PowerPC and ARMv7. It also now runs on *Windows*
and *OSX*. Other *NIX variants may work too.

%prep
%setup -n %{name}-%{version}

%build
%configure --with-sleep=250 --enable-gtest=no --enable-doxygen-warnings=no
%{__make}

%install
%make_install

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%{_bindir}/f8c
%{_bindir}/f8print
%{_bindir}/f8test
%{_bindir}/harness
%{_bindir}/hfprint
%{_bindir}/seqedit
%{_bindir}/hftest
%{_libdir}/libfix8.la
%{_libdir}/libfix8.so
%{_libdir}/libfix8.so.1
%{_libdir}/libfix8.so.1.0.3
%{_libdir}/libhftest.la
%{_libdir}/libhftest.so
%{_libdir}/libhftest.so.0
%{_libdir}/libhftest.so.0.0.0
%{_libdir}/libmyfix.la
%{_libdir}/libmyfix.so
%{_libdir}/libmyfix.so.0
%{_libdir}/libmyfix.so.0.0.0
%{_exec_prefix}/include/fix8
%{_exec_prefix}/share/fix8

%changelog
* Fri Sep 16 2016 David L. Dight <fix@fix8.org> 1.4.0
- Fixed Jira tickets FX-530,FX-533,FX-539,FX-562,FX-563,FX-564,FX-560,FX-588,FX-569,
							FX-596,FX-642,FX-633,FX-615,FX-609,FX-655
- Added verison tag to Nuget packages
- Fixed Seqedit reports corrupted persister index
- Added Provide programmatic way to set reset sequence number flag on logon
- Fixed XML parser should report line numbers of mismatched element start/end
- Added Compiler should optionally report unused tags
- Added Session should provide callback for rejected inbound message
- Fixed XmlData fields unsupported
- Fixed Rejected inbound messages do not appear in protocol log
- Fixed FIX time to epoch converter
- Fixed Acceptor mode: Crash while receiving logout message
- Fixed Sequence number reset does not function correctly
- Fixed Expected Sequence number reaches extreme and unrealistic value
- Upgraded FastFlow to v2.1.0
- Added ConsoleMenu permit messages to be created from inbound messages
- Added ConsoleMenu SelectMsgFrom now displays message sending time and seqnum if available
- Fixed crash on "Send one message, optionally save before send"
- Fixed f8c unhandled exception while stoul'ing fields
- Fixed login_retries="0" not working
- Fixed Expected Sequence number reaches extreme and unrealistic value
- Fixed Crashes on heartbeat

* Sun Aug 23 2015 David L. Dight <fix@fix8.org> 1.3.4
- Fixed Jira tickets FX-508, FX-511, FX-490, FX-491, FX-480, FX-470, FX-336, FX-525, FX-524,
							FX-523, FX-520, FX-516, FX-527
- Client logout crashes FIX server
- SessionWrapper needs to be cleaned up in the destructor
- Fixed Seqedit reports corrupted persister index
- Fixed compile errors on OSX
- Fixed Provide hook in Session to modify header before sending
- Fixed ReliableClientSession crash when connection failed
- Fixed Crash on sending cloned message
- Added Provide optional improved checksum calculation
- Added Provide Consolemenu method to remove msg from list and return to application
- Fixed Replace get_value<> with stoi, stoul, stof, etc
- Added Provide non-const header and trailer accessors
- Fixed With f8config installed in system includes, #defines causes namespace pollution
- Fixed Test harness improvements, testing

* Fri Apr 24 2015 David L. Dight <fix@fix8.org> 1.3.3
- Fixed Jira tickets FX-321, FX-319, FX-336, FX-480
- Fixed Provide capability to build stock FIX libraries
- Fixed seqedit Poco linkage prolem
- Added CMake find_package support
- Fixed ssout_xxxx() macros can be used outside FIX8 namespace
- Fixed Schedule::test bug fix for calculating "today" in local time zone
- Fixed support application framework to manage all purmutations of process_model and mode
- Fixed issue in MessageBase::clear
- Fixed XML parser does not support CDATA values
- Fixed ReliableClientSession crash when connection failed
- Fixed Client logout crashes FIX server

* Fri Jan 02 2015 David L. Dight <fix@fix8.org> 1.3.2
- Fixed Jira tickets FX-394, FX-385, FX-379, FX-372, FX-371, FX-355, FX-353, FX-350, FX-321,
							FX-328, FX-326, FX-307, FX-332, FX-333, FX-369, FX-354, FX-323
- Fixed f8test client and server core dumps on exit when compiled with stdthread
- Fixed copy_legal causes segfault on windows
- Fixed schedule is_valid() returns true even schedule is invalid under win
- Fixed Fix8 has empty timestamps under windows
- Fixed client session reconnect failure after previous abnormal session disconnect
- Fixed unhandled message and reject problems
- Fixed invalid tag in test log of Win build
- Fixed Tickval::todouble returning 0
- Fixed provide capability to build stock FIX libraries
- Fixed improve VS2013 build wth stock FIX schemas
- Fixed replace time/date handling (Tickval) with C++11 std::chrono
- Fixed ReliableClientSession crash when socket connection refused
- Fixed Fix8 test harness (client) improvements
- Fixed provide support for longname field lookup
- Fixed add git revision & fix8 version reporting to log during fix8 start
- Fixed crashing in hftest of Win build
- Fixed on exit when using std::thread, logger reports "resource deadlock avoided"

* Sun Aug 24 2014 David L. Dight <fix@fix8.org> 1.3.1
- Fixed Jira tickets FX-325
- 1.3 build bug under Win

* Sun Aug 17 2014 David L. Dight <fix@fix8.org> 1.3.0
- Fixed Jira tickets FX-309, FX-308, FX-307, FX-306, FX-305, FX-304, FX-303, FX-302, FX-301,
							FX-300, FX-299, FX-298, FX-296, FX-295, FX-294, FX-293, FX-292, FX-291,
							FX-290, FX-289, FX-288, FX-287, FX-286, FX-236, FX-310, FX-312, FX-311
							FX-297, FX-281, FX-233, FX-231, FX-313, FX-315, FX-316, FX-317, FX-318
							FX-319
- Provide XML logger
- Overhaul logging system
- Loggers should support log level
- Allow shallow message construction
- Provide Message::move_legal
- XML parser does not support CDATA values
- gcc 4.7.2 linux build broken
- Allow shallow message construction
- Provide Message::move_legal
- Facilitate "pass-through" fields which are not mentioned in the Dictionary
- MAGIC_NUM expression can cause problems
- Support package and configuration string queries
- Provide flag settings to control XML parser
- Remove main Nuget package link dependency to gtest
- Replace FIX8::dthread with std::thread
- ReliableClientSession crash when socket connection refused
- Compilation error on clean checkout 14/07/10
- Protocol Logger Thread is not destroyed after deleting session
- Wrong Timer implementation
- RAII std::ostream Singleton log target
- GlobalLogger::create_instance needs refactoring
- Precision was altered unintentionally
- Support flattened field query in messages
- Allow SingleLogger to accept user defined LogFlags
- Add mini-timestamp flag to logger
- hftest server exits when sending preloaded messages under windows
- Update on 14-06-24 introduced build warnings on win
- Fix variadic templates compile error under VS2013
- Windows build fails when configured w/o TBB
- Create VS2012 build of FIX8
- Provide programmatic/generic method of loading and using Fix8 metadata
- Permit lookup of fields and messages by their long name
- Xml improvements: find_child, GetLocString
- Field equivalence operators missing
- Option to compiler to generate router stubs without defaults
- Session state does not changed when connection goes down.
- Allow the option to the getters from a fix message those values that are fixed point values to be stored in float instead of double
- Make dist, rpmbuild and pro build broken
- Make nuget package generation files (*.autopkg) to be version independent

* Wed Jun 04 2014 David L. Dight <fix@fix8.org> 1.2.0
- Fixed Jira tickets FX-278, FX-276, FX-275, FX-274, FX-273, FX-272, FX-271, FX-270, FX-269,
							FX-268, FX-267, FX-266, FX-265, FX-264, FX-263, FX-228, FX-261, FX-260,
							FX-259, FX-258, FX-257, FX-256, FX-253, FX-252, FX-251, FX-250, FX-249,
							FX-248, FX-247, FX-246, FX-245, FX-244, FX-243, FX-242, FX-241, FX-240,
							FX-239, FX-238, FX-237, FX-236, FX-235, FX-233, FX-232, FX-231, FX-230,
							FX-229, FX-282, FX-280, FX-279, FX-283, FX-285, FX-176, FX-220, FX-195,
							FX-217
- Provide access to raw inbound and outbound FIX message text
- Make --enable-extended-metadata work in windows
- Provide a session configuration option to enable or disable retransmission
- Provide tabsize setting to customise fix printer
- Update wiki with instruction of building NuGet packages
- On Mac OS X Maverick, clang generates lots of warnings
- building with --enable-tbb-malloc=yes on OS X gives error
- poco error under OS X Maverics
- Realm range not working as expected
- Poco On Windows
- Add a few helper methods to BaseEntry and BaseMsgEntry
- Mandatory fields not propagating through compiler with FIXT
- MarketDataRequest with certain fields throws exception invalid field
- default_appl_ver_id (1137) applied if configured, regardless of FIX version
- Example of how to subscribe to MarketData
- Distinguish between invalid and unknown field exceptions in message
- Replace StaticTable with std::map
- Facilitate Fix8Pro and open source common build
- Segfault in ~Session::Session/Session:stop
- Create FIX8 NuGet package
- Create a .net port of fix8
- Upgrade bundled FastFlow from 2.0.2 to 2.0.4
- Replace FIX8::f8_atomic with std::atomic
- FX-242 Write Fix8 1.1 to 1.2 migration guide
- Replace all the sizes from unsigned to size_t
- OSX g++-4.2.1 on mac does not support -fno-var-tracking-assignments.
- Invalid inbound acceptor SenderCompID ignored
- Create OSX HOWTO in Confluence
- Acceptor SenderCompID not configurable
- Provide test example for multi-session support
- Provide support for underlying FieldType introspection
- Support optional CompID enforcement
- Replace FIX8::scoped_ptr with std::unique_ptr
- Client logs should be created with SessionID suffix
- Restructure Session wrapper classes to support non-templated base classes
- Allow user to set SO_KEEPALIVE option from config
- Complete confluence documentation for 1.1.0 and 1.2.0 features
- Provide support and management for multiple ServerInstances
- Server support for predefined set of remote SenderCompIDs
- Allow user to set SO_REUSEADDR option from config
- Allow user to set SO_LINGER option from config
- Support defaults section in Session xml configuration
- FX-41 Replace FIX8::dthread with std::thread
- Add option to FIX8::logger to suppress LF on logline
- Windows build fails when configured w/o TBB
- Linux End-of-Line Charactor not handled by Message::factory
- hftest server exits when sending preloaded messages under windows
- f8print will not decode f8test runs properly
- Cmd line scripts do not like spaces in path when building fix8 under Windows
- Move compilation to use precompiled header

* Sun Apr 06 2014 David L. Dight <fix@fix8.org> 1.1.0
- Fixed Jira tickets FX-223, FX-222, FX-221, FX-219, FX-216, FX-214, FX-213, FX-212, FX-211, FX-209,
							FX-206, FX-205, FX-204, FX-200, FX-198, FX-193, FX-192, FX-191, FX-189, FX-187,
							FX-185, FX-183, FX-180, FX-178, FX-177, FX-175, FX-184, FX-224, FX-225, FX-226,
							FX-227, FX-203, FX-230
- Fixed Win64 build failed with seqnum mismatch
- Fixed f8c compiler crashes if schema file not found
- Fixed Logfile creation should handle new paths
- Added session state change event callback
- Fixed Won't reconnect if exchange log session out.
- Fixed Deadlock in retransmission behaviour
- Added global logger needs optional file and line attributes when logging
- Added provide redis persister
- Fixed Session silently ignores no logger, no plogger and no persister errors
- Fixed Speedup Win build
- Update Windows Wiki (confluence) page
- Fixed Make auto linking fix8 lib optional
- Fixed Remove public static vars from generated code
- Fixed hftest works incompletely under win32/64
- Added malloc configuration defines to f8config.h
- Fixed Test fix8 with onload/SFC 10G cards
- Fixed Reliable session fails to re-connect on connection errors
- Fixed UTs build fails when running via make
- Add support for Session based BusinessMessageReject ('j')
- Added support for Session login and logout time
- Added make socket read buffering optional
- Added expose FIX8::Session scheduler to user session class
- Added support for Session Start time and End Time
- Fixed Hang in FIXReader::sockRead
- Fixed gcc 4.2 and greater supports -fno-var-tracking -fno-var-tracking-assignments
- Fixed Complete build options for Pthread API
- Added message handling: allow non-const operations
- Fixed Non-standard XML attribute comment problem
- Added mechanism to support ad-hoc message recycling
- Added permit alternate source/header extensions when generating code
- Added generic access to key/value pair put() and get() in Persister
- Added precompiled header to f8c generated files
- Fixed f8print will not decode f8test runs properly

* Thu Jan 16 2014 David L. Dight <fix@fix8.org> 1.0.0
- Our first official GA release
- Fixed Jira tickets FX-107, FX-129, FX-130, FX-131, FX-134, FX-139, FX-140, FX-141, FX-142, FX-143,
							FX-144, FX-146, FX-147, FX-149, FX-150, FX-151, FX-157, FX-158, FX-159, FX-161,
							FX-162, FX-163, FX-164, FX-165, FX-166, FX-167, FX-168, FX-169, FX-170, FX-173,
							FX-174
- Provide support for basic client failover capability
- Make connection timeout configurable
- Add support for non-standard XML attribute comments
- Add support for OSX
- Add repeating group test cases for permissive mode
- Support a permissive message field mode in decoder
- Provide override to -fno-var-tracking-assignments
- Fixed Session::send_process() dumps core in reliable mode if client drops connection before login
- Added When working in coro mode there has to be a flag that session is ready to operate
- Added When working in coro mode reader.execute() calls to base class operator()
- Merged fix8:dev with fix8:master
- Added MonthYear and LocalMktDate Date Formats
- Fixed f8test doesn't work as expected
- Fixed clang 3.2-3.4 compilation warnings
- Fixed Sending of FIX message takes too long
- Added Batch message sending
- Fixed MessageBase::extract_element(..., f8String& tag, f8String& val) is ineffective
- Fixed FIXReader calls sockRead too many times
- Added Make includes relative to project root
- Added SSL support
- Fixed XmlElement::find with attribute and value not finding correctly
- Fixed Segfault with non-set SessionConfig on heartbeat
- Added Support custom field addition on f8c command line
- Fixed Fields of type 'data' are not parsed according to FIX specification
- Fixed time_to_epoch tm_mon ternary operator does not allow January dates to be converted to an epoch timestamp
- Fixed Makefile.am does not reference f8dll.h
- Fixed Build error on OS X -rdynamic
- Fixed error: 'uint32_t' does not name a type
- Fixed CLOCK_REALTIME error on compilation on Windows
- Fixed Make include guards standard-compliant
- Code freeze for GA 1.0.0 final

* Sun Nov 10 2013 David L. Dight <fix@fix8.org> 0.10.0
- Fixed Jira tickets FX-102, FX-103, FX-104, FX-105, FX-107, FX-110, FX-113, FX-114, FX-115, FX-116, FX-119, FX-120,
-                    FX-122, FX-124, FX-127
- Fixed allow sender to take ownership of messages after send
- Fixed removed message recycling
- Fixed session::send not thread safe with multiple senders in threaded mode
- Fixed TBB allocator is not used when linking to tbb
- Fixed there is no itoa for int64
- Fixed hb interval is set 1 when using reliable connection
- Fixed multiple instances of FIX8 session share the last messages table
- Fixed groups with 0 elements are not processed
- Fixed error when sending message with BodyLength > 9999
- Fixed issues with Windows build
- Added Fix8 include path in generated files are now configurable
- Added -P switch to f8c to embed fix8 in include paths
- Added order batch send mode
- Added allow application to detach messages when received from framework: Session::handle_application API change
- Added provide way to set default precison for floating point values

* Sun Oct 13 2013 David L. Dight <fix@fix8.org> 0.9.6
- Fixed Jira tickets FX-76, FX-93, FX-94, FX-95, FX-96, FX-97, FX-98, FX-99, FX-100, FX-101
- Decode latency reduced; throughput now 3x quickfix
- Fixed SIOF - static initialisation inconsistent on different platforms; use ctx() instead of ctx
- Fixed compiler treats all repeating groups with the same name as common
- Fixed core dump on message or field instantiation
- Resolved not build tests on centos 6.4
- Fixed required Fields in Optional Components Should be Flagged as Optional
- Fixed remove FieldTraits reserve behaviour
- Added provide switch to suppress doxygen warnings
- Added missing some date/time related fields
- Fixed Fix8 does not build properly on arm. Test cases build and pass on ARMv7
- Fixed link dependencies for clang compilation
- Added -C switch to f8c to turn off version checking
- Added -I switch to f8c, providing more info about build config and platform
- Added -W switch to f8c, to suppress warning messages

* Sun Sep 22 2013 David L. Dight <fix@fix8.org> 0.9.5
- Fixed Jira tickets FX-78, FX-79, FX-80, FX-81, FX-82, FX-83, FX-84, FX-85, FX-86, FX-87, FX-88,
- 							FX-89, FX-90, FX-91, FX-29, FX-92
- Fixed SendingTime and TransactTime not being output by Fix8 printer
- Added compiler option to suppress realm use during field construction
- Replaced Poco::DateTime with custom date time parser, reduced decode latency ~ 20%
- Fixed f8c compiler crashing on exit
- Fixed Incorrect sequence number in GenerateSequenceReset
- Removed coroutine process mode spinlocks
- Workaround for f8test not building on low memory platforms or with older compilers
- Skip formal decode of some header/trailer fields
- Fixed error checking on logfile creation
- Fixed F8MetaCntx::_bme.find() not returning end() if not found
- Fixed ignore_logon_sequence_check check core dumping in client
- Added permit applications to by-pass chksum checking
- Replace field string parameter with const char *
- Fixed generated files should not build with newer framework versions
- Fixed replace compiler f8c generated instantiators with compiler generated versions
- Fixed bug with some linux distros, threaded sessions core dump on exit
- Replaced #ifdef 0 comment blocks with /* ... */
- Templated Field::add_field
- Improved fix printer formatting, removed incorrect group metadata
- Added rdtsc option for codec timing
- Added set_scheduler and set_affinity support

* Sun Aug 25 2013 David L. Dight <fix@fix8.org> 0.9.4
- Merged in Richard Bourne's Windows port.
- Fixed Jira tickets FX-72, FX-73, FX-74, FX-75
- Merged from evdubs: remove the friend declaration in f8_scoped_lock_impl
- Fixup package spec for pre-release to Fedora (now builds on f20 rawhide)
- Added ReliableClientSession::has_given_up()
- Fixed: Gcc locks up with compiler generated traits file; reduced _traits.cpp file by 40%
- Fixed: Compile error with gcc 4.8.1
- Fixed: XML character entity parsing broken; extended entity set;
- Fixed: XML parser does not provide meaningful indication of errors.

* Sun Aug 04 2013 David L. Dight <fix@fix8.org> 0.9.3
- Fixed Jira tickets FX-67, FX-68, FX-69, FX-70, FX-71
- Fixed race condition in Singleton
- Added backup the persist file instead of purging after sequence reset
- Added forced logout message should contain error text
- Fixed server crashes when reliable client attempts sync reconnect
- Fixed reset sequence number not truncating BDB persist database

* Sun Jul 21 2013 David L. Dight <fix@fix8.org> 0.9.2
- Fixed Jira tickets FX-64, FX-65, FX-66
- Merged Neomantra changes allows Fix8 to be built using C++11 compiler
- Fixed sequence reset persist database not purged
- Fixed reset sequence number on logon not working
- Fixed persister not writing any data

* Sat Jun 29 2013 David L. Dight <fix@fix8.org> 0.9.0
- Fixed Jira tickets FX-57, FX-58, FX-59, FX-60, FX-61, FX-62, FX-63
- Logflags - support specific inbound and outbound flags for protocol logs
- Replace cfpopen with non GPL replacement
- Fixed compiler generated include guards do not work if alternate output directory specified.
- Fixed f8c compiler - can't specify output directory by "-o" as expected
- Remove header/trailer field lookups in encode and decode
- Fixed unit tests not building properly
- Add optional coroutine version of FIX reader and writer

* Fri May 10 2013 David L. Dight <fix@fix8.org> 0.8.0
- Fixed Jira tickets FX-56, FX-55, FX-54, FX-53, FX-52, FX-51, FX-50, FX-49, FX-48, FX-47, FX-46, FX-45, FX-31
- Integrate a 3rd party unit testing framework
- Integrate gperf tcmalloc alternate heap allocator
- Modify session to force sequence number assignment when requested
- Improve fmt_chksum routine
- Implement hash array index lookup for fields
- Provide component metadata visibility
- Replace double field encode (sprintf) with modp_dtoa
- Remove custom field support
- Remove some virtual methods from fields and generated messages
- Fix Fastflow install not placing includes in correct path
- Fix MemoryPersister::get not handling end record situation correctly
- Fix Invalid Session::handle_resend_request not resetting session state
- Fix In get_last_seqnum(unsigned& to) of MemoryPersister, can't get last seqnum from the argument "to"
- Fix hftest preload should preload on startup

* Sun Apr 07 2013 David L. Dight <fix@fix8.org> 0.7.2
- Fixed jira tickets FX-23, FX-35, FX-36, FX-37, FX-38, FX-39, FX-40, FX-42, FX-43, FX-44, FX-17
- Partial implemntation of stack based messages.
- TBB optional; Fastflow now used; pipelining options; codec timings improvements;
- Added man-pages for seqedit and f8c
- Fixed under load, server disconnects client reporting it has timed out on receiving messages
- Provide utility to edit next send/expected receive in persistence files
- Investigate and perhaps deploy fastflow lock free containers to replace TBB
- Permit selection of pipelined or non-pipelined operation, through session config
- Change performance test application to provide better measure of codec performance
- Make Intel TBB optional
- Fixed FileLogger::rotate() not working as expected
- Use FastFlow queue processing
- Fixed FIXReader, FIXWriter dropping bytes when buffers full
- Fixed build hftest issue

* Sat Feb 23 2013 David L. Dight <fix@fix8.org> 0.7.0
- File based persistence now implemented and default. Dependence on BerekelyDB removed.
- rpmbuild will now create an rpm from fix8.spec
- Fixed jira tickets FX-34, FX-33, FX-32, FX-30, FX-29, FX-28
- XML parser accepts embedded spaces between attribute, '=' and attribute value
- Provide mechanism for client or server to set next expected send/receive sequence number
- Client correctly handling sequence_reset from server
- Multiple server sessions write to different logs and persistence files
- Permit applications to by-pass chksum checking
- Chksum logic correctly comparing calculated to passed value

* Mon Jan 28 2013 David L. Dight <fix@fix8.org> 0.6.7
- Fixed jira issues: FX-17, FX-19, FX-20, FX-21, FX-24, FX-26, FX-27; Reduction in encode/decode latency by around 29%

* Sun Dec 16 2012 David L. Dight <fix@fix8.org> 0.6.6
- Fixed jira issues: FX-17, FX-18

* Sun Dec 09 2012 David L. Dight <fix@fix8.org> 0.6.5
- Changed to LGPL; added performance script; fixed jira issues: FX-11, FX-12, FX-13, FX-14, FX-15, FX-16

* Thu Nov 22 2012 David L. Dight <fix@fix8.org> 0.6.4
- Fixed jira issues: FX-4, FX-10

* Sun Nov 18 2012 David L. Dight <fix@fix8.org> 0.6.3
- Fixed jira issues: FX-1, FX-4, FX-5, FX-6, FX-7, FX-8, FX-9

* Tue Oct 23 2012 David L. Dight <fix@fix8.org> 0.6.2
- Changed to GPLv2; added shell command pipe variable import to XML; added xi:include to XML;

* Fri Sep 07 2012 David L. Dight <fix@fix8.org> 0.6.1
- Added configurable max message length(maxmsglen); xml xpath permits absolute xpaths; fixed issue with compiler and msgtype;

* Sat Jul 21 2012 David L. Dight <fix@fix8.org> 0.6.0
- Added buffered logging; redesigned and improved field and message encoding and decoding performance, field lookups and static jump tables; added simple console based metadata driven test harness; compiler optimisations including pruning of unused fields;

* Fri May 25 2012 David L. Dight <fix@fix8.org> 0.5.7
- Added HF test client demonstrating preload and bulk transmit capabilities; encode/decode performance improvements with cached lookups;
- optimised field generation; fast ascii to int/double;

* Sat May 12 2012 David L. Dight <fix@fix8.org> 0.5.5
- Added support to compiler to generate user session class permitting quicker startup development;
- added presorted_set which significantly reduces Message contruction time; added codec and profile compilation switches;

* Sun Apr 29 2012 David L. Dight <fix@fix8.org> 0.5.1
- Optimsed compiler, enforce unique fields; updated schemas and documentation.
- Myfix.cpp now uses FIX5.0SP2.

* Sun Apr 22 2012 David L. Dight <fix@fix8.org> 0.5.0
- Support for FIX5.X and FIXT1.1; Support for nested components and repeating groups; Numerous bug fixes;
- Myfix.cpp now uses FIX5.0SP2.

* Tue Mar 20 2012 David L. Dight <fix@fix8.org> 0.4.17
- Postmessage ctor automatically called;

* Thu Mar 08 2012 David L. Dight <fix@fix8.org> 0.4.16
- reliable nanosleep;pipelogger,bclogger;gzstream append;bug fixes

* Thu Mar 01 2012 David L. Dight <fix@fix8.org> 0.4.15
- Fixed static const in class definition storage linker error; fixed superfluous const level return warnings on functions;
- sequence reset flag support; log entries timestamped at creation; threadcode purging; seqnum seeding;
- numerous bugfixes;

* Sun Feb 19 2012 David L. Dight <fix@fix8.org> 0.4.12
- Config updated - separate out log files into their own entity; added addiitonal log flags;
- retransmission improved; socket conditioning; sequence number enforcement on login; sequence
- number control at message level; session wrappers; reliable client wrapper; improved multithreading;
- updated myfix to use session wrapper; myfix supports seqnum cmd line args;

* Sun Feb 05 2012 David L. Dight <fix@fix8.org> 0.4.10
- Added custom seqnum support; Fixed retransmission behaviour; Added SessionWrapper classes
- to simplify client/server session setup; client connect will retry configurable number of times with interval;
- fixed message field replace, remove and copy_legal; myfix.cpp uses new session wrappers;
- added new config extract methods;

* Fri Jan 27 2012 David L. Dight <fix@fix8.org> 0.4.4
- Fixed checksum and bodylength calculation bugs on encode and decode;
- Test server permits reconnects and detects logout;
- Connection classes shutdown properly, gracefully;

* Mon Jan 23 2012 David L. Dight <fix@fix8.org> 0.4.2
- Moved to github; numerous fixes; documentation and wiki;

* Sat Jan 07 2012 David L. Dight <fix@fix8.org> 0.3.580
- Initial release on sourceforge


