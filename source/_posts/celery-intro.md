---
title: celery 介绍
date: 2019-01-08 15:54:48
categories: mq
tags: [celery]
---

按照[官方说法](http://docs.celeryproject.org/en/latest/index.html) Celery 是一个简单，灵活可靠的分布式消息处理组件。至于这货性能如何，实际测试才知道。

<!-- more -->



## 创建 application

```python
from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y
```

这里的 broker 指定消息中间件的地址，rabbitmq 有多种写法：

- amqp://
- pyamqp://
-  librabbitmq://

如果安装了librabbitmq，则 amqp 使用 librabbitmq，否则使用 py-amqp。当然也可直接指定。librabbitmq是python封装的c库，效率更高。

## 启动Celery

```
celery -A tasks worker --loglevel=info
```

## 调用task

调用 task 有多种方式，分别是

- apply_async(args[, kwargs[, …]])

  发送消息，支持多种参数

- delay(*args, **kwargs)

  发送消息，不支持执行参数

- *calling* (`__call__`)



```python
>>> from tasks import add
>>> add.delay(4, 4)
```

调用`task`会返回一个`AsyncResult`对象，可以用来获取`task`是否完成，返回值，异常信息。

## 保存结果

如果需要`task`的状态，需要通过`backend`参数设置状态的存放地址，可以是 SQLAlchemy/DjangoORM, Memcached, Redis, RPC(RabbitMQ/AMQP)

### 完成状态

```python
result = add.delay(4, 4)
result.ready()
```

### 释放资源

每一个`AsyncResult`都需要显示调用`get()`,`forget()`来释放资源。



## celery 配置



