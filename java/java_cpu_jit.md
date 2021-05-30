
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
 

