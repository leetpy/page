---
title: 谈谈计算机的编码
date: 2019-04-03 17:40:47
tags:
---

我们经常听到 ASCII, 大致样子如下图所示。ASCII 由一个 7bit 组成，故只能表示2^7(128)个字符。由于 ASCII 能表示的字符数量有限，对很多语言支持无能为力。于是人们又搞了一套 unicode(又称万国码或者国际码，统一编码等)。 unicode 以4～6个十六进制数表示，前缀加`U+`

<!-- more -->

![USASCII_code_chart](USASCII_code_chart.png)

是不是认为全部使用unicode编码就万事大吉了，其实也不是，例如英文字符其实只需要7bit 即可表示，如果每个字符都使用2字节的原Unicode编码传输，其第一字节的8位始终为0。这就造成了比较大的浪费。于是人们又提出了Unicode转换格式（Unicode Transformation Format，简称为UTF） ，我们常听到的 utf-8 编码就是其中的一种。

UTF-8 使用1~6字节来编码，具体如下：

1. 128个ASCII 使用一个字节编码；

2. 拉丁，希腊，等用两个字节编码；

3. 少数语言（汉子）使用三字节编码；

4. 极少数辅助字符使用4～6字节编码；

   

这里举个例子说明下。例如我们想表示字母`A`, 用 ASCII 表示为 `100 0001`, 如果用 unicode 表示为 `U+0041`换成二进制是 `0000 0000 0000 0000 0000 0100 0000 0001`。而使用utf-8编码则为 `0100 0001`。

|      | ASCII    | Unicode                                 | UTF-8     |
| ---- | -------- | --------------------------------------- | --------- |
| A    | 100 0001 | 0000 0000 0000 0000 0000 0100 0000 0001 | 0100 0001 |



## 现代编码模型

在现代编码模型里要知道一个字符如何映射成计算机里比特，需要经过如下几个步骤。

1. 知道一个系统需要支持哪些字符，这些字符的集合被称为字符表（Character repertoire）
2. 给字符表里的抽象字符编上一个数字，也就是字符集合到一个整数集合的映射。这种映射称为编码字符集（CCS:Coded Character Set）,unicode是属于这一层的概念，跟计算机里的什么进制啊没有任何关系，它是完全数学的抽象的。
3. 将CCS里字符对应的整数转换成有限长度的比特值，便于以后计算机使用一定长度的二进制形式表示该整数。这个对应关系被称为字符编码表（CEF:Character Encoding Form）UTF-8, UTF-16都属于这层。
4. 对于CEF得到的比特值具体如何在计算机中进行存储，传输。因为存在大端小端的问题，这就会跟具体的操作系统相关了。这种解决方案称为字符编码方案（CES:Character Encoding Scheme）。



## 字符集

字符集从字面意思讲就是字符的集合，例如可以把数字0-9, 字母a-z, A-Z 一起组成一个字符集，可以把所有的汉子组成一个字符集。

## 码位

上面说的 ASCII 和 unicode 都是码位，也称编码的位置，英文 code point. 不同的字符集有不同的码位。码位其实就是一个字符和计算机二进制的映射。简单地讲就是定义了字符集里一个字符对应的二进制编码。



## 字符编码

字符编码主要是为了减少码位的长度，方便传输。把码位转换成字节序列的过程叫编码，把字节序列转换成码位的过程叫解码。

在 python2 中 `str` 是原始序列，而 unicode 则需要加 `u`表示，在 python3 中 `str` 就是 unicode 类型。eg:

```python
# python2
>>> country = u'中国'
>>> type(country)
<type 'unicode'>
>>> country
u'\u4e2d\u56fd'
>>> name = country.encode('utf-8')
>>> name
'\xe4\xb8\xad\xe5\x9b\xbd'
>>> print names
中国

>>> city = '苏州'
>>> type(city)
<type 'str'>
>>> city
'\xe8\x8b\x8f\xe5\xb7\x9e'
>>> city.decode('utf-8')
u'\u82cf\u5dde'


# python3
>>> country = '中国'
>>> type(country)
<class 'str'>
>>> country
'中国'
```



## 参考文献

[1] <https://en.wikipedia.org/wiki/ASCII>

[2] <https://en.wikipedia.org/wiki/Unicode>

[3] <https://en.wikipedia.org/wiki/Character_encoding>

[4] <https://en.wikipedia.org/wiki/Code_point>

[5] <http://blog.jobbole.com/39309/>