---
title: python mock使用
date: 2018-12-20 22:02:28
tags: [python]
---

在测试中可以使用mock来模拟很多场景，而不需要去真正的执行代码。例如数据库查询，网络请求等。

<!-- more -->

## 使用场景

- patching 方法
- 记录方法调用情况

查看方法是否通过正确的参数调用

```python
class ProductionClass:
    def method(self):
        self.something(1, 2, 3)

    def something(self, a, b, c):
        pass

real = ProductionClass()
real.something = MagicMock()
real.method()
real.something.assert_called_once_with(1, 2, 3)
```

## Mock类型

Mock用来创建一个要模拟的对象。

```python
mock.Mock(spec=None, side_effect=None, return_value=DEFAULT,
          wraps=None, name=None, spec_set=None, unsafe=False, **kwargs)
```

- `spec:` 该参数代表要mock的对象，可以是list, strings, 类或者对象。如果传的是一个对象，会调用`dir()`,访问dir结果之外的属性都会报`AttributeError`.如果传的是对象，`__class__`会返回原来的类型。
- `return_value:` mock对象调用的返回值,默认是Mock对象。
- `side_effect:` 会覆盖`return_value`的返回值，一般用在抛异常或者动态改变返回值。

### 举例说明

- `return_value`

  ```python
  import mock
  
  class Production(ojbect):
      def print_hello(self):
          print 'hello world' 
  
  m1 = mock.Mock(spec=Production)
  m2 = mock.Mock(spec=Production, return_value=1)
  
  print m1()             # <Mock name='mock()' id='4443060048'>
  print m2()             # 1
  print type(m1())       # <class 'mock.mock.Mock'>
  print type(m2())       # <type 'int'>
  ```

- `side_effect`的值可以是函数，可迭代对象或者是异常。
  - 如果传参是函数，则会和mock使用相同的参数并调用。如果函数的返回值是`DEFAULT`怎使用正常的返回值（return_value指定的），否则返回函数的返回值。
  - 如果传参是可迭代对象，则每次调用使用迭代器的返回值。
  - 如果传参是异常，则调用会抛指定异常。
  
  设置异常:
  ```python
  >>> mock = Mock()
  >>> mock.side_effect = Exception('Boom!')
  >>> mock()
  Traceback (most recent call last):
    ...
  Exception: Boom!
  ```
  设置可迭代对象:
  ```python
  >>> mock = Mock()
  >>> mock.side_effect = [3, 2, 1]
  >>> mock(), mock(), mock()
  (3, 2, 1)
  ```
  设置函数，这里返回`DEFAULT`:
  ```python
  >>> mock = Mock(return_value=3)
  >>> def side_effect(*args, **kwargs):
  ...     return DEFAULT
  ...
  >>> mock.side_effect = side_effect
  >>> mock()
  3
  ```
  通过参数指定：
  ```python
  >>> side_effect = lambda value: value + 1
  >>> mock = Mock(side_effect=side_effect)
  >>> mock(3)
  4
  >>> mock(-8)
  -7
  ```
  设置为None：
  ```python
  >>> m = Mock(side_effect=KeyError, return_value=3)
  >>> m()
  Traceback (most recent call last):
   ...
  KeyError
  >>> m.side_effect = None
  >>> m()
  3
  ```

MagicMock是Mock的子类，它实现了大部分的`magic method`，而不需要你自己去配置。

## patch 装饰器

### mock.patch

```python
mock.patch(target, new=DEFAULT, spec=None, create=False, spec_set=None,
           autospec=None, new_callable=None, **kwargs)
```

patch() 可以作为函数装饰器，类装饰器或上下文管理器。

如果没有指定`new`参数，patch对象会使用`MagiMock`替换。
