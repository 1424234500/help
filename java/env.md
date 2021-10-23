``JAVA_HOME
D:\workspace\jdk\jdk1.8.0_131
PATH
%JAVA_HOME%\bin;%JAVA_HOME%\jre\bin

export JAVA_HOME=/mnt/d/linux/jre1.8.0_202
export CLASSPATH=.:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export PATH=$JAVA_HOME/bin:$PATH

//反编译
javap -v ServiceImpl.class
javap -verbose ServiceImpl.class 
J2SE 8 = 52
J2SE 7 = 51
J2SE 6.0 = 50



//tomcat maven web jdk 编译问题
配置  Project Facets 
Dynamic Web Module 3.0
Java 1.8
配置  Java Compiler
jdk1.8
配置  Java Build Path
jdk1.8
配置  Deployment Assembly

配置tomcat特定jdk eclipse 
导入tomcat可选定jdk

idea部署tomcat web项目
artifacts
__:war exploded 
　　热部署
　　不会自动copy配置文件到目录？
___:war
　　发布模式,这是先打成war包,再部署
debug configuration tabs
tomcat
add war artifacts
application context : url !!! /walker-web	#上下文
 
//node  vue
wget https://cdn.npm.taobao.org/dist/node/v12.10.0/node-v12.10.0-linux-x64.tar.xz
xz -d node-v12.10.0-linux-x64.tar.xz
tar -xvf node-v12.10.0-linux-x64.tar
mv node-v12.10.0-linux-x64/ nodejs
echo 'export PATH=$PATH:'`pwd -LP`'/nodejs/bin'  | sudo tee -a /etc/profile
source /etc/profile
配置代理和仓库
npm config delete registry
npm set https-proxy http://xxx
npm set proxy http://xxx
npm set registry https://registry.npm.taobao.org
npm config get registry
核对 c/user/.npmrc
npm -v
npm install vue
项目下
npm install 
  
//eclipse 启动jvm内存 jvm 内存不够oom
Jdk edit 附加参数 -Xmx1024M

//websphere was配置
/washome/IBM/WebSphere/AppServer/bin/startManager.sh
/washome/IBM/WebSphere/AppServer/profiles/AppSrv02/bin/startNode.sh
/washome/IBM/WebSphere/AppServer/profiles/AppSrv02/bin/startServer.sh  server1 --servername

cd /washome/IBM/WebSphere/AppServer/bin  
./manageprofiles.sh -listProfiles	#1.列出现有概要文件
./manageprofiles.sh -validateAndUpdateRegistry	#2.刷新概要文件注册表
./manageprofiles.sh -deleteAll	#3.删除概要文件
./manageprofiles.sh -delete -profileName AppSrv01	#若过于慢 则直接删除对于目录 然后 刷新 然后删除

#创建概要 profile
./manageprofiles.sh -create -profileName  server1 -profilePath /washome/IBM/WebSphere/AppServer/profiles/server1
#启动管理
/washome/IBM/WebSphere/AppServer/profiles/Dmgr01/bin/startManager.sh
#查看端口SOAP	8879
grep SOAP /washome/IBM/WebSphere/AppServer/profiles/Dmgr01/logs/AboutThisProfile.txt
#创建节点 profile
/washome/IBM/WebSphere/AppServer/profiles/AppSrv01/bin/addNode.sh 127.0.0.1 8879
Error: The system cannot create a SOAP connector to connect to host 127.0.0.1 at port 8879
此时 使用命令 hostname 得到主机名
切换到“/washome/IBM/WebSphere/AppServer/profiles/AppSrv02/bin/”下: 
执行 : ./syncNode.sh 主机名 8879

#启动 node
/washome/IBM/WebSphere/AppServer/profiles/AppSrv01/bin/startNode.sh 	#Error:  端口被占用 
#后台登录测试
http://你的ip地址:9060/washome/IBM/console/login.do
#新建服务server1	启动应用服务 开始验证
cd /washome/IBM/WebSphere/AppServer/profiles/AppSrv01/bin/ ; ./startServer.sh server1 
访问不了:注意火墙 

2.简单化配置
不需要创建 _portdef_AppSvr.props以及_portdef_DMgr.props文件
直接创建两个概要

创建管理概要
./manageprofiles.sh
-create
-profileName  Dmgr01
-profilePath  /washome/IBM/WebSphere/AppServer/profiles/Dmgr01
-templatePath  /washome/IBM/WebSphere/AppServer/profileTemplates/dmgr/

