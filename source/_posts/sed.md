---
title: sed
date: 2017-01-23 11:19:09
tags: [shell]
categories: shell
---

sed 主要用于替换匹配等操作。

<!-- more -->

## 匹配空格

```
sed -i 's/key[[:space:]]*=[[:space:]]*value/key=new_value/' file
```

## 行范围

```
# 匹配行到最后一行
sed -n '/Installed Packages/,$'p file.txt

# 前两行
sed -n '1,2'p file.txt

# 去掉第一行
sed -n '2,$'p file.txt
```

## 模糊匹配

```
# 替换 *.iso 为 test.iso, 注意引号的区别
sed -i "s/\\(.*\\)iso/test.iso/" vm.xml
sed -i 's/\(.*\)iso/test.iso/' vm.xml
```
