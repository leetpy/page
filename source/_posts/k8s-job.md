---
title: k8s学习之job
date: 2018-11-21 09:56:45
categories: PaaS
tags: [k8s]
---

Kubernetes 有两种类型的 job, 分别是 `Job` 和 `CronJonb`。

- Job: 负责批量处理短暂的一次性任务，仅执行一次，并保证处理的一个或者多个Pod成功结束。
- CronJob: 负责定时任务，在指定的时间周期运行指定的任务。

<!-- more -->
