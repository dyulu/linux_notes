Linux Tracing Technologies:
https://www.kernel.org/doc/html/latest/trace/index.html
https://www.kernel.org/doc/Documentation/trace/ftrace.txt

$ mount -t debugfs debugfs /sys/kernel/debug
$ mount | grep debugfs
debugfs on /sys/kernel/debug type debugfs (rw,nosuid,nodev,noexec,relatime)
$ ls  /sys/kernel/debug/tracing/
README                      kprobe_events           set_ftrace_pid
available_events            kprobe_profile          set_graph_function
available_filter_functions  max_graph_depth         set_graph_notrace
available_tracers           options                 timestamp_mode
buffer_percent              per_cpu                 trace
buffer_size_kb              printk_formats          trace_clock
buffer_total_size_kb        saved_cmdlines          trace_marker
current_tracer              saved_cmdlines_size     trace_marker_raw
dyn_ftrace_total_info       saved_tgids             trace_options
dynamic_events              set_event               trace_pipe
enabled_functions           set_event_notrace_pid   tracing_cpumask
error_log                   set_event_pid           tracing_on
events                      set_ftrace_filter       tracing_thresh
free_buffer                 set_ftrace_notrace      uprobe_events
instances                   set_ftrace_notrace_pid  uprobe_profile

