JAVA_HOME
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








