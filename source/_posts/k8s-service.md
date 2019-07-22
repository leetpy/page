---
title: k8s学习之service
date: 2018-11-20 20:52:38
categories: PaaS
tags: [k8s]
---

由于重新调度等原因，pod 在 kubernetes 中的 IP 地址不是固定的，因此需要一个代理来确保使用 pod 的应用不需要知晓 pod 的真实 IP 地址。另一个原因是当使用 replication controller 创建了多个 pod 副本时，需要一个代理来为这些 pod 做负载均衡。

service 主要由一个 IP 地址和 label selector 构成。在创建之初，每个 service 便被分配了一个独一无二的 IP 地址，该 IP 地址与 service 的生命周期相同，且不再更改。

<!-- more -->

## service 工作原理

kubernetes 在每个节点都运行 kube-proxy 服务，它是实现 service 的主要组件。kube-proxy 有 userspace 和 iptables 两种工作模式。Kubernetes 在 1.2.0及以后的版本默认启用 iptables 模式，只有在系统 kernel 版本或者 iptables 版本不支持时，才使用 userspace 模式。

kubernetes 会给每个 service 分配一个固定 IP，这是一个虚拟IP（也称 ClusterIP）, 其范围是在集群初始化时 `--service-cluster-ip-range` 指定。

Service 是根据 Label Selector 来筛选 pod 的，实际上 service 是通过 endpoints 来衔接 pod 的。

```
$ kubectl get svc
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE
kubernetes   ClusterIP   192.168.2.1     <none>        443/TCP         7d18h
nginx        NodePort    192.168.2.39    <none>        80:3782/TCP     42h

$ kubectl get pods
nginx-deployment-d55b94fd-5thcb   1/1     Running   0          47h

$ kubectl get endpoints nginx -o yaml
apiVersion: v1
kind: Endpoints
metadata:
  creationTimestamp: 2018-11-28T08:03:17Z
  name: nginx
  namespace: default
  resourceVersion: "688700"
  selfLink: /api/v1/namespaces/default/endpoints/nginx
  uid: 1081f1a7-f2e4-11e8-858a-fa163e433fda
subsets:
- addresses:
  - ip: 192.168.3.15
    nodeName: master
    targetRef:
      kind: Pod
      name: nginx-deployment-d55b94fd-5thcb
      namespace: default
      resourceVersion: "663671"
      uid: 99782bc0-f2ba-11e8-858a-fa163e433fda
  - port: 80
    protocol: TCP
```

通过上面的例子可以看出 endpoints 里有服务对应 pod 的名字和 ip 信息。

### userspace 模式

对于每个 service, kube-proxy 都会在宿主机上随机监听一个端口与这个 service 对应起来，并非在宿主机上建立起 iptables 规则，将 service IP: service port 重定向到上述端口。

### iptables 模式

iptables 模式下 kube-proxy 只负责创建和维护 iptables 规则，其余工作均有内核完成。

## service 的自发现

一旦 service 被创建，该 service 的 IP 和 port 等信息都可以注入到 pod 中供他们使用。Kubernetes 支持两种 service 发现机制： 环境变量和 DNS.

### 环境变量方式

环境变量的注入只发生在 pod 创建时，且不会被自动更新。

### DNS 方式

#### DNS 缓存问题会导致如下两种不可靠情况

- DNS 函数库对 DNS TTL 支持不良问题由来已久。
- 即使应用程序和 DNS 服务器能够进行恰当的域名重解析操作，每个客户端频繁的域名重解析请求将给系统带来极大的负荷。

## service 外部路由

service 通常分为三种类型，分别为 ClusterIP, NodePort 和 Loadbalancer。其中 ClusterIP 是最基本的类型，在默认情况下只能在集群内部访问。

### NodePort

如果将 service 设置为 NodePort, 系统会从 `service-node-port-range` 范围中分配一个端口，默认随机分配，用户也可以自行指定。集群中每个工作节点都会打开该端口。

### Loadbalancer

Loadbalancer 类型的 service 并不是由 kubernetes 集群维护的，需要云服务提供商的支持。如何将外部 loadbalancer 接入的流量导到后端 pod，取决于具体云服务提供商的实现。

### external ip

## service 模板

```
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  selector:
    app: app
  type: NodePort
  ports:
  - protocol: TCP
    port: 5000
    nodePort: 80
```