$ ls -d /sys/kernel/debug/tracing/*/           # 4 dirs under tracing dir; others are regular files
/sys/kernel/debug/tracing/events/     /sys/kernel/debug/tracing/options/
/sys/kernel/debug/tracing/instances/  /sys/kernel/debug/tracing/per_cpu/

$ /sys/kernel/debug/tracing# cat README 
tracing mini-HOWTO:

# echo 0 > tracing_on : quick way to disable tracing
# echo 1 > tracing_on : quick way to re-enable tracing

 Important files:
  trace			- The static contents of the buffer
			  To clear the buffer write into this file: echo > trace
  trace_pipe		- A consuming read to see the contents of the buffer
  current_tracer	- function and latency tracers
  available_tracers	- list of configured tracers for current_tracer
  error_log	- error log for failed commands (that support it)
  buffer_size_kb	- view and modify size of per cpu buffer
  buffer_total_size_kb  - view total size of all cpu buffers

  trace_clock		-change the clock used to order events
       local:   Per cpu clock but may not be synced across CPUs
      global:   Synced across CPUs but slows tracing down.
     counter:   Not a clock, but just an increment
      uptime:   Jiffy counter from time of boot
        perf:   Same clock that perf events use
     x86-tsc:   TSC cycle counter

  timestamp_mode	-view the mode used to timestamp events
       delta:   Delta difference against a buffer-wide timestamp
    absolute:   Absolute (standalone) timestamp

  trace_marker		- Writes into this file writes into the kernel buffer

  trace_marker_raw		- Writes into this file writes binary data into the kernel buffer
  tracing_cpumask	- Limit which CPUs to trace
  instances		- Make sub-buffers with: mkdir instances/foo
			  Remove sub-buffer with rmdir
  trace_options		- Set format or modify how tracing happens
			  Disable an option by prefixing 'no' to the
			  option name
  saved_cmdlines_size	- echo command number in here to store comm-pid list

  available_filter_functions - list of functions that can be filtered on
  set_ftrace_filter	- echo function name in here to only trace these
			  functions
	     accepts: func_full_name or glob-matching-pattern
	     modules: Can select a group via module
	      Format: :mod:<module-name>
	     example: echo :mod:ext3 > set_ftrace_filter
	    triggers: a command to perform when function is hit
	      Format: <function>:<trigger>[:count]
	     trigger: traceon, traceoff
		      enable_event:<system>:<event>
		      disable_event:<system>:<event>
		      stacktrace
		      dump
		      cpudump
	     example: echo do_fault:traceoff > set_ftrace_filter
	              echo do_trap:traceoff:3 > set_ftrace_filter
	     The first one will disable tracing every time do_fault is hit
	     The second will disable tracing at most 3 times when do_trap is hit
	       The first time do trap is hit and it disables tracing, the
	       counter will decrement to 2. If tracing is already disabled,
	       the counter will not decrement. It only decrements when the
	       trigger did work
	     To remove trigger without count:
	       echo '!<function>:<trigger> > set_ftrace_filter
	     To remove trigger with a count:
	       echo '!<function>:<trigger>:0 > set_ftrace_filter
  set_ftrace_notrace	- echo function name in here to never trace.
	    accepts: func_full_name, *func_end, func_begin*, *func_middle*
	    modules: Can select a group via module command :mod:
	    Does not accept triggers
  set_ftrace_pid	- Write pid(s) to only function trace those pids
		    (function)
  set_ftrace_notrace_pid	- Write pid(s) to not function trace those pids
		    (function)
  set_graph_function	- Trace the nested calls of a function (function_graph)
  set_graph_notrace	- Do not trace the nested calls of a function (function_graph)
  max_graph_depth	- Trace a limited depth of nested calls (0 is unlimited)
  dynamic_events		- Create/append/remove/show the generic dynamic events
			  Write into this file to define/undefine new trace events.
  kprobe_events		- Create/append/remove/show the kernel dynamic events
			  Write into this file to define/undefine new trace events.
  uprobe_events		- Create/append/remove/show the userspace dynamic events
			  Write into this file to define/undefine new trace events.
	  accepts: event-definitions (one definition per line)
	   Format: p[:[<group>/]<event>] <place> [<args>]
	           r[maxactive][:[<group>/]<event>] <place> [<args>]
	           -:[<group>/]<event>
	    place: [<module>:]<symbol>[+<offset>]|<memaddr>
place (kretprobe): [<module>:]<symbol>[+<offset>]%return|<memaddr>
   place (uprobe): <path>:<offset>[%return][(ref_ctr_offset)]
	     args: <name>=fetcharg[:type]
	 fetcharg: %<register>, @<address>, @<symbol>[+|-<offset>],
	           $stack<index>, $stack, $retval, $comm, $arg<N>,
	           +|-[u]<offset>(<fetcharg>), \imm-value, \"imm-string"
	     type: s8/16/32/64, u8/16/32/64, x8/16/32/64, string, symbol,
	           b<bit-width>@<bit-offset>/<container-size>, ustring,
	           <type>\[<array-size>\]
  events/		- Directory containing all trace event subsystems:
      enable		- Write 0/1 to enable/disable tracing of all events
  events/<system>/	- Directory containing all trace events for <system>:
      enable		- Write 0/1 to enable/disable tracing of all <system>
			  events
      filter		- If set, only events passing filter are traced
  events/<system>/<event>/	- Directory containing control files for
			  <event>:
      enable		- Write 0/1 to enable/disable tracing of <event>
      filter		- If set, only events passing filter are traced
      trigger		- If set, a command to perform when event is hit
	    Format: <trigger>[:count][if <filter>]
	   trigger: traceon, traceoff
	            enable_event:<system>:<event>
	            disable_event:<system>:<event>
		    stacktrace
	   example: echo traceoff > events/block/block_unplug/trigger
	            echo traceoff:3 > events/block/block_unplug/trigger
	            echo 'enable_event:kmem:kmalloc:3 if nr_rq > 1' > \
	                  events/block/block_unplug/trigger
	   The first disables tracing every time block_unplug is hit.
	   The second disables tracing the first 3 times block_unplug is hit.
	   The third enables the kmalloc event the first 3 times block_unplug
	     is hit and has value of greater than 1 for the 'nr_rq' event field.
	   Like function triggers, the counter is only decremented if it
	    enabled or disabled tracing.
	   To remove a trigger without a count:
	     echo '!<trigger> > <system>/<event>/trigger
	   To remove a trigger with a count:
	     echo '!<trigger>:0 > <system>/<event>/trigger
	   Filters can be ignored when removing a trigger.
