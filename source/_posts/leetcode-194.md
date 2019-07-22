---
title: Transpose File
date: 2015-01-29 06:09:30
tags: [leetcode]
---

## 描述

Given a text file file.txt, transpose its content.

You may assume that each row has the same number of columns and each field is separated by the ' ' character.

<!-- more -->

题目链接：[https://leetcode.com/problems/transpose-file/](https://leetcode.com/problems/transpose-file/)

## 分析

矩阵转制，用一个数组保存结果。

## 代码

```shell
awk '{\
    for(i=1;i<=NF;i++){\
        if(NR==1){\
            s[i]=$i\
        } else {\
            s[i]=s[i]" "$i;\
        }\
    }\
} \
END{\
    for(i=1;s[i]!="";i++) print s[i]\
}' file.txt
```