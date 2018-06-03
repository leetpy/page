---
title: ip 命令使用
date: 2017-04-30 17:10:50
categories: os
tags: [linux]
---

ip命令用来显示或操纵Linux主机的路由、网络设备、策略路由和隧道，是Linux下较新的功能强大的网络配置工具。

<!-- more -->

## tun/tap 设备

```shell
# create
sudo ip tuntap add dev tap-node-0i2 mode tap

# delete
sudo ip tuntap del dev tap-node-0i2 mode tap
```

## 创建 veth pair

```shell
ip link add veth_0 type veth peer name veth_0_peer
```

## Configure 802.1Q VLAN Tagging

```shell
$ # add
$ sudo ip link add link enp2s0 name enp2s0.100 type vlan id 100

$ # delete
$ sudo ip link del dev enp2s0.100

$ # show
$ ip -d link show enp2s0.100
19: enp2s0.100@enp2s0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether 50:7b:9d:1b:34:df brd ff:ff:ff:ff:ff:ff promiscuity 0
    vlan protocol 802.1Q id 100 <REORDER_HDR> addrgenmode eui64
```


## 网口操作

```shell
# 查看网口状态
ip addr show

# ifup
ip link set ens4 up

# 设置 ip 地址
ip addr add 10.5.1.23/24 dev enp132s0f0
```

## 路由

### 查看路由表

```console
$ ip route show
$ route -n
$ netstat -rn
```

### 根据 IP 查路由


```console
$ ip route get 10.0.2.14
10.0.2.14 dev eth0  src 10.0.2.15
```