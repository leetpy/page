---
title: python 迭代器和生成器
date: 2018-04-23 12:08:45
categories: coding
tags: [python]
---

在 python 中我们常用 **for in** 来遍历 list, set, dict, str 等。
**for in** 的本质就干了两件事：

1. 调用 _\_iter__() 获取迭代器;
2. 调用 next() 直到 StopIteration 异常; (python3 中是 _\_next__())

<!-- more -->

## 迭代器

我们先了解几个概念：

* Iterable: 可迭代对象
* Iterator: 迭代器

我们先看看 Iterable 的实现
```python
from collections import Iterable

help(Iterable)

class Iterable(__builtin__.object)
 |  Methods defined here:
 |
 |  __iter__(self)
 |
 |  ----------------------------------------------------------------------
 |  Class methods defined here:
 |
 |  __subclasshook__(cls, C) from abc.ABCMeta
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  __dict__
 |      dictionary for instance variables (if defined)
 |
 |  __weakref__
 |      list of weak references to the object (if defined)
 |
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |
 |  __abstractmethods__ = frozenset(['__iter__'])
 |
 |  __metaclass__ = <class 'abc.ABCMeta'>
 |      Metaclass for defining Abstract Base Classes (ABCs).
 |
 |      Use this metaclass to create an ABC.  An ABC can be subclassed
 |      directly, and then acts as a mix-in class.  You can also register
 |      unrelated concrete classes (even built-in classes) and unrelated
 |      ABCs as 'virtual subclasses' -- these and their descendants will
```
再看看 Iterator 的实现
```python
from collections import Iterator

help(Iterator)

class Iterator(Iterable)
 |  Method resolution order:
 |      Iterator
 |      Iterable
 |      __builtin__.object
 |
 |  Methods defined here:
 |
 |  __iter__(self)
 |
 |  next(self)
 |      Return the next item from the iterator. When exhausted, raise StopIteration
 |
 |  ----------------------------------------------------------------------
 |  Class methods defined here:
 |
 |  __subclasshook__(cls, C) from abc.ABCMeta
 |
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |
 |  __abstractmethods__ = frozenset(['next'])
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors inherited from Iterable:
 |
 |  __dict__
 |      dictionary for instance variables (if defined)
 |
 |  __weakref__
 |      list of weak references to the object (if defined)
 |
 |  ----------------------------------------------------------------------
 |  Data and other attributes inherited from Iterable:
 |
 |  __metaclass__ = <class 'abc.ABCMeta'>
 |      Metaclass for defining Abstract Base Classes (ABCs).
 |
 |      Use this metaclass to create an ABC.  An ABC can be subclassed
 |      directly, and then acts as a mix-in class.  You can also register
 |      unrelated concrete classes (even built-in classes) and unrelated
 |      ABCs as 'virtual subclasses' -- these and their descendants will
 |      be considered subclasses of the registering ABC by the built-in
 |      issubclass() function, but the registering ABC won't show up in
 |      their MRO (Method Resolution Order) nor will method
 |      implementations defined by the registering ABC be callable (not
 |      even via super()).
```

从继承关系来看，所有的 Iterator(迭代器)都是 Iterable(可迭代对象)，
从实现角度看 Iterator 新增了 next() 方法。

### 判断是 Iterator 还是 Iterable

* 凡是可以 for 循环的，都是 Iterable;
* 凡是可以 next() 的，都是 Iterator;
* list, tuple, dict, str, set 都不是 Iterator，但是可以通过 _\_iter__() 返回一个 Iterator 对象

```python
from collections import Iterator, Iterable

isinstance([1,], Iterator)    // False
isinstance((1,), Iterator)    // False
isinstance({}, Iterator)      // False
isinstance("abc", Iterator)   // False
isinstance(set([]), Iterator) // False

isinstance([1,], Iterable)    // True
isinstance((1,), Iterable)    // True
isinstance({}, Iterable)      // True
isinstance("abc", Iterable)   // True
isinstance(set([]), Iterable) // True

dir([])                       // 没有 next() 方法
dir([].__iter__())            // 有 next() 方法
```

## 生成器

将完了迭代器，我们再说说生成器，这里引用廖雪峰博客里的介绍:

通过列表生成式，我们可以直接创建一个列表。但是，受到内存限制，列表容量肯定是有限的。
而且，创建一个包含100万个元素的列表，不仅占用很大的存储空间，
如果我们仅仅需要访问前面几个元素，那后面绝大多数元素占用的空间都白白浪费了。

所以，如果列表元素可以按照某种算法推算出来，那我们是否可以在循环的过程中不断推算出后续的元素呢？
这样就不必创建完整的list，从而节省大量的空间。在Python中，这种一边循环一边计算的机制，
称为生成器（Generator）。

生成器的创建很简单，可以通过推导列表创建：

```python
 g = (x * x for x in range(10))  // 使用 [] 返回的是 list, () 返回的是 generator
```

还有一种方式是通过 **yield** 关键字生成。


先看看生成器的实现:

```python
<genexpr> = class generator(object)
 |  Methods defined here:
 |
 |  __getattribute__(...)
 |      x.__getattribute__('name') <==> x.name
 |
 |  __iter__(...)
 |      x.__iter__() <==> iter(x)
 |
 |  __repr__(...)
 |      x.__repr__() <==> repr(x)
 |
 |  close(...)
 |      close() -> raise GeneratorExit inside generator.
 |
 |  next(...)
 |      x.next() -> the next value, or raise StopIteration
 |
 |  send(...)
 |      send(arg) -> send 'arg' into generator,
 |      return next yielded value or raise StopIteration.
 |
 |  throw(...)
 |      throw(typ[,val[,tb]]) -> raise exception in generator,
 |      return next yielded value or raise StopIteration.
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  gi_code
 |
 |  gi_frame
 |
 |  gi_running
```

可以发现生成器较迭代器多了 **send**, **throw** 等方法。

### send

这里重点介绍下 **send** 方法，我们知道在使用迭代器时，遇到 **yield** 关键字
会退出来，下一迭代时会继续执行。先看个例子：

```python
def MyGenerator():
    value = yield 1
    value = yield value

gen = MyGenerator()
print gen.next()         // print 1
print gen.next()         // print None
```

我们看看具体执行过程：

* 调用 next() 方法，走到 **yield 1** 退出，注意这个时候还没有走到 value 的 赋值操作(即: value = yield 1 只执行了右侧部分)
* 调用 next() 方法，继续上次的代码执行(即：value = yield 1 只执行了右侧的赋值部分)
* 由于 yield 并没有返回值，所以 value = None
* 返回 None, 并打印

修改下上面的例子：

```python
def MyGenerator():
    value = yield 1
    value = yield value

gen = MyGenerator()
print gen.next()         // print 1
print gen.send(2)        // print 2
```

send 方法是指定的是上一次被挂起的yield语句的返回值，这么说有点抽象，我们看执行过程：

* 调用 next() 方法，走到 **yield 1** 退出，注意这个时候还没有走到 value 的 赋值操作(即: value = yield 1 只执行了右侧部分)
* 调用 send(2) 方法，继续上次的代码执行(即：value = yield 1 只执行了右侧的赋值部分)
* value 使用 send 传的值，即： value = 2
* 返回 2, 并打印


## 协程

协程就是利用 **yield** 和生成器的 **send()** 方法实现的。