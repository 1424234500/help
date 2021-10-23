部署

docker run -d --hostname my-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3.8.0-beta.4-management



整合sb

https://www.cnblogs.com/sgh1023/p/11256273.html

Server：接收客户端的连接，实现AMQP实体服务。

Connection：连接，应用程序与Server的网络连接，TCP连接。

Channel：信道，消息读写等操作在信道中进行。客户端可以建立多个信道，每个信道代表一个会话任务。

Message：消息，应用程序和服务器之间传送的数据  

    Properties[privoty/level]， Body[json str]

    TTL min 每条消息发送时配置特定过期时间    队列初始化时配置默认的最大过期时间    0立即投递or过期

    消费者订阅队列时指定autoAck    true:发给消费者后自动确认    false:消费者主动上报确认    确认即从内存或者硬盘中删除(kafka的游标?)

    交换器持久化    声明队列时将durable参数设置为true。如果交换器不设置持久化，那么在RabbitMQ服务重启之后，相关的交换器元数据会丢失，不过消息不会丢失，只是不能将消息发送到这个交换器了。

    队列持久化    保证其本身的元数据不会因异常情况而丢失，但是不能保证内部所存储的消息不会丢失。要确保消息不会丢失，需要将其设置为持久化。队列的持久化可以通过在声明队列时将durable参数设置为true。 

当RabbitMQ服务重启之后，消息依然存在。如果只设置队列持久化或者消息持久化，重启之后消息都会消失



死信队列    异常记录器?

消息被拒 过期 最大长度 通过调用basic.reject或者basic.nack并且设置requeue=false。

进入死信交换器DLX  

设置死信队列的exchange和queue，然后进行绑定

Exchange：dlx.exchange   Queue：dlx.queue     RoutingKey：#  arguments.put（“x-dead-letter-exchange”,“dlx.exchange”）

延迟队列 

Virtual Host：虚拟主机 namespace? 逻辑隔离 有若干个Exchange和Queue 不同名

Binding：绑定，交换器和消息队列之间的虚拟连接，绑定中可以包含一个或者多个RoutingKey。

RoutingKey：路由键，生产者将消息发送给交换器 会发送一个RoutingKey 指定路由规则 交换器由此分发路由

Queue：消息队列，用来保存消息，供消费者消费。生产者声明并bind or 消费者声明并bind or 生产者消费者均声明并bind需一致性

Exchange：主题?交换器，接收消息 将消息规则路由到一个或者多个队列 如果路由不到，或者返回给生产者，或者直接丢弃, 拥有属性：ExchangeType 交换类型

生产者在发送消息时，都需要指定一个RoutingKey和Exchange(""为默认bind的direct交换)

rabbitmqadmin publish routing_key=test.route.1a  exchange=test.topic payload="sendmsg"

exchange的bind列表中按照ExchangeType 交换类型匹配queue

exchange            queue                RoutingKey

| test.exchange| test_queue_1        | test.route.* | 

| test.exchange| test_queue_2        | test.route1.2 | 

| test.exchange| test_queue_3        | test.route.# |

消费队列（bind队列用*#） 生产队列用 具体url 也可以用 *#

send exchangeName test.route.1a -> 1 3

send exchangeName test.route.1b.2a -> 3

send exchangeName test.route1.2 -> 2

    direct    = 1个exchange生产 1个queue消费

    topic      正则匹配路由 abc.*->abc.def  abc.#->abc.def.ghi

    fanout    广播所 RoutingKey参数无效? 转发快 性能好  1个exchange发布n个queue订阅

    headers    消息内容中的headers属性提取后按照bindingKey?进行匹配    性能差