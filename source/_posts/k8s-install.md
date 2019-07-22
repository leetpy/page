---
title: kubeadm 安装 k8s
date: 2018-11-20 17:58:18
categories: PaaS
tags: [k8s]
---

本文介绍使用 kubeadm 安装 k8s 集群。建议不要用在生产环境。使用 kubeadm 安装，如果 master 节点挂了，是没有办法操作的。

安装版本：

- k8s: 1.12.2
- docker: 17.3.2

<!-- more -->

## 防火墙配置

```
# 关闭 firewalld
systemctl disable firewalld
systemctl stop firewalld

# 关闭 selinux
setenforce 0
sed -i "s/^SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config
```

## 内核参数配置

```
echo 1 > /proc/sys/net/bridge/bridge-nf-call-iptables
```

## hosts 配置

在 `/etc/hosts` 文件中配置集群的主机，例如：

```
192.168.1.2	master
192.168.1.3	node1
192.168.1.4	node2
```

## yum 源配置

### 添加 docker 源

CentOS 默认源的docker版本比较低，很多特性不支持，另外k8s对docker版本有要求，这里我们配置 `docker-ce` 源。

```
yum-config-manager --add-repo \
    http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```

### 添加 k8s 源

```
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
       http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
```

## 安装 docker

由于 k8s 对 docker 版本有要求，最新的 docker 版本不一定支持，这里安装指定版本。

```
# 查看可用版本
yum list docker-ce --showduplicates

yum install -y --setopt=obsoletes=0 \
   docker-ce-17.03.2.ce-1.el7.centos.x86_64 \
   docker-ce-selinux-17.03.2.ce-1.el7.centos.noarch

systemctl enable docker
systemctl start docker
```

## 安装 kubeadm 和 kubectl

```
yum install -y kubeadm kubectl

systemctl enable kubelet
```

## 下载 k8s 镜像

由于网络原因，kubeadm 需要的镜像无法下载，这里我们使用别人的代理下载。

### 查看所需 docker 镜像

```
# 这个命令仅使用 v1.10 以上
kubeadm config images list
```

添加 `pullimages.sh` 脚本, 并执行， 脚本内容如下：

```
#!/bin/bash
images=(
    kube-apiserver:v1.12.2
    kube-controller-manager:v1.12.2
    kube-scheduler:v1.12.2
    kube-proxy:v1.12.2
    pause:3.1
    etcd:3.2.24
    coredns:1.2.2
)
for imageName in ${images[@]} ; do
    docker pull anjia0532/google-containers.$imageName
    docker tag anjia0532/google-containers.$imageName k8s.gcr.io/$imageName
    docker rmi anjia0532/google-containers.$imageName
done
```

## 初始化集群

```
kubeadm init \
	  --kubernetes-version=v1.12.2 \
	  --pod-network-cidr=192.168.3.0/24 \
      --service-cidr=192.168.2.0/24
```

## master 参与调度

默认情况下集群不会调度 pod 到 master 节点，可以执行如下命令来控制

```
kubectl taint nodes --all node-role.kubernetes.io/master-
```

## 命令补全

```
yum install -y bash-completion
source /usr/share/bash-completion/bash_completion
source <(kubectl completion bash)
echo "source <(kubectl completion bash)" >> ~/.bashrc
```

## servcie 端口范围修改

k8s service 默认的端口范围是 30000-32767, 如果想修改端口范围，进行如下操作：

1. 修改 /etc/kubernetes/manifests/kube-apiserver.yaml，添加： `--service-node-port-range=80-32767`
2. systemctl restart kubelet.service



## 常见问题

### Dns loop detected

- 编辑 configmap
  ```
  kubectl -n kube-system edit configmap coredns
  ```
- 注释掉 loop
  ```
  apiVersion: v1
  data:
    Corefile: |
      .:53 {
          errors
          health
          kubernetes cluster.local in-addr.arpa ip6.arpa {
             pods insecure
             upstream
             fallthrough in-addr.arpa ip6.arpa
          }
          prometheus :9153
          proxy . /etc/resolv.conf
          cache 30
          #loop
          reload
          loadbalance
      }
  kind: ConfigMap
  metadata:
    creationTimestamp: 2018-11-20T03:08:28Z
    name: coredns
  ```

### token 过期

token 默认有效期是 24h, 如果 token 过期了，创建新 token 再加入集群：

```
kubeadm token create
```

### 其它节点 pod cidr 问题

- 查看节点是否设置了 pod cide
  `kubectl get nodes -o jsonpath='{.items[*].spec.podCIDR}'`
- 如果没有设置，设置节点的 pod CIDR
  `kubectl patch node <NODE_NAME> -p '{"spec":{"podCIDR":"<SUBNET>"}}'`

参考： [flannel  Troubleshooting](https://github.com/coreos/flannel/blob/master/Documentation/troubleshooting.md#kubernetes-specific)
