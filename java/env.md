``JAVA_HOME
D:\workspace\jdk\jdk1.8.0_131
PATH
%JAVA_HOME%\bin;%JAVA_HOME%\jre\bin

export JAVA_HOME=/mnt/d/linux/jre1.8.0_202
export CLASSPATH=.:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export PATH=$JAVA_HOME/bin:$PATH

//������
javap -v ServiceImpl.class
javap -verbose ServiceImpl.class 
J2SE 8 = 52
J2SE 7 = 51
J2SE 6.0 = 50



//tomcat maven web jdk ��������
����  Project Facets 
Dynamic Web Module 3.0
Java 1.8
����  Java Compiler
jdk1.8
����  Java Build Path
jdk1.8
����  Deployment Assembly

����tomcat�ض�jdk eclipse 
����tomcat��ѡ��jdk

idea����tomcat web��Ŀ
artifacts
__:war exploded 
�����Ȳ���
���������Զ�copy�����ļ���Ŀ¼��
___:war
��������ģʽ,�����ȴ��war��,�ٲ���
debug configuration tabs
tomcat
add war artifacts
application context : url !!! /walker-web	#������
 
//node  vue
wget https://cdn.npm.taobao.org/dist/node/v12.10.0/node-v12.10.0-linux-x64.tar.xz
xz -d node-v12.10.0-linux-x64.tar.xz
tar -xvf node-v12.10.0-linux-x64.tar
mv node-v12.10.0-linux-x64/ nodejs
echo 'export PATH=$PATH:'`pwd -LP`'/nodejs/bin'  | sudo tee -a /etc/profile
source /etc/profile
���ô���Ͳֿ�
npm config delete registry
npm set https-proxy http://xxx
npm set proxy http://xxx
npm set registry https://registry.npm.taobao.org
npm config get registry
�˶� c/user/.npmrc
npm -v
npm install vue
��Ŀ��
npm install 
  
//eclipse ����jvm�ڴ� jvm �ڴ治��oom
Jdk edit ���Ӳ��� -Xmx1024M

//websphere was����
/washome/IBM/WebSphere/AppServer/bin/startManager.sh
/washome/IBM/WebSphere/AppServer/profiles/AppSrv02/bin/startNode.sh
/washome/IBM/WebSphere/AppServer/profiles/AppSrv02/bin/startServer.sh  server1 --servername

cd /washome/IBM/WebSphere/AppServer/bin  
./manageprofiles.sh -listProfiles	#1.�г����и�Ҫ�ļ�
./manageprofiles.sh -validateAndUpdateRegistry	#2.ˢ�¸�Ҫ�ļ�ע���
./manageprofiles.sh -deleteAll	#3.ɾ����Ҫ�ļ�
./manageprofiles.sh -delete -profileName AppSrv01	#�������� ��ֱ��ɾ������Ŀ¼ Ȼ�� ˢ�� Ȼ��ɾ��

#������Ҫ profile
./manageprofiles.sh -create -profileName  server1 -profilePath /washome/IBM/WebSphere/AppServer/profiles/server1
#��������
/washome/IBM/WebSphere/AppServer/profiles/Dmgr01/bin/startManager.sh
#�鿴�˿�SOAP	8879
grep SOAP /washome/IBM/WebSphere/AppServer/profiles/Dmgr01/logs/AboutThisProfile.txt
#�����ڵ� profile
/washome/IBM/WebSphere/AppServer/profiles/AppSrv01/bin/addNode.sh 127.0.0.1 8879
Error: The system cannot create a SOAP connector to connect to host 127.0.0.1 at port 8879
��ʱ ʹ������ hostname �õ�������
�л�����/washome/IBM/WebSphere/AppServer/profiles/AppSrv02/bin/����: 
ִ�� : ./syncNode.sh ������ 8879

#���� node
/washome/IBM/WebSphere/AppServer/profiles/AppSrv01/bin/startNode.sh 	#Error:  �˿ڱ�ռ�� 
#��̨��¼����
http://���ip��ַ:9060/washome/IBM/console/login.do
#�½�����server1	����Ӧ�÷��� ��ʼ��֤
cd /washome/IBM/WebSphere/AppServer/profiles/AppSrv01/bin/ ; ./startServer.sh server1 
���ʲ���:ע���ǽ 

