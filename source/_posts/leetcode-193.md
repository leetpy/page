---
title: Valid Phone Numbers
date: 2015-01-29 06:09:30
tags: [leetcode]
---

## 描述

Given a text file file.txt that contains list of phone numbers (one per line), write a one liner bash script to print all valid phone numbers.

<!-- more -->

题目链接：[https://leetcode.com/problems/valid-phone-numbers/](https://leetcode.com/problems/valid-phone-numbers/)

## 分析

编写匹配电话号码的正则表达式，过滤指定文件。使用 `grep` 即可。

## 代码

```shell
grep "^\(([0-9]\{3\}) \|[0-9]\{3\}-\)[0-9]\{3\}-[0-9]\{4\}$" file.txt
```

## 说明

- grep 在双引号(")中使用括号时需要加转意符；
- `[0-9]` 匹配数字；
- `{n}` 表示要匹配的次数；
- `(|)` 来表示或；