---
title: k8s学习之pod
date: 2018-11-20 20:52:00
categories: PaaS
tags: [k8s]
---

在 Kubernetes 中，能够被创建，调度和管理的最小单元是 pod, 而非单个容器。一个 pod 是由若干个 Docker 容器构成的容器组（pod意为豆荚）。

<!-- more -->

pod里的容器共享 network namespace, 并通过 volume 机制共享一部分存储。

pod里的容器共享如下资源：

- pod 是IP等网络资源分配的基本单位，这个IP及network namespace是由pod里的容器共享的。
- pod内的所有容器也共享volume。
- IPC namespace
- UTS namespace

## label

每个pod都有一个属性`labels` -- 一组键值对，例如：

```
"labels": {
    "key1": "value1",
    "key2": "value2"
}
```

### 相等查询

```
environment = production
tier != frontend
```

### 子集查询

```
environment in (production, qa)
tier notin (frontend, backend)
partition
```

## pod 模板

```
kind: Pod
metadata:
  name: busybox
  namespace: default
spec:
  containers:
  - name: busybox
    image: busybox
    command:
      - sleep
      - "36000"
    imagePullPolicy: IfNotPresent
  restartPolicy: Always
```

## 常用命令

### 根据 label 获取 pod

```
kubectl get pods -l name=nginx
```