2.�򵥻�����
����Ҫ���� _portdef_AppSvr.props�Լ�_portdef_DMgr.props�ļ�
ֱ�Ӵ���������Ҫ

���������Ҫ
./manageprofiles.sh
-create
-profileName  Dmgr01
-profilePath  /washome/IBM/WebSphere/AppServer/profiles/Dmgr01
-templatePath  /washome/IBM/WebSphere/AppServer/profileTemplates/dmgr/

����Ӧ�ø�Ҫ
./manageprofiles.sh
-create
-templatePath  /washome/IBM/WebSphere/AppServer/profileTemplates/default 
-profileName  AppSvr02
-profilePath   /washome/IBM/WebSphere/AppServer/profiles/AppSvr02  
����Ҳ�ǿ��Եġ�


##ibm/sun jdk 1.6 1.8 jvm����˵��
https://www.ibm.com/support/knowledgecenter/en/SSYKE2/earlier_releases/earlier_releases.html
���ø�ʽ
���ø�������
-X : �Ǳ�׼ѡ��
 -Xms22M
-XX: ���ȶ�ѡ�� 
 -XX:Xxxx=128M
 -XX:+UseCompressedOops	+���� ѹ��ָ��
 -XX:-UseCompressedOops	-ͣ�� ѹ��ָ��

�鿴jvm xxʵʱ����
jinfo -flag ThreadStackSize ${pid} 	#�鿴ָ��jvmֵ!
java -XX:+PrintFlagsFinal -version | grep Metaspac

####�� �ڴ� new old gc
```
������� ��λ 1[k|K|m|M|g|G]  
-XX:MaxDirectMemorySize=1G	�����ڴ�max 1.8
-XX:MetaspaceSize=64M	Ԫ�ռ�init/max 1.8 -XX:PermSize 1.7  maxĬ����û�����Ƶ�?
-XX:MaxMetaspaceSize=64M

-XX:InitialCodeCacheSize=64M	#Code Cache ���뻺���� init/max
-XX:ReservedCodeCacheSize=200M	
-XX:+UseCodeCacheFlushing	���û���

-XX:CodeCacheExpansionSize=1M	
-XX:CodeCacheMinimumFreeSpace=1M	
-XX:MinMetaspaceExpansion=1M
-XX:MaxMetaspaceExpansion=8M
-XX:CompressedClassSpaceSize=256M
 
-Xmn10M	new init=max �ɱ��ⶶ��
-XX:NewSize=2M	new init/max
-XX:MaxNewSize=2M 
-XX:NewRatio=2	new:old=2:1
-XX:SurvivorRatio=8	new eden:survivor=8:1
-XX:TargetSurvivorRatio=50	survivor��>50% -> old
-XX:MaxTenuringThreshold=15	survivor->old ���� Parallel=15 CMS=6

-Xms128M	����init def=Min(1/64,1G) init=max �ɱ��ⶶ�� OutOfMemoryError
-Xmx256M	����max def=Min(1/64,1G) 
-Xss1M	���߳�ջ	def=1M
-XX:ThreadStackSize=1M	�����߳�ջ

####gc
-XX:MaxGCPauseMillis=500	 gc ��ͣʱ�� max ms
-XX:+UseAdaptiveSizePolicy	����ӦGC����
-XX:+UseSerialGC	�ô��л�����
-XX:+UseParallelGC	�ò��������ռ��� Ĭ�Ͽ�������-old
-XX:+UseParallelOldGC
-XX:ParallelGCThreads=4	gc�߳��� def=cpu
-XX:+UseConcMarkSweepGC	��CMS�ռ���-old
-XX:+CMSClassUnloadingEnabled	������Ԫ���ݻ���
-XX:+UseG1GC	��G1������
-XX:G1HeapRegionSize=16m	G1-Region size(1M - 32M)
-XX:+DisableExplicitGC	����System.gc() 
-XX:+PrintGCDetails	GC��־
-XX:+PrintGCTimeStamps	GCʱ���
-XX:+PrintGCDateStamps	GC����
-XX:+PrintHeapAtGC	GCʱ-����Ϣ
-Xloggc:/home/gc.$$.log	GC��־λ��
-XX:+UseGCLogFileRotation	����������־��¼
-XX:NumberOfGCLogFiles=5	�������� f.0, f.1 ...
-XX:GCLogFileSize=8M	ÿ���ļ���С

####�ѿ���
-XX:+HeapDumpOnOutOfMemoryError	�����������¼����
-XX:HeapDumpPath=/home/oom.%t.log	�ѿ���λ��
-XX:+UseLargePages	
-XX:LargePageSizeInBytes=4m	��ҳ 2^*
```

 

