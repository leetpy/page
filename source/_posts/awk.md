---
title: awk
date: 2017-01-23 11:27:30
tags: [shell]
categories: shell
---

awk 主要用于分词。

<!-- more -->

## 取匹配次数是三的倍数

```
cat $source_file | awk 'BEGIN{count=0} {i=1; while(i <= NF){ if(count%3==0){print $i}; count++; i++ }}'
```


## 取行数大于1的行的第一列

```
cat $source_file | awk '{ if(NF>1){print $1}}'
```

## 使用正则表达式

```
cat $source_file | awk '$1~/(x86_64$)|(noarch$)|(i686$)/{print $1}'
```