创建应用概要
./manageprofiles.sh
-create
-templatePath  /washome/IBM/WebSphere/AppServer/profileTemplates/default 
-profileName  AppSvr02
-profilePath   /washome/IBM/WebSphere/AppServer/profiles/AppSvr02  
这样也是可以的。


##ibm/sun jdk 1.6 1.8 jvm参数说明
https://www.ibm.com/support/knowledgecenter/en/SSYKE2/earlier_releases/earlier_releases.html
配置格式
后置覆盖配置
-X : 非标准选项
 -Xms22M
-XX: 非稳定选项 
 -XX:Xxxx=128M
 -XX:+UseCompressedOops	+启用 压缩指针
 -XX:-UseCompressedOops	-停用 压缩指针

查看jvm xx实时参数
jinfo -flag ThreadStackSize ${pid} 	#查看指定jvm值!
java -XX:+PrintFlagsFinal -version | grep Metaspac

####堆 内存 new old gc
```
分配参数 单位 1[k|K|m|M|g|G]  
-XX:MaxDirectMemorySize=1G	堆外内存max 1.8
-XX:MetaspaceSize=64M	元空间init/max 1.8 -XX:PermSize 1.7  max默认是没有限制的?
-XX:MaxMetaspaceSize=64M

-XX:InitialCodeCacheSize=64M	#Code Cache 代码缓冲区 init/max
-XX:ReservedCodeCacheSize=200M	
-XX:+UseCodeCacheFlushing	启用回收

-XX:CodeCacheExpansionSize=1M	
-XX:CodeCacheMinimumFreeSpace=1M	
-XX:MinMetaspaceExpansion=1M
-XX:MaxMetaspaceExpansion=8M
-XX:CompressedClassSpaceSize=256M
 
-Xmn10M	new init=max 可避免抖动
-XX:NewSize=2M	new init/max
-XX:MaxNewSize=2M 
-XX:NewRatio=2	new:old=2:1
-XX:SurvivorRatio=8	new eden:survivor=8:1
-XX:TargetSurvivorRatio=50	survivor区>50% -> old
-XX:MaxTenuringThreshold=15	survivor->old 年龄 Parallel=15 CMS=6

-Xms128M	堆内init def=Min(1/64,1G) init=max 可避免抖动 OutOfMemoryError
-Xmx256M	堆内max def=Min(1/64,1G) 
-Xss1M	主线程栈	def=1M
-XX:ThreadStackSize=1M	非主线程栈

####gc
-XX:MaxGCPauseMillis=500	 gc 暂停时间 max ms
-XX:+UseAdaptiveSizePolicy	自适应GC策略
-XX:+UseSerialGC	用串行回收器
-XX:+UseParallelGC	用并行垃圾收集器 默认开启并行-old
-XX:+UseParallelOldGC
-XX:ParallelGCThreads=4	gc线程数 def=cpu
-XX:+UseConcMarkSweepGC	用CMS收集器-old
-XX:+CMSClassUnloadingEnabled	启用类元数据回收
-XX:+UseG1GC	用G1回收器
-XX:G1HeapRegionSize=16m	G1-Region size(1M - 32M)
-XX:+DisableExplicitGC	禁用System.gc() 
-XX:+PrintGCDetails	GC日志
-XX:+PrintGCTimeStamps	GC时间戳
-XX:+PrintGCDateStamps	GC日期
-XX:+PrintHeapAtGC	GC时-堆信息
-Xloggc:/home/gc.$$.log	GC日志位置
-XX:+UseGCLogFileRotation	开启滚动日志记录
-XX:NumberOfGCLogFiles=5	滚动命名 f.0, f.1 ...
-XX:GCLogFileSize=8M	每个文件大小

####堆快照
-XX:+HeapDumpOnOutOfMemoryError	开启堆溢出记录快照
-XX:HeapDumpPath=/home/oom.%t.log	堆快照位置
-XX:+UseLargePages	
-XX:LargePageSizeInBytes=4m	大页 2^*
```

 

##cpu冲高400%分析
4c8g 4核cpu 最高 400% 每个线程可能被指派给某单核cpu处理 
######可能原因:
单线程导致 cpu持续100% 死循环(hashmap线程不安全) 无阻塞 正则匹配 复杂计算(6w 大map 大list 遍历)
频繁gc(导致cpu卡顿 毛刺)
多线程的上下文切换
######分析思路
分析业务日志 存在大量集中错误
分析接口请求量级变化(tcp/http io dubbo 监控) 存在异常访问
对比分析集群模式下每台差异 同时冲高 此起彼伏 单台特例