##cpu���400%����
4c8g 4��cpu ��� 400% ÿ���߳̿��ܱ�ָ�ɸ�ĳ����cpu���� 
######����ԭ��:
���̵߳��� cpu����100% ��ѭ��(hashmap�̲߳���ȫ) ������ ����ƥ�� ���Ӽ���(6w ��map ��list ����)
Ƶ��gc(����cpu���� ë��)
���̵߳��������л�
######����˼·
����ҵ����־ ���ڴ������д���
�����ӿ����������仯(tcp/http io dubbo ���) �����쳣����
�Աȷ�����Ⱥģʽ��ÿ̨���� ͬʱ��� ����˷� ��̨����

��ߵ��߳�ջjavacore/jstack���ѿ���headdump/jmap��ȡ ��̨��ʱ��ڵ��ȡ�Աȱ仯
linuxϵͳ top H��ps H��nmon��tcp http��db���ӳء�redis����...���쳣�ֳ���Ϣ��ȡ

##### javacore ���� ��ע���javacore����Щ�߳�һֱ����
TITLE	Javacore ������ԭ�� ʱ���Լ��ļ���·��
    1TISIGINFO  Dump Event "user"   user: SIGQUIT �ź� gpf: ����һ�㱣���Դ�����ϵͳ���� systhrow: JVM �ڲ��׳����쳣 
GPINFO	GPF(һ�㱣���Դ���)��Ϣ
ENVINFO	ϵͳ����ʱ�Ļ����� JVM ����
MEMINFO	�ڴ�ʹ������������������
LOCKS	�û���������ϵͳ���������
CLASSES	�������Ϣ
THREADS	���� java �߳̿��� ״̬��Ϣ��ִ�ж�ջ
    ����(Deadlock)���ص㡿�໥��Դռ��
    ִ����(Runnable)���ص㡿����ʹ��cpu��Դ ���ps H��Ϣ��ռ���˶���cpu ����߳�ջ���ڸ���
    �ȴ���Դ(Waiting on condition)���ص㡿������ȡĳ��Դ ��Դ�� �̵߳ȴ�״̬
	����(Blocked)���ص��ע��������Դ�ȴ���ʱ ���̹߳�������ʶΪ����״̬
    �ȴ�����������Դ(Waiting on monitor)
    ��ͣ(Suspended)
    ����ȴ���(Object.wait())
    ֹͣ(Parked)



### �ѷ���
https://www.javadoop.com/post/metaspace
https://stuefe.de/posts/metaspace/what-is-metaspace/

