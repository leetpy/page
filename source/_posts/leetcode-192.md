---
title: Word Frequency
date: 2015-01-29 06:09:30
tags: [leetcode]
---

## 描述

Write a bash script to calculate the frequency of each word in a text file words.txt.

<!-- more -->

题目链接：[https://leetcode.com/problems/word-frequency/](https://leetcode.com/problems/word-frequency/)

## 分析

这题的思路是先用awk打印每个单词，再用sort排序，使相同的行在一起，再用uniq去除重复行，再根据次数排序，最后awk调换下打印顺序即可。

## 代码

```shell
awk '{i=1;while(i<=NF){print $i; i++}}' words.txt | \
	sort | uniq -c | sort -k1nr | awk '{print $2, $1}'
```