---
title: 谈谈 python 的并发
date: 2019-07-04 15:50:07
tags:
categories: python
---

并发无外乎进程，线程，协程三种方式。 Python 由于GIL锁的存在，多线程有些鸡雏，只能跑在一个核上。多进程各种语言差不多，创建开销比较大。

<!-- more -->

协程并不是操作系统内核提供的，它是用户态下实现的。协程主要用在网络上。参考许式伟的文档：大部分你看到的协程（纤程）库只是一个半吊子。它们都只实现了协程的创建和执行权的切换，缺了非常多的内容。包括：

- 协程的调度；
- 协程的同步、互斥与通讯；
- 协程的系统调用包装，尤其是网络 IO 请求的包装。

python3 的协程主要是 `asyncio` + `aiohttp` 实现，其中 `aiphttp`还存在不少坑。如果是 python2 可以用 `gevent` 或者 `eventlet` 之类的库。



## future 模块



```python
import random
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


def foo(i):
  # do something
  time.sleep(random.randint(1, 5))
	return i

# max_workers 指定线程池大小，如果不指定默认是 cpu *5
p = ThreadPoolExecutor(max_workers=4)

# 提交任务
tasks = [p.submit(foo, i) for i in range(10)]

# 获取返回结果, 这里的返回并不是按照提交顺序来的，而是谁先完成，谁先返回
for future in as_completed(tasks):
  print(future.result())
  
  
# 如果希望有序返回，使用 map
# 这里 result 是生成器，可以使用 list(result) 转换为 list 类型
result = p.map(foo, range(10))
```