### �����������
```
	#Netty	nio	-Dio.netty.noUnsafe=true	#Ĭ���㿽�� ByteBuf NioByteUnsafe
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
		Inflater��������ڴ�
		Deflater�ͷ��ڴ� 
		����close()�����������ͷ�  or ��������һ��GC

	Ϊʲôʹ�ö����ڴ�
	����ʹ�û���ʱ ���ػ���������ٵ� ��������������GCѹ��
	ʹ��Ӳ�̻��߷ֲ�ʽ�������Ӧʱ���Ƚϳ� ��ʱ�򡸶��⻺�桹����һ���ȽϺõ�ѡ��
	Ehcache ֧�ַ�������ڴ� ��֧��KV���� ���������GC	���㷺����Spring ֧�ֶ��� ���� ���� �ֲ�ʽ
	�����ڴ���Լ���GC��ѹ�� �Ӷ�����GC��ҵ���Ӱ�� 
	https://blog.csdn.net/lycyingO/article/details/80854669
```

   
####�������̶����ڴ� ��Ӱ����� ע��dump���ڴ���С ����
```
	pmap -x ${pid}  | sort -n -k3 -r  > maps.map 	#��������64M���ڴ���ԭ������Glibc
	# total kB        19108352  858872  840348
	#Address           Kbytes     RSS   Dirty Mode   Mapping
	#0x00000000fc000000  196608  196608  196608 rw---    [ anon ]
	#0x00000000e0000000  262144       0       0 -----    [ anon ]
	#
	#head -n 20 maps.map | sed -e "s/\([0-9a-f]\{8\}\)-\([0-9a-f]\{8\}\)/0x\1 0x\2/" | awk '{printf("\033[0;33m[%8d Page]\033[0m \033[0;35m[%8d KB]\033[0m %s\n", (0+$2 - $1)/4096, (0+$2 - $1)/1024, $0)}'
	#������������������ڴ�����	�ܶ�1000+
	grep rw-p /proc/${pid}/maps | sed -n 's/^\([0-9a-f]*\)-\([0-9a-f]*\) .*$/\1 \2/p' | head | while read start stop; do 
		gdb --batch --pid ${pid} -ex "dump memory ${pid}-$start-$stop.dump 0x$start 0x$stop"
	done
	#�ڴ����ݾ���
	strings -n 10 *dump # ���������ַ��͹����� �鿴�ڴ�
	#��� jcmd ${pid} help GC.heap_info �ɿ���java heap������ egen old metaspace��Ӧ�ĵ�ַ���� ��С���ܶ���
	#�������Ƕ���Ķ����Ĵ�����ַ�� ��� jcmd ${pid} VM.native_memory summary/detail �ɲ鿴java���̵�ȫ�ڴ�(����)��� �ɷ�������||meta�ľ���dump�ļ�
	#ͨ��������ַ����鿴 �ڴ��д�Ŵ���ʲô���� 

```




## jdk ����
#### jcmd --help
jdk1.7 ������ܹ����� �����ѡ��鿴Java���̡������߳���Ϣ��ִ��GC�������Խ��в�������
```
jcmd ${pid} help 
jcmd ${pid} VM.native_memory summary	
#The following commands are available:
	VM.native_memory  [summary | detail | baseline | summary.diff | detail.diff | shutdown] [scale= KB | MB | GB] 
		���� jvm ���� -XX:NativeMemoryTracking=detail	�鿴ԭ���ڴ���Ϣ nmt 	!!! ����5%-10%��������� 
		# summary: �����ڴ�ʹ�����.
		# detail: ��ϸ�ڴ�ʹ�����������summary��Ϣ֮�⻹�����������ڴ�ʹ�������
		# baseline: �����ڴ�ʹ�ÿ��գ�����ͺ������Ա�
		# summary.diff: ����һ��baseline��summary�Ա�
		# detail.diff: ����һ��baseline��detail�Ա�
		# shutdown: �ر�NMT

	ManagementAgent.stop
	ManagementAgent.start_local
	ManagementAgent.start
	VM.classloader_stats	�������
	GC.rotate_log 
	Thread.print	�߳̿���	jstack
	GC.class_stats	-XX:+UnlockDiagnosticVMOptions
	GC.class_histogram	��ֱ��ͼ�鿴���鿴ϵͳ����ͳ����Ϣ
	GC.heap_dump $file_jmap		��������Ϣ==jmap
	GC.finalizer_info
	GC.heap_info	gc��״̬ͳ��	jvm��metaspaceռ�����!!!
	GC.run_finalization
	GC.run	ִ��gc!!!
	VM.uptime
	VM.dynlibs	��̬���ӿ�?
	VM.flags	��ȡ��������
	VM.system_properties	��ȡϵͳProperties����
	VM.command_line	������������
	VM.version	������汾
	PerfCounter.print	��ȡ���������������
	help
```