冲高的线程栈javacore/jstack、堆快照headdump/jmap获取 单台多时间节点获取对比变化
linux系统 top H、ps H、nmon、tcp http、db连接池、redis快照...等异常现场信息获取

##### javacore 分析 关注多个javacore中哪些线程一直存在
TITLE	Javacore 产生的原因 时间以及文件的路径
    1TISIGINFO  Dump Event "user"   user: SIGQUIT 信号 gpf: 程序一般保护性错误导致系统崩溃 systhrow: JVM 内部抛出的异常 
GPINFO	GPF(一般保护性错误)信息
ENVINFO	系统运行时的环境和 JVM 参数
MEMINFO	内存使用情况和垃圾回收情况
LOCKS	用户监视器和系统监视器情况
CLASSES	类加载信息
THREADS	所有 java 线程快照 状态信息、执行堆栈
    死锁(Deadlock)【重点】相互资源占用
    执行中(Runnable)【重点】正在使用cpu资源 结合ps H信息看占用了多少cpu 结合线程栈看在干嘛
    等待资源(Waiting on condition)【重点】大量读取某资源 资源锁 线程等待状态
	阻塞(Blocked)【重点关注】所需资源等待超时 被线程管理器标识为阻塞状态
    等待监控器检查资源(Waiting on monitor)
    暂停(Suspended)
    对象等待中(Object.wait())
    停止(Parked)



### 堆分析
https://www.javadoop.com/post/metaspace
https://stuefe.de/posts/metaspace/what-is-metaspace/

### 常见堆外操作
```
	#Netty	nio	-Dio.netty.noUnsafe=true	#默认零拷贝 ByteBuf NioByteUnsafe
	#was ehcache
	https://www.jianshu.com/p/17e72bb01bf1
	#nio-bytebuffer unsafe
	ByteBuffer buffer = ByteBuffer.allocateDirect(10 * 1024 * 1024);
	Unsafe unsafe = Unsafe.getUnsafe();
	unsafe.allocateMemory(1024);
	unsafe.reallocateMemory(1024, 1024);
	unsafe.freeMemory(1024);

	ByteBuffer.allocateDirect
	#GZIPInputStream
		Inflater申请堆外内存
		Deflater释放内存 
		调用close()方法来主动释放  or 延续到下一次GC

	为什么使用堆外内存
	考虑使用缓存时 本地缓存是最快速的 但会给虚拟机带来GC压力
	使用硬盘或者分布式缓存的响应时间会比较长 这时候「堆外缓存」会是一个比较好的选择
	Ehcache 支持分配堆外内存 又支持KV操作 还无需关心GC	被广泛用于Spring 支持堆内 堆外 磁盘 分布式
	堆外内存可以减少GC的压力 从而减少GC对业务的影响 
	https://blog.csdn.net/lycyingO/article/details/80854669
```

   
####分析进程堆外内存 会影响服务 注意dump的内存块大小 慎用
```
	pmap -x ${pid}  | sort -n -k3 -r  > maps.map 	#大量申请64M大内存块的原因是由Glibc
	# total kB        19108352  858872  840348
	#Address           Kbytes     RSS   Dirty Mode   Mapping
	#0x00000000fc000000  196608  196608  196608 rw---    [ anon ]
	#0x00000000e0000000  262144       0       0 -----    [ anon ]
	#
	#head -n 20 maps.map | sed -e "s/\([0-9a-f]\{8\}\)-\([0-9a-f]\{8\}\)/0x\1 0x\2/" | awk '{printf("\033[0;33m[%8d Page]\033[0m \033[0;35m[%8d KB]\033[0m %s\n", (0+$2 - $1)/4096, (0+$2 - $1)/1024, $0)}'
	#导出进程申请的所有内存区块	很多1000+
	grep rw-p /proc/${pid}/maps | sed -n 's/^\([0-9a-f]*\)-\([0-9a-f]*\) .*$/\1 \2/p' | head | while read start stop; do 
		gdb --batch --pid ${pid} -ex "dump memory ${pid}-$start-$stop.dump 0x$start 0x$stop"
	done
	#内存数据精简
	strings -n 10 *dump # 过滤特殊字符和过短行 查看内存
	#结合 jcmd ${pid} help GC.heap_info 可看到java heap各个区 egen old metaspace对应的地址区间 大小都能对上
	#其他则是堆外的断续的大量地址区 结合 jcmd ${pid} VM.native_memory summary/detail 可查看java进程的全内存(内外)情况 可分析堆外||meta的具体dump文件
	#通过各个地址区间查看 内存中大概存了什么内容 

```




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



