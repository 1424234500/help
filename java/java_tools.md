
## jdk 工具
#### jcmd --help
jdk1.7 后的万能工具箱 导出堆、查看Java进程、导出线程信息、执行GC、还可以进行采样分析 
```
jcmd ${pid} help 
jcmd ${pid} VM.native_memory summary	
#The following commands are available:
	VM.native_memory  [summary | detail | baseline | summary.diff | detail.diff | shutdown] [scale= KB | MB | GB] 
		依赖 jvm 参数 -XX:NativeMemoryTracking=detail	查看原生内存信息 nmt 	!!! 带来5%-10%的性能损耗 
		# summary: 分类内存使用情况.
		# detail: 详细内存使用情况，除了summary信息之外还包含了虚拟内存使用情况。
		# baseline: 创建内存使用快照，方便和后面做对比
		# summary.diff: 和上一次baseline的summary对比
		# detail.diff: 和上一次baseline的detail对比
		# shutdown: 关闭NMT

	ManagementAgent.stop
	ManagementAgent.start_local
	ManagementAgent.start
	VM.classloader_stats	类加载器
	GC.rotate_log 
	Thread.print	线程快照	jstack
	GC.class_stats	-XX:+UnlockDiagnosticVMOptions
	GC.class_histogram	堆直方图查看：查看系统中类统计信息
	GC.heap_dump $file_jmap		导出堆信息==jmap
	GC.finalizer_info
	GC.heap_info	gc堆状态统计	jvm代metaspace占用情况!!!
	GC.run_finalization
	GC.run	执行gc!!!
	VM.uptime
	VM.dynlibs	动态链接库?
	VM.flags	获取启动参数
	VM.system_properties	获取系统Properties内容
	VM.command_line	启动参数命令
	VM.version	虚拟机版本
	PerfCounter.print	获取所有性能相关数据
	help
```

##### jstat --help gc分析 
jstat -gc ${pid} [2000 2S定时查询] [4 采样4次]
```
	pid=$1
	[ -z "${pid}" ] &&  echo 'eg: ./make.sh ${pid} ' && exit 1 
	#https://docs.oracle.com/javase/7/docs/technotes/tools/share/jstat.html
	jstat -gc ${pid}  	#垃圾回收统计 
	jstat -gccapacity ${pid}  	#垃圾回收内存统计 
	jstat -gccause ${pid}  	 
	jstat -gcnew ${pid}  	 
	jstat -gcnewcapacity ${pid}  	 
	jstat -gcold ${pid}  	#old
	jstat -gcoldcapacity ${pid}  	 
	#exe jstat -gcpermcapacity ${pid}  	#jdk7 永生代 内存统计
	jstat -gcmetacapacity ${pid}  	#JDK8 元空间 内存统计
	jstat -gcutil ${pid}  	#总结垃圾回收统计	Summary of garbage collection statistics
	echo 'over' 

	#-gc Option Garbage-collected heap statistics 
	S0U=Survivor 0 Used/S0C=Survivor 0 Capacity	  已用/容量	(KB).
	EC/EU=Eden	OC/OU=Old	PC/PU=Permanent	MC/MU=Mentaspace	
	YGC 次数/YGCT 耗时	young gc 	
	FGC 次数/FGCT 耗时 	full gc
	GCT=Total garbage collection time.	gc总耗时
	#-gccapacity Option 
	NGCMN/NGCMX/NGC	年轻代young min/max/now当前容量
	OGCMN/OGCMX/OGC	老年代old  min/max/now当前容量  
	PGCMN/PGCMX/PGC	永久代pert min/max/now当前容量   
	MCMN/MCMX/MC	元空间meta min/max/now当前容量   
```

### pmap --help
名称：
       pmap - report memory map of a process(查看进程的内存映像信息)
用法
       pmap [ -x | -d ] [ -q ] pids...
       pmap -V
选项含义
       -x   extended       Show the extended format. 显示扩展格式
       -d   device         Show the device format.   显示设备格式
       -q   quiet          Do not display some header/footer lines. 不显示头尾行
       -V   show version   Displays version of program. 显示版本
扩展格式和设备格式域：
        Address:  start address of map  映像起始地址
        Kbytes:  size of map in kilobytes  映像大小
        RSS:  resident set size in kilobytes  驻留集大小
        Dirty:  dirty pages (both shared and private) in kilobytes  脏页大小
        Mode:  permissions on map 映像权限: r=read, w=write, x=execute, s=shared, p=private (copy on write)  
        Mapping:  file backing the map , or '[ anon ]' for allocated memory, or '[ stack ]' for the program stack.  映像支持文件,[anon]为已分配内存 [stack]为程序堆栈
        Offset:  offset into the file  文件偏移
        Device:  device name (major:minor)  设备名
 
### jmap --help 	headdump 获取方式
jmap [option] $pid
jmap [option] [server_id@]<remote server IP or hostname>
    -<none> 这个意思是说，jmap可以不加任何option参数信息，只是指定Java进程的进程号。这种情况下，jmap命令将按照Linux操作系统进程内存分析命令pmap的相关性，输出内存分析结果。
    -heap 查看整个JVM内存状态   改参数将输出当前指定java进程的堆内存概要信息 
    -clstats 该参数将打印出当前java进程中，存在的每个类加载器，以及通过该类加载器已经完成加载的各类信息，包括但不限于类加载器的活动情况、已经加载的类数量、关联的父类加载器等等(class文件通过类加载器完成的载入、连接、验证初始化等过程可以在这个命令的输出详情中具体体现出来)。
    finalizerinfo 该参数可打印出等待终结的对象信息，当Java进程在频繁进行Full GC的时候，可以通过该命令获取问题的排查依据。
    -histo[:live] 查看JVM堆中对象详细占用情况 该参数可以输出每个class的实例数目、内存占用、类全名等信息。如果live子参数加上后,只统计活的对象数量
    -dump:<dump-options> 取得当前指定java进程堆内存中各个class实例的详细信息，并输出到指定文件。dump命令还有三个子参数分别是。
        live只分析输出目前有活动实例的class信息；
        format输出格式，默认为“b”，可以使用配套的分析软件进行分析；
        file子参数可以指定输出的文件，注意，如果输出文件已经存在，则可以使用-F 参数来强制执行命令。
    eg:
    jmap -dump:format=b,file=文件名 [pid]
 
 
#### 其他辅助工具
//jhat -J-Xmx1024M $jmap_file #在线html分析headdump http://127.0.0.1:7000
jvisualvm $file_jmap	#图形化分析工具 jconsole的升级版? #可在线跟踪 java pid	也可以分析  dump 文件 hprof
ha456.jar	ibm分析堆工具 dump
jca457.jar	ibm分析 javacore 工具
gcviewer.jar  gc分析工具