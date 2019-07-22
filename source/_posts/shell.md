---
title: shell 常用技巧
date: 2018-04-22 11:10:11
categories: shell
tags: [shell]
---

记录些 shell 的使用技巧。

<!-- more -->

## 输出颜色控制

```
RED='\033[0;31m'
NC='\033[0m'
echo "${RED}hello world!${NC}"
```

