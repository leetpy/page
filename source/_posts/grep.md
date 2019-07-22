---
title: grep
date: 2017-01-23 11:23:58
tags: [shell]
categories: shell
---

grep 主要用于查找过滤。

<!-- more -->

## OR

```
# using \|
grep 'pattern1\|pattern2' filename

# using -E
grep -E 'pattern1|pattern2' filename

# using egrep
egrep 'pattern1|pattern2' filename

# using -e
grep -e pattern1 -e pattern2 filename
```

## AND

```
grep -E 'pattern1.*pattern2' filename

grep -E 'pattern1.*pattern2|pattern2.*pattern1' filename

# Multiple grep
grep -E 'pattern1' filename | grep -E 'pattern2'
```

## NOT

```
# using -v
grep -v 'pattern1' filename
```
