---
title: k8s学习之Replica Sets
date: 2018-11-21 09:56:06
categories: PaaS
tags: [k8s]
---

ReplicaSet 是下一代的Replication Controller.一个 ReplicaSet 和一个 Replication Controller 之间唯一的不同目前是对选择器的支持. ReplicaSet 支持最新的基于集合的选择器需求,这描述在标签用户指南然而一个Replication Controller 仅仅支持基于等号的选择器需求.

<!-- more -->

大部分的kubectl命令不仅支持Replication Controllers也支持ReplicaSets.一个例外是rolling-update命令. 如果你想功能上滚动升级,请考虑使用Deployments来替代.并且rolling-update是命令式的而Deployments则是陈述式的,所以我们推荐 通过rollout这个命令来使用Deployments.

当ReplicaSets能够被独立地使用的时候,今天它主要地被用在Deployments上作为精心策划pod创建,删除和升级的一个机制.当你使用Deployments的时候,你无需去 担心Deployments建立的ReplicaSets怎么去管理.Deployments 拥有和管理他们自己的ReplicaSets.

## 使用 ReplicaSet

一个ReplicaSet保证pod副本为一个指定的数目在给定的任何时间内.然而,一个Deployment是一个更高级别的概念来去管理ReplicaSets 和提供描述性的pods升级以及很多其他有用的特性.因此,我们推荐使用Deployments来替代直接使用ReplicaSets,除非你需要定制的更新编排 或者一点也不需要更新. 这个事实上意味着你可能从不需要操作ReplicaSet对象： 直接使用一个Deployment然后在声明部分定义你的应用.