#### cpu冲高案例 jit
https://www.ezlippi.com/blog/2018/01/linux-high-load.html

#####JIT分层编译
1.8默认开启 1.7 -XX:+TieredCompilation 开启 分为C1客户端编译和C2服务端编译器
编译级别
0: 解释执行 最慢
1: 简单C1编译代码
2: 受限的C1编译代码,不做性能分析 根据方法调用次数和方法内部循环次数来启动
3: 完全C1编译代码,编译器收集分析信息之后做的编译
4: C2编译代码,编译最慢,编译后执行速度最快
jvm启动参数
```
    JIT相关JVM参数简介    只能用于server模式
    选项	默认值	解释
    CompileThreshold	1000 or 1500/10000	编译阈值,方法执行多少次后进行编译
    PrintCompilation	false	jit编译时输出日志
    InitialCodeCacheSize	160K (varies)	初始codecache大小
    ReservedCodeCacheSize	32M/48M	codecache最大值
    ExitOnFullCodeCache	false	codecache满了退出jvm
    UseCodeCacheFlushing	false	codecache满了时清空一半的codecache
    PrintFlagsFinal	false	打印所有的jvm选项
    PrintCodeCache	false	jvm退出时打印codecache
    PrintCodeCacheOnCompilation	false	编译时打印codecache使用情况
```
0最开始都是解释执行
1理想情况下应转成level3编译
2根据C1队列长度和C1编译线程数来调整编译的阈值
3根据C2队列长度可能转向C2编译
4根据C2队列长度、C2编译线程数调整level4编译阈值
如果方法非常小,没什么可以优化的空间 直接转level1编译
最常见的编译层次转换:0 -> 3 -> 4

#####解决方案
1)为了避免CodeCache满导致JIT停止编译或者 CodeCacheFlushing
获取到当前JIT的CodeCache大小  空间可能不够用 另一方面是 CodeCache 是不会回收的 所以会累积的越来越多 推荐调大
//常在64 bit机器上默认是48m 当 code cache 用满了后 编译优化就被禁掉了 此时会回归到解释执行 RT可想而知不会好到哪去
jinfo -flag ReservedCodeCacheSize ${pid}
jinfo -flag InitialCodeCacheSize ${pid}
-XX:InitialCodeCacheSize=2 555 904
-XX:ReservedCodeCacheSize=251 658 240
根据实际情况调整 ReservedCodeCacheSize 的大小,最后调整之后我们在jvm启动脚本中加上了如下两个参数:
-XX:ReservedCodeCacheSize=512m
-XX:-UseCodeCacheFlushing   (启用回收)
2) 编写预热代码
   编写WarmUpContextListener实现Spring的ApplicationContextAware接口 确保在Web容器启动完成前,调用需要预热的方法；
   WarmUpContextListener读取预先配置好的参数,包括要调用的目标方法、请求参数、执行次数和超时时间;
   新建线程池执行目标方法,执行N次触发JIT编译;
   执行完成,关闭预热线程池;




