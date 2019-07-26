---
title: alpine
date: 2019-07-25 11:41:22
tags: [docker]
---

alpine 是一个很小的linux 镜像，只有十几M大小，很适合部分服务。不过 alpine 的 c 库不是 glibc，所以依赖 glibc 时会有一些问题。

<!-- more -->

## 定制时区

```bash
apk add tzdata --no-cache
ls /usr/share/zoneinfo

echo "Europe/Brussels" >  /etc/timezone

# 或者通过环境变量方式设置
ENV TZ Asia/Shanghai
```

