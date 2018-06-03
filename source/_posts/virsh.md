---
title: virsh 常用命令
date: 2016-04-30 16:54:27
categories: kvm
tags: [openstack]
---

virsh 是 libvirt 的 cli 工具，通过调用 libvirt 接口来控制虚拟机。
<!-- more -->

## 常用命令

```shell
# 查看虚机列表
$ virsh list
Id    Name                           State
----------------------------------------------------
 3     dev_test                       running

# 查看网络
$ virsh net-list

# dumpxml
$ virsh dumpxml <id>

# 查看 vnc 端口号
$ virsh vncdisplay <id>

# 增加网卡
virsh attach-interface --domain vm1 --type bridge --source br1
```