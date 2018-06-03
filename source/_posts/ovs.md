---
title: ovs 常用命令
date: 2016-05-01 16:54:27
categories: kvm
tags: [openstack]
---

## 连接网桥

例如现有两个 ovs 桥 br-1 和 br-2, 这两个桥上都挂有虚机， 如果不做处理，两个桥之间的虚机是不通的，如下图所示，要在 vm2 中访问 vm4, 需要把两个桥打通，或者有一个机器同时接到两个桥。

<!-- more -->

```
+----------------------+
|                      |
|  +-----+   +-----+   |
|  | vm1 |   | vm2 |   |
|  +-----+   +-----+   |
|      |       |       |
|    +----------+      |
|    |   br-1   |      |
|    +----------+      |
|          |           |
|          |           |
|    +----------+      |
|    |   br-2   |      |
|    +----------+      |
|      |       |       |
|  +-----+   +-----+   |
|  | vm4 |   | vm3 |   |
|  +-----+   +-----+   |
+----------------------+
```

创建 peer 口：

```shell
# ovs-vsctl add-br br-1
# ovs-vsctl add-br br-2

# ovs-vsctl add-port br-1 patch-br2 -- set Interface patch-br2 type=internal
# ovs-vsctl add-port br-2 patch-br1 -- set Interface patch-br1 type=internal

# ovs-vsctl set interface patch-br2 options:peer=patch-br1
# ovs-vsctl set interface patch-br1 options:peer=patch-br2

# ovs-vsctl show
c0618d27-6364-4e3f-9e38-f5c520575954
    Bridge "br-1"
        Port "br-1"
            Interface "br-1"
                type: internal
        Port "patch-br2"
            Interface "patch-br2"
                type: internal
                options: {peer="patch-br1"}
    Bridge "br-2"
        Port "br-2"
            Interface "br-2"
                type: internal
        Port "patch-br1"
            Interface "patch-br1"
                type: internal
                options: {peer="patch-br2"}
```

## VLAN 设置

```shell
# ovs-vsctl set port {port} vlan_mode=access
# ovs-vsctl set port {port} tag={segmentation_id}

# ovs-vsctl clear port {port} tag
# ovs-vsctl clear port {port} trunks
# ovs-vsctl clear port {port} vlan_mode
```

## 查看 interface 信息

```shell
# ovs-vsctl list interface tapaf2a9c21-d7
_uuid               : 7b32826b-dcf6-4e69-8b2c-0c8f7da946a0
admin_state         : down
bfd                 : {}
bfd_status          : {}
cfm_fault           : []
cfm_fault_status    : []
cfm_flap_count      : []
cfm_health          : []
cfm_mpid            : []
cfm_remote_mpids    : []
cfm_remote_opstate  : []
duplex              : []
error               : []
external_ids        : {attached-mac="fa:16:3e:d6:f8:96", iface-id="af2a9c21-d7c3-485b-a869-af701ab53ba2", iface-status=active}
ifindex             : 0
ingress_policing_burst: 0
ingress_policing_rate: 0
lacp_current        : []
link_resets         : 0
link_speed          : []
link_state          : down
lldp                : {}
mac                 : []
mac_in_use          : []
mtu                 : []
mtu_request         : []
name                : "tapaf2a9c21-d7"
ofport              : 6
ofport_request      : []
options             : {}
other_config        : {}
statistics          : {collisions=0, rx_bytes=488, rx_crc_err=0, rx_dropped=0, rx_errors=0, rx_frame_err=0, rx_over_err=0, rx_packets=5, tx_bytes=438, tx_dropped=0, tx_errors=0, tx_packets=5}
status              : {driver_name=openvswitch}
type                : internal
```

## 查看流表

```shell
# ovs-ofctl dump-flows brbm
```