##### jstat --help gc����
jstat -gc ${pid} [2000 2S��ʱ��ѯ] [4 ����4��]
```
	pid=$1
	[ -z "${pid}" ] &&  echo 'eg: ./make.sh ${pid} ' && exit 1 
	#https://docs.oracle.com/javase/7/docs/technotes/tools/share/jstat.html
	jstat -gc ${pid}  	#��������ͳ�� 
	jstat -gccapacity ${pid}  	#���������ڴ�ͳ�� 
	jstat -gccause ${pid}  	 
	jstat -gcnew ${pid}  	 
	jstat -gcnewcapacity ${pid}  	 
	jstat -gcold ${pid}  	#old
	jstat -gcoldcapacity ${pid}  	 
	#exe jstat -gcpermcapacity ${pid}  	#jdk7 ������ �ڴ�ͳ��
	jstat -gcmetacapacity ${pid}  	#JDK8 Ԫ�ռ� �ڴ�ͳ��
	jstat -gcutil ${pid}  	#�ܽ���������ͳ��	Summary of garbage collection statistics
	echo 'over' 

	#-gc Option Garbage-collected heap statistics 
	S0U=Survivor 0 Used/S0C=Survivor 0 Capacity	  ����/����	(KB).
	EC/EU=Eden	OC/OU=Old	PC/PU=Permanent	MC/MU=Mentaspace	
	YGC ����/YGCT ��ʱ	young gc 	
	FGC ����/FGCT ��ʱ 	full gc
	GCT=Total garbage collection time.	gc�ܺ�ʱ
	#-gccapacity Option 
	NGCMN/NGCMX/NGC	�����young min/max/now��ǰ����
	OGCMN/OGCMX/OGC	�����old  min/max/now��ǰ����  
	PGCMN/PGCMX/PGC	���ô�pert min/max/now��ǰ����   
	MCMN/MCMX/MC	Ԫ�ռ�meta min/max/now��ǰ����   
```

### pmap --help
���ƣ�
pmap - report memory map of a process(�鿴���̵��ڴ�ӳ����Ϣ)
�÷�
pmap [ -x | -d ] [ -q ] pids...
pmap -V
ѡ���
-x   extended       Show the extended format. ��ʾ��չ��ʽ
-d   device         Show the device format.   ��ʾ�豸��ʽ
-q   quiet          Do not display some header/footer lines. ����ʾͷβ��
-V   show version   Displays version of program. ��ʾ�汾
��չ��ʽ���豸��ʽ��
Address:  start address of map  ӳ����ʼ��ַ
Kbytes:  size of map in kilobytes  ӳ���С
RSS:  resident set size in kilobytes  פ������С
Dirty:  dirty pages (both shared and private) in kilobytes  ��ҳ��С
Mode:  permissions on map ӳ��Ȩ��: r=read, w=write, x=execute, s=shared, p=private (copy on write)  
Mapping:  file backing the map , or '[ anon ]' for allocated memory, or '[ stack ]' for the program stack.  ӳ��֧���ļ�,[anon]Ϊ�ѷ����ڴ� [stack]Ϊ�����ջ
Offset:  offset into the file  �ļ�ƫ��
Device:  device name (major:minor)  �豸��

### jmap --help 	headdump ��ȡ��ʽ
jmap [option] $pid
jmap [option] [server_id@]<remote server IP or hostname>
-<none> �����˼��˵��jmap���Բ����κ�option������Ϣ��ֻ��ָ��Java���̵Ľ��̺š���������£�jmap�������Linux����ϵͳ�����ڴ��������pmap������ԣ�����ڴ���������
-heap �鿴����JVM�ڴ�״̬   �Ĳ����������ǰָ��java���̵Ķ��ڴ��Ҫ��Ϣ
-clstats �ò�������ӡ����ǰjava�����У����ڵ�ÿ������������Լ�ͨ������������Ѿ���ɼ��صĸ�����Ϣ����������������������Ļ������Ѿ����ص��������������ĸ���������ȵ�(class�ļ�ͨ�����������ɵ����롢���ӡ���֤��ʼ���ȹ��̿���������������������о������ֳ���)��
finalizerinfo �ò����ɴ�ӡ���ȴ��ս�Ķ�����Ϣ����Java������Ƶ������Full GC��ʱ�򣬿���ͨ���������ȡ������Ų����ݡ�
-histo[:live] �鿴JVM���ж�����ϸռ����� �ò����������ÿ��class��ʵ����Ŀ���ڴ�ռ�á���ȫ������Ϣ�����live�Ӳ������Ϻ�,ֻͳ�ƻ�Ķ�������
-dump:<dump-options> ȡ�õ�ǰָ��java���̶��ڴ��и���classʵ������ϸ��Ϣ���������ָ���ļ���dump����������Ӳ����ֱ��ǡ�
liveֻ�������Ŀǰ�лʵ����class��Ϣ��
format�����ʽ��Ĭ��Ϊ��b��������ʹ�����׵ķ���������з�����
file�Ӳ�������ָ��������ļ���ע�⣬�������ļ��Ѿ����ڣ������ʹ��-F ������ǿ��ִ�����
eg:
jmap -dump:format=b,file=�ļ��� [pid]


