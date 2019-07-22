---
title: rabbitmq
date: 2018-10-17 11:49:05
categories: mq
tags: [mq]
---


## Exchange

在生产者/消费者模型中，生产者是不会直接将消息发送到队列的，生产者只能把消息发送到 exchange 上。
<!-- more -->

先看一个简单的模型：

![](rabbitmq/exchanges.png)

exchange 的一端是生产者，另一端是队列，exchange 需要知道把消息发送到哪些队列。

有了 exchange 和队列之后，需要进行 bindings, 来告诉 exchange 把消息发送到指定队列。

![](rabbitmq/bindings.png)

```python
channel.queue_bind(exchange=exchange_name,
                   queue=queue_name,
                   routing_key='black')
```

在 bindings 的时候，可以指定 routing_key，来控制消息要发送的队列。

![](rabbitmq/direct-exchange.png)

当然多个队列可以有相同的 routing_key

![](rabbitmq/direct-exchange-multiple.png)

一个完整的生产者消费者模型如下：


![](rabbitmq/python-three-overall.png)


根据不同的规则，
rabbitmq 划分了四种 exchange：

- Direct
- Fanout: 把消息发送到所有绑定的队列；
- Topic:
- Headers
