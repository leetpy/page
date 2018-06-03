---
title: qemu 常用命令
date: 2016-04-30 16:54:27
categories: kvm
tags: [openstack]
---


## 镜像基本操作

```shell
# 创建镜像
$ qemu-img create -f <format> <filename> <size>

# 查看镜像信息
$ qemu-img info <filename>
```

<!-- more -->

## 格式转换

```shell
$ qemu-img convert -c -f <fmt> -O <out_fmt> -o <options> <fname> <out_fname>
```

## 扩容

```shell
$ qemu-img resize test.img +2G
```

## qemu-img 快照

```shell
# 创建快照
$ qemu-img snapshot -c first_snapshot /var/lib/test.img

# 查询快照
$ qemu-img snapshot -l /var/lib/test.img
Snapshot list:
ID        TAG                 VM SIZE                DATE       VM CLOCK
1         first_snapshot            0 2017-07-11 09:30:40   00:00:00.000

# 使用快照
$ qemu-img snapshot -a 1 /var/lib/test.img

# 删除快照
$ qemu-img snapshot -d 1 /var/lib/test.img
```

## qemu 镜像修改

有时候当我们的qemu 镜像系统挂了或者是没有密码时，我们可以挂载qemu镜像，然后对镜像进行修改和文件备份。操作步骤如下：

* 挂载qcow2
    ```shell
    modprobe nbd max_part=8
    qemu-nbd -c /dev/nbd0 vdisk01.img
    mount /dev/nbd0p1 /mnt/
    ```

* 挂载lvm分区 qcow2镜像

    ```shell
    vgscan
    vgchange -ay
    mount /dev/VolGroupName/LogVolName /mnt/
    ```

* 卸载qcow2

    ```shell
    umount /mnt/
    vgchange -an VolGroupName
    killall qemu-nbd
    ```