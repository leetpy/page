---
title: 常用 Docker 容器
date: 2019-03-07 15:35:43
categories: PaaS
tags: [docker]
---

主要记录开发过程中常用的容器创建命令。

<!-- more -->

## Rabbitmq

```
docker pull rabbitmq
docker run -d --hostname my-rabbit --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq
```

