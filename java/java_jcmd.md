

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
