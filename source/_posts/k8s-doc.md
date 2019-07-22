---
title: k8s学习之帮助查看
date: 2018-11-20 17:58:20
categories: PaaS
tags: [k8s]
---

kubectl 提供了 explain 子命令来帮助我们查看 kubernetes 文档。

<!-- more -->


例如我们想查看 pod 有哪些参数：

```
$ kubectl explain pod
```

具体演示参考：

{% asciinema nr99mYPfYNY7UkSEVym3TBbav %}
