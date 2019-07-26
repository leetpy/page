---
title: vagrant 使用
date: 2019-07-24 14:33:09
tags:
---

Vagrant 是一款虚拟机管理工具，支持hyper, libvirt, virtual box, VMware_desktop, 可以和IDE 集成。使用vagrant的好处是可以在windows或者macos下编写代码，在linux下运行。

<!-- more -->

## 安装

[https://www.vagrantup.com/downloads.html](https://www.vagrantup.com/downloads.html) 下载对应安装包安装即可。



## 安装虚拟机

Vagrant 可以使用命令安装虚拟机，不过网络容易断，建议先下载镜像，再离线安装。

### 在线安装

虚拟机类型根据自己需求选择，这里选择的是 virtualbox

```bash
vagrant box add centos/7


This box can work with multiple providers! The providers that it
can work with are listed below. Please review the list and choose
the provider you will be working with.

1) hyperv
2) libvirt
3) virtualbox
4) vmware_desktop

Enter your choice: 3
```

### 离线安装

vagrant 网站提供了一些镜像下载，地址如下： [https://app.vagrantup.com/boxes/search](https://app.vagrantup.com/boxes/search), 这里以centos7为例：

1. 下载镜像 centos7 的镜像；
2. `vagrant box add —name 'centos/7' [box_path]`

## 虚拟机操作

```bash
# 生成虚拟机配置文件
vagrant init centos/7

# 启动虚拟机
vagrant up

# 登录虚拟机(默认账号密码都是vagrant, 可以 su 到 root)
vagrant ssh

# 关闭虚拟机
vagrant halt

# 销毁虚拟机
vagrant destroy
```

## pycharm 集成

Vagrant 只支持pycharm 专业版，不需要单独安装插件。



## vagrant 配置说明

```bash
# 配置同步目录
config.vm.synced_folder "./", "/vagrant_data/my_project", create: true

# 配置网络
config.vm.network "private_network", ip: "192.168.33.10"
```



## FAQ

1. vboxsf  mount 问题

   ```bash
   vagrant plugin install vagrant-vbguest
   vagrant destroy && vagrant up
   ```

   