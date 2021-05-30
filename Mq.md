
# 为什么用

削峰  并发 1000  缓存db

异步解耦  abcd 系统 动态增删 复制队列 1:n 问题 互不影响

模式 订阅 推 | 消费 拉  


# 对比

mq  |   量级  |   语言  |  高可用 | 丢消息 |  特点
-   |    -    |   -    |  - | -   
rabbitMq | 几万 | erlang | 主备 镜像队列 | 生产重试次数/发送者确认模式/持久化 | 语言快/社区活跃/可视化界面/吞吐量相对小/核心难以维护
rocketMq | 几十万 | java | 多主多备 | 持久化 | 性能双十一/文档好/高级特性:定时推送:延时推送:分布式事务 可靠
kafka | 大规模分布式 | | 多主多备 | 持久化 | zookeeper分布式消息订阅




# 架构

NameServer 注册中心 zk? 队列协调 无状态 多个相互独立 每个持有完整路由信息
org.apache.rocketmq.namesrv.routeinfo.RouteInfoManager 存储模型
        Broker 管理 存活列表(120s)心跳下线
        Topic 路由表  管理 TopicRouteData 
            Topic1 : Broker Master 1
            Topic2 : Broker Master 2
                        
                        
Broker 长连接(30s 心跳) 到 所有 NameServer 注册 Topic 高可用集群(BrokerName 分组) 1主(BrokerId=0) n备(slave 60s 同步 master)
        提供消息存取 Master(读写) Slave(读 仅当 master 压力大时被重定向到 slave)
        本地文件存储
            CommitLog   存储所有 Topic 消息  
                单文件 1G 
                文件命名 起始偏移量明明 20位 前补0
                TopicA-1-{msg}-offset
            ConsumeQueue    消费队列 CommitLog 中消息的索引 消费者从这里拿到消息地址去 CommitLog 获取 
                单文件 对应 Topic - Queue
                CommitLog 中的 物理偏移量(8 byte) + 消息长度(4 byte) + Tag hash(8 byte)
            IndexFile   索引文件 用于查找消息 console?
                通过 key 或 时间区间 查询
                文件名 时间命名 
                单文件 400M 2000w个索引 20 byte?
            存储优化
                零拷贝 mmap 内存映射(程序虚拟页面 映射 页缓存) 避免 内核空间 用户空间 拷贝 使用定长结构文件! 一次性映射
                文件预分配 预热 避免迟加载抖动(如 xms xmx) AllocateMappedFileService warmMappedFile 
                    mlock   将进程部分或全部的地址空间锁定在物理内存中 防止其被swap
                    madvise 系统标记文件即将使用 提前读几页
            持久化 内存 可靠性 取舍
                kill -9 Broker / shutdown / 断电 / 磁盘毁坏
                同步存储
                异步存储 丢消息
                副本双写
        Remoting 远程模块，处理客户请求
        Client Manager 管理客户端，维护订阅的主题
        Store Service 提供消息存储查询服务
        HA Serivce  主从同步高可用 slave 根据自己最大偏移量(CommitLog) 去 master 增量分页同步 
        Index Serivce，通过指定key 建立索引，便于查询
        
        
        
Producer 从 NameServer (120s)Addrs (10s)TopicRouteData 路由信息(TopicPublishInfo) 连接 Broker 存储
        MQClientInstance(producer 和 consmuer 公用 单例? ip-default)
        ->producerTable
        ->Topic TBW102
        ->remoteClient
        ->定时任务(同步 NameServer, 同步 Topic 路由表, 心跳 Broker 清理, 动态调整线程池?)
        ->拉取消息服务
        ->平衡服务
        ->心跳 Broker
        跟每一个(自己需要的?) Topic 1->n Broker 长连接(30s) 发送消息
            查找 Topic 路由(本地优先 迟同步?) 
                默认 TBW102(只负责根据 autoCreateTopicEnable 决定自动创建 目标 Topic?) 
                    只被受理到 同一台 Broker? 可能多台
                    自动创建 Topic 后 心跳 30s 延迟同步到 NameServer 
                        30s 内多次发送 未被广播同步 部分多个 Broker 创建同名 Topic 负载部分失效
                        30s 内单次发送 已被广播同步 后续所有都负载到该 单个 Broker 负载失效
            失败重试次数 retryTimesWhenSendAsyncFailed
                同步发送时 用不同 Broker 重试
                异步发送时 仅用同 Broker 重试? 
                    退步延时 故障延迟机制 sendLatencyFaultEnable
                    
                  