#### jcmd采集信息堆分析
```
#jcmd ${pid} VM.command_line | grep  'jvm_args'  
jvm_args: -Xms256m -Xmx512m -Xss256k -XX:MaxNewSize=64m -XX:MetaspaceSize=64m   

#jcmd ${pid} GC.heap_info | grep -v ${pid}  
   PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND                                                                                                            
167453 root      20   0 13.9g 826m  21m S  0.0  1.3   1:55.78 java                                                                                                               
 PSYoungGen      total 51200K, used 31462K [0x00000000fc000000, 0x0000000100000000, 0x0000000100000000)
  eden space 36864K, 64% used [0x00000000fc000000,0x00000000fd763fb8,0x00000000fe400000)
  from space 14336K, 52% used [0x00000000fe400000,0x00000000feb55b50,0x00000000ff200000)
  to   space 13824K, 0% used [0x00000000ff280000,0x00000000ff280000,0x0000000100000000)
 ParOldGen       total 380416K, used 282636K [0x00000000e0000000, 0x00000000f7380000, 0x00000000fc000000)
  object space 380416K, 74% used [0x00000000e0000000,0x00000000f14032d8,0x00000000f7380000)
 Metaspace       used 101056K, capacity 106722K, committed 107136K, reserved 1142784K
  class space    used 11727K, capacity 12861K, committed 12928K, reserved 1048576K
#jcmd ${pid} VM.native_memory summary  scale=MB
Total: reserved=2200MB, committed=983MB +65MB	#java进程总内存 总是会超过xmx
-                 Java Heap (reserved=512MB, committed=493MB)		#堆内 内存	xmx	
								-Xms256m -Xmx512m
                            (mmap: reserved=512MB, committed=493MB) 
 
-                     Class (reserved=1145MB +17MB, committed=132MB +18MB)		#Metaspace 元空间 加载类的元数据
                            (classes #18096)						#已加载18096个class
                            (malloc=27MB #37266) 
                            (mmap: reserved=1118MB, committed=105MB) 
-                    Thread (reserved=90MB, committed=90MB +2MB)			# thread占用内存 JVM本身也需要一些线程来执行其内部操作 如GC或即时编译  每个堆栈大约1 MB JVM在创建时将内存分配给线程 因此保留和提交的分配是相等的 
								-Xss1M: 设置线程栈的大小 1M(默认1M)
								-XX:ThreadStackSize=1M  主线程以 -Xss为准 其他线程以 ?-XX:ThreadStackSize 为准
                            (thread #232)							#目前有225个线程
                            (stack: reserved=89MB, committed=89MB)
                            (malloc=1MB #1386) 
                            (arena=1MB #447)
-                      Code (reserved=255MB, committed=70MB +41MB)		#Code Cache 代码缓冲区 
#JVM生成的native code存放的内存空间称之为Code Cache；JIT编译、JNI等都会编译代码到native code 其中JIT生成的native code占用了Code Cache的绝大部分空间  
#内部会先尝试解释执行Java字节码 方法调用或循环回边达到一定次数时 会触发即时编译 将Java字节码编译成本地机器码以提高执行效率
#只能以server模式启动时 分层编译默认开启
								-XX:InitialCodeCacheSize	初始值
								-XX:ReservedCodeCacheSize	最大值
								UseCodeCacheFlushing		启用gc回收
							(malloc=12MB #16539) 
                            (mmap: reserved=244MB, committed=58MB) 
-                        GC (reserved=46MB, committed=46MB)			#保留和已提交都接近46MB 致力于帮助 GC 平衡内存和性能 gc 算法(G1/ Serial GC)
                            (malloc=27MB #676) 
                            (mmap: reserved=19MB, committed=19MB) 
-                  Compiler (reserved=1MB, committed=1MB)			#jit compiler生成的code的时候

Symbol 运行时常量池 字符串string大量重复问题 存储每个 String 的单例 多次引用 称为 String Interning 
由于JVM只能内部编译时间字符串常量 手动调用字符串的 intern 方法来获取内部编译字符串 
JVM将实际存储的字符串存储在本机特殊固定大小并称为字符串表的哈希表中 也称为字符串池
可以通过-XX：StringTableSize调整标志配置表大小(即桶的数量) 
-                  Internal (reserved=123MB, committed=123MB +2MB)		#命令行解析、JVMTI等
                            (malloc=123MB #26485) 
-                    Symbol (reserved=23MB, committed=23MB +1MB)			#诸如string table 字符串表 及 constant pool 常量池 等 symbol(符号)
                            (malloc=20MB #213317) 
                            (arena=4MB #1)
 
-    Native Memory Tracking (reserved=5MB, committed=5MB +1MB)			#表示jcmd该功能自身?占用
                            (tracking overhead=5MB)
原生分配 堆外			
Metaspace(元空间)	VM使用名为Metaspace的专用区域 已加载类的元数据 而不是它们的实例	-XX：MetaspaceSize 和-XX：MaxMetaspaceSize
Native Byte Buffers(本地字节缓冲区) JVM通常有大量分配本机内存的嫌疑 另外也可以JNI调用的malloc和NIO中可直接调用的ByteBuffers 

used 已用, capacity 容量, committed 已分配, reserved 内存预分配 计划 
 
https://zhuanlan.zhihu.com/p/83009929	jvm中的本地内存介绍 nmt 分析 !!!

```











