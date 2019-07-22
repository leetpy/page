---
title: celery任务超时控制
date: 2019-01-10 16:43:09
categories: mq
tags: [celery, python]
---

有时候celery任务的执行时间过长，如果没有有效控制可能导致mq消息大量堆积。celery 3.1以后的版本提供了超时机制。

<!-- more -->

# 超时设置

celery 提供了两个参数来控制task超时时间：

- task_time_limit: 在指定时间内没有完成，task会被kill，然后开始下一个task。
- task_soft_time_limit: 

## 在celery配置文件中使用

```python
time_limit = 30
soft_time_limit = 10
```

## 在装饰器中使用

```python
@app.task
def mytask(time_limit=30, soft_time_limit=10):
   do_your_job()
```

## 捕获异常

```
from celery.exceptions import SoftTimeLimitExceeded

@app.task
def mytask(soft_time_limit=10):
    try:
        return do_work()
    except SoftTimeLimitExceeded:
        cleanup_in_a_hurry()
```

这里实际测试有些情况下仍然捕获不到异常，会直接抛出，出现类似打印：

```
[2019-01-10 15:42:13,716: ERROR/ForkPoolWorker-11] Pool process <celery.concurrency.asynpool.Worker object at 0x107fddb90> error: SoftTimeLimitExceeded()
Traceback (most recent call last):
  File "/Library/Python/2.7/site-packages/billiard/pool.py", line 289, in __call__
    sys.exit(self.workloop(pid=pid))
  File "/Library/Python/2.7/site-packages/billiard/pool.py", line 347, in workloop
    req = wait_for_job()
  File "/Library/Python/2.7/site-packages/billiard/pool.py", line 447, in receive
    ready, req = _receive(1.0)
  File "/Library/Python/2.7/site-packages/billiard/pool.py", line 419, in _recv
    return True, loads(get_payload())
  File "/Library/Python/2.7/site-packages/billiard/queues.py", line 355, in get_payload
    return self._reader.recv_bytes()
  File "/Library/Python/2.7/site-packages/billiard/connection.py", line 245, in recv_bytes
    buf = self._recv_bytes(maxlength)
  File "/Library/Python/2.7/site-packages/billiard/connection.py", line 458, in _recv_bytes
    buf = self._recv(4)
  File "/Library/Python/2.7/site-packages/billiard/connection.py", line 424, in _recv
    chunk = read(handle, remaining)
  File "/Library/Python/2.7/site-packages/billiard/pool.py", line 227, in soft_timeout_sighandler
    raise SoftTimeLimitExceeded()
SoftTimeLimitExceeded: SoftTimeLimitExceeded()
```

# 参考文献

[1] [http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_time_limit](http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_time_limit)