Consumer  从 NameServer 获取 Topic 路由信息 连接 Broker 
        跟每一个(自己需要的?) Topic->Broker 长连接? 接受消息
        广播模式    group 下多个订阅者 各自消费 自己的队列 Topic 1:n 独立偏移量 并行复制消费 就像是复制队列
        集群模式    group 下多个消费者 协作消费 同一个队列 Topic 1:1 共享偏移量 协作消费
        负载 定期同步 Topic 下的所有队列 关联 Topic 的订阅列表(消费者列表)
            TopicA-Queue1
            TopicA-Queue2
            每个 queue 队列均摊到已有的 消费者身上
        每个消费组 ConsumerGroup  都有一个 重试队列 Topic %RETRY%consumerGroup 及 延时配置
            重试任务放置于 延时队列中 delay 后移入 重试队列                  
            超过次数上限 后移入 死信队列 Topic %DLQ%ConsumerGroup
        全局顺序 
            消除所有并发 一个 Topic 仅 一个队列 仅一个 Producer 一个 Consumer 
            Producer 生产消息时 MessageQueueSelector 指定队列发送 
            Comsuer 消费时 MessageListenerOrderly 指定消费
            Broker 锁清单分配 mqLockTable 保证独享锁才能消费
        局部顺序
            单队列顺序 多队列之间并行
        Broker 宕机后 重平衡乱序!!
        ConsumerGroup 之间 每个Consumer 需要有相同的订阅? 心跳同步间隔 相互覆盖?
        优化
            提高并行程度 队列数 消费者数 提供单消费者性能 consumeThreadMax
            批处理消费 consumeMessageBatchMaxSize 
            丢弃次要消息 直接消费跳过

Topic 消息主题 建议一个应用一个 实质 一个主题多个队列 route? 收发前创建 
1:n
MessageQueue(kafka 分区 Partition) 消息并行入队 消费者并行消费队列
Tags 标签 同 Topic 中区分多个业务 灵活
Keys 主键 消息业务唯一标识 方便定位



# rocketMq env
wget https://mirrors.bfsu.edu.cn/apache/rocketmq/4.8.0/rocketmq-all-4.8.0-bin-release.zip
unzip rocketmq-all-4.8.0-bin-release.zip
cd rocketmq-all-4.8.0-bin-release
setx ROCKETMQ_HOME D:\cph\workspace\rocketmq-all-4.8.0-bin-release\rocketmq-all-4.8.0-bin-release   #环境变量

## 配置
./conf/
    Broker.conf #Broker配置
        BrokerClusterName = DefaultCluster
        BrokerName = Broker-a   #同名分组
        BrokerId = 0    #0主
        deleteWhen = 04
        fileReservedTime = 48
        BrokerRole = ASYNC_MASTER
        flushDiskType = ASYNC_FLUSH
    logback_*.xml   #各组件日志
        ${user.home}/logs/rocketmqlogs/Broker_default.log

## 启动
./bin/
    mqnamesrv   #启动 NameServer 依赖 环境变量 ROCKETMQ_HOME
    mqBroker -n 127.0.0.1:9876 autoCreateTopicEnable=true #启动 Broker 自动 Topic 异常 runBroker.cmd 修改 set "JAVA_OPT=%JAVA_OPT% -cp "%CLASSPATH%""

## 监控
wget https://github.com/apache/rocketmq-externals/blob/master/rocketmq-console
mvn clean package -Dmaven.test.skip=true
java -jar  