#### ������������
//jhat -J-Xmx1024M $jmap_file #����html����headdump http://127.0.0.1:7000
jvisualvm $file_jmap	#ͼ�λ��������� jconsole��������? #�����߸��� java pid	Ҳ���Է���  dump �ļ� hprof
ha456.jar	ibm�����ѹ��� dump
jca457.jar	ibm���� javacore ����
gcviewer.jar  gc��������



#### cpu��߰��� jit
https://www.ezlippi.com/blog/2018/01/linux-high-load.html

#####JIT�ֲ����
1.8Ĭ�Ͽ��� 1.7 -XX:+TieredCompilation ���� ��ΪC1�ͻ��˱����C2����˱�����
���뼶��
0: ����ִ�� ����
1: ��C1�������
2: ���޵�C1�������,�������ܷ��� ���ݷ������ô����ͷ����ڲ�ѭ������������
3: ��ȫC1�������,�������ռ�������Ϣ֮�����ı���
4: C2�������,��������,�����ִ���ٶ����
jvm��������
```
    JIT���JVM�������    ֻ������serverģʽ
    ѡ��	Ĭ��ֵ	����
    CompileThreshold	1000 or 1500/10000	������ֵ,����ִ�ж��ٴκ���б���
    PrintCompilation	false	jit����ʱ�����־
    InitialCodeCacheSize	160K (varies)	��ʼcodecache��С
    ReservedCodeCacheSize	32M/48M	codecache���ֵ
    ExitOnFullCodeCache	false	codecache�����˳�jvm
    UseCodeCacheFlushing	false	codecache����ʱ���һ���codecache
    PrintFlagsFinal	false	��ӡ���е�jvmѡ��
    PrintCodeCache	false	jvm�˳�ʱ��ӡcodecache
    PrintCodeCacheOnCompilation	false	����ʱ��ӡcodecacheʹ�����
```
0�ʼ���ǽ���ִ��
1���������Ӧת��level3����
2����C1���г��Ⱥ�C1�����߳����������������ֵ
3����C2���г��ȿ���ת��C2����
4����C2���г��ȡ�C2�����߳�������level4������ֵ
��������ǳ�С,ûʲô�����Ż��Ŀռ� ֱ��תlevel1����
����ı�����ת��:0 -> 3 -> 4

#####�������
1)Ϊ�˱���CodeCache������JITֹͣ������� CodeCacheFlushing
��ȡ����ǰJIT��CodeCache��С  �ռ���ܲ����� ��һ������ CodeCache �ǲ�����յ� ���Ի��ۻ���Խ��Խ�� �Ƽ�����
//����64 bit������Ĭ����48m �� code cache �����˺� �����Ż��ͱ������� ��ʱ��ع鵽����ִ�� RT�����֪����õ���ȥ
jinfo -flag ReservedCodeCacheSize ${pid}
jinfo -flag InitialCodeCacheSize ${pid}
-XX:InitialCodeCacheSize=2 555 904
-XX:ReservedCodeCacheSize=251 658 240
����ʵ��������� ReservedCodeCacheSize �Ĵ�С,������֮��������jvm�����ű��м�����������������:
-XX:ReservedCodeCacheSize=512m
-XX:-UseCodeCacheFlushing   (���û���)
2) ��дԤ�ȴ���
   ��дWarmUpContextListenerʵ��Spring��ApplicationContextAware�ӿ� ȷ����Web�����������ǰ,������ҪԤ�ȵķ�����
   WarmUpContextListener��ȡԤ�����úõĲ���,����Ҫ���õ�Ŀ�귽�������������ִ�д����ͳ�ʱʱ��;
   �½��̳߳�ִ��Ŀ�귽��,ִ��N�δ���JIT����;
   ִ�����,�ر�Ԥ���̳߳�;




#### jcmd�ɼ���Ϣ�ѷ���
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
Total: reserved=2200MB, committed=983MB +65MB	#java�������ڴ� ���ǻᳬ��xmx
-                 Java Heap (reserved=512MB, committed=493MB)		#���� �ڴ�	xmx	
								-Xms256m -Xmx512m
                            (mmap: reserved=512MB, committed=493MB) 
 
