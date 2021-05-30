JAVA_HOME
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








