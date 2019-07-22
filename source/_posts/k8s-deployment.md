---
title: k8s学习之deployment
date: 2018-11-21 09:56:12
categories: PaaS
tags: [k8s]
---

Deployment 多用于为 pod 和 replia set 提供更新，并且可以方便地跟踪观察其所属的 replica set 或者 pod 数量以及状态的变化。

<!-- more -->

## Node 调度

有时候我们希望 pod 运行在指定的一个或者一批 node 上。可以通过 node 的名字或者 label 来完成。

## NodeName

Pod.spec.nodeName用于强制约束将Pod调度到指定的Node节点上，这里说是“调度”，但其实指定了nodeName的Pod会直接跳过Scheduler的调度逻辑，直接写入PodList列表，该匹配规则是强制匹配。

eg:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deploy
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: my-app
    spec:
      nodeName: master # 指定调度到master节点
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
```

### NodeSelector

- Pod.spec.nodeSelector是通过kubernetes的label-selector机制进行节点选择，由scheduler调度策略
- MatchNodeSelector进行label匹配，调度pod到目标节点，该匹配规则是强制约束。

#### 查看节点 label

```
kubectl get nodes --show-labels
```

#### 添加 label

```
kubectl label nodes <node_name> <key>=<value>

# eg:
kubectl label nodes master region=shanghai
```

#### pod 中指定 label

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deploy
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: my-app
    spec:
      nodeSelector:
        region: shanghai # 指定调度到上海的节点
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
```