-                     Class (reserved=1145MB +17MB, committed=132MB +18MB)		#Metaspace Ԫ�ռ� �������Ԫ����
                            (classes #18096)						#�Ѽ���18096��class
                            (malloc=27MB #37266) 
                            (mmap: reserved=1118MB, committed=105MB) 
-                    Thread (reserved=90MB, committed=90MB +2MB)			# threadռ���ڴ� JVM����Ҳ��ҪһЩ�߳���ִ�����ڲ����� ��GC��ʱ����  ÿ����ջ��Լ1 MB JVM�ڴ���ʱ���ڴ������߳� ��˱������ύ�ķ�������ȵ� 
								-Xss1M: �����߳�ջ�Ĵ�С 1M(Ĭ��1M)
								-XX:ThreadStackSize=1M  ���߳��� -XssΪ׼ �����߳��� ?-XX:ThreadStackSize Ϊ׼
                            (thread #232)							#Ŀǰ��225���߳�
                            (stack: reserved=89MB, committed=89MB)
                            (malloc=1MB #1386) 
                            (arena=1MB #447)
-                      Code (reserved=255MB, committed=70MB +41MB)		#Code Cache ���뻺���� 
#JVM���ɵ�native code��ŵ��ڴ�ռ��֮ΪCode Cache��JIT���롢JNI�ȶ��������뵽native code ����JIT���ɵ�native codeռ����Code Cache�ľ��󲿷ֿռ�  
#�ڲ����ȳ��Խ���ִ��Java�ֽ��� �������û�ѭ���رߴﵽһ������ʱ �ᴥ����ʱ���� ��Java�ֽ������ɱ��ػ����������ִ��Ч��
#ֻ����serverģʽ����ʱ �ֲ����Ĭ�Ͽ���
								-XX:InitialCodeCacheSize	��ʼֵ
								-XX:ReservedCodeCacheSize	���ֵ
								UseCodeCacheFlushing		����gc����
							(malloc=12MB #16539) 
                            (mmap: reserved=244MB, committed=58MB) 
-                        GC (reserved=46MB, committed=46MB)			#���������ύ���ӽ�46MB �����ڰ��� GC ƽ���ڴ������ gc �㷨(G1/ Serial GC)
                            (malloc=27MB #676) 
                            (mmap: reserved=19MB, committed=19MB) 
-                  Compiler (reserved=1MB, committed=1MB)			#jit compiler���ɵ�code��ʱ��

Symbol ����ʱ������ �ַ���string�����ظ����� �洢ÿ�� String �ĵ��� ������� ��Ϊ String Interning 
����JVMֻ���ڲ�����ʱ���ַ������� �ֶ������ַ����� intern ��������ȡ�ڲ������ַ��� 
JVM��ʵ�ʴ洢���ַ����洢�ڱ�������̶���С����Ϊ�ַ�����Ĺ�ϣ���� Ҳ��Ϊ�ַ�����
����ͨ��-XX��StringTableSize������־���ñ��С(��Ͱ������) 
-                  Internal (reserved=123MB, committed=123MB +2MB)		#�����н�����JVMTI��
                            (malloc=123MB #26485) 
-                    Symbol (reserved=23MB, committed=23MB +1MB)			#����string table �ַ����� �� constant pool ������ �� symbol(����)
                            (malloc=20MB #213317) 
                            (arena=4MB #1)
 
-    Native Memory Tracking (reserved=5MB, committed=5MB +1MB)			#��ʾjcmd�ù�������?ռ��
                            (tracking overhead=5MB)
ԭ������ ����			
Metaspace(Ԫ�ռ�)	VMʹ����ΪMetaspace��ר������ �Ѽ������Ԫ���� ���������ǵ�ʵ��	-XX��MetaspaceSize ��-XX��MaxMetaspaceSize
Native Byte Buffers(�����ֽڻ�����) JVMͨ���д������䱾���ڴ������ ����Ҳ����JNI���õ�malloc��NIO�п�ֱ�ӵ��õ�ByteBuffers 

used ����, capacity ����, committed �ѷ���, reserved �ڴ�Ԥ���� �ƻ� 
 
https://zhuanlan.zhihu.com/p/83009929	jvm�еı����ڴ���� nmt ���� !!!

```











