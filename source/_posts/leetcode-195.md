---
title: Tenth Line
date: 2015-01-29 06:09:30
tags: [leetcode]
---

## 描述

Given a text file file.txt, print just the 10th line of the file.

<!-- more -->

题目链接：[https://leetcode.com/problems/tenth-line/](https://leetcode.com/problems/tenth-line/)

## 分析

题目的意思很简单，就是输出文件的第十行，需要考虑文件行数少于10的情况。

## 代码

```shell
# Solution 1
cnt=0
while read line && [ $cnt -le 10 ]; do
  let 'cnt = cnt + 1'
  if [ $cnt -eq 10 ]; then
    echo $line
    exit 0
  fi
done < file.txt

# Solution 2
awk 'FNR == 10 {print }'  file.txt
# OR
awk 'NR == 10' file.txt

# Solution 3
sed -n 10p file.txt

# Solution 4
tail -n+10 file.txt|head -1
```