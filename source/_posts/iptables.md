---
title: iptables 介绍
date: 2018-06-29 14:30:10
categories: os
tags: [linux, iptables]
---

在Linux系统中，对于防火墙的实现一般分为包过滤防火墙，TCP-Wrapper即程序管控，代理服务器等几种方式。其中，iptables作为一种基于包过滤方式的防火墙工具，在实际中应用非常广泛，是非常重要的一个安全工具。真正实现防火墙功能的是 netfilter，它是一个 linux 内核模块，做实际的包过滤。实际上，除了 iptables 以外，还有很多类似的用户空间工具。

<!-- more -->
![](iptables-netfilter.png)

## iptable 介绍

![](Netfilter-packet-flow.svg)

![](iptables.png)

## iptables的“链”与“表”

netfilter 使用表（table）和 链（chain）来组织网络包的处理规则（rule）。它默认定义了以下表和链：

![](ipatbles_chain.png)

### filter表

主要用于对数据包进行过滤，根据具体的规则决定是否放行该数据包（如DROP、ACCEPT、REJECT、LOG）。filter 表对应的内核模块为iptable_filter，包含三个规则链：

- `INPUT`链：INPUT针对那些目的地是本地的包
- `FORWARD`链：FORWARD过滤所有不是本地产生的并且目的地不是本地(即本机只是负责转发)的包
- `OUTPUT链`：OUTPUT是用来过滤所有本地生成的包

### nat表

主要用于修改数据包的IP地址、端口号等信息（网络地址转换，如SNAT、DNAT、MASQUERADE、REDIRECT）。属于一个流的包(因为包
的大小限制导致数据可能会被分成多个数据包)只会经过这个表一次。如果第一个包被允许做NAT或Masqueraded，那么余下的包都会自动地被做相同的操作，也就是说，余下的包不会再通过这个表。表对应的内核模块为 iptable_nat，包含三个链：

- `PREROUTING`链：作用是在包刚刚到达防火墙时改变它的目的地址
- `OUTPUT`链：改变本地产生的包的目的地址
- `POSTROUTING`链：在包就要离开防火墙之前改变其源地址

### mangle表

主要用于修改数据包的TOS（Type Of Service，服务类型）、TTL（Time To Live，生存周期）指以及为数据包设置Mark标记，以实现Qos(Quality Of Service，服务质量)调整以及策略路由等应用，由于需要相应的路由设备支持，因此应用并不广泛。包含五个规则链——PREROUTING，POSTROUTING，INPUT，OUTPUT，FORWARD。

### raw表

是自1.2.9以后版本的iptables新增的表，主要用于决定数据包是否被状态跟踪机制处理。在匹配数据包时，raw表的规则要优先于其他表。包含两条规则链——OUTPUT、PREROUTING

iptables中数据包和4种被跟踪连接的4种不同状态：

- `NEW`：该包想要开始一个连接（重新连接或将连接重定向）
- `RELATED`：该包是属于某个已经建立的连接所建立的新连接。例如：FTP的数据传输连接就是控制连接所 - - - RELATED出来的连接。--icmp-type 0 ( ping 应答) 就是--icmp-type 8 (ping 请求)所RELATED出来的。
- `ESTABLISHED`：只要发送并接到应答，一个数据连接从NEW变为ESTABLISHED,而且该状态会继续匹配这个连接的后续数据包。
- `INVALID`：数据包不能被识别属于哪个连接或没有任何状态比如内存溢出，收到不知属于哪个连接的ICMP错误信息，一般应该DROP这个状态的任何数据。

### 防火墙处理数据包的方式（规则）：

- `ACCEPT`：允许数据包通过
- `DROP`：直接丢弃数据包，不给任何回应信息
- `REJECT`：拒绝数据包通过，必要时会给数据发送端一个响应的信息。

- `SNAT`：源地址转换。在进入路由层面的route之后，出本地的网络栈之前，改写源地址，目标地址不变，并在本机建立NAT表项，当数据返回时，根据NAT表将目的地址数据改写为数据发送出去时候的源地址，并发送给主机。解决内网用户用同一个公网地址上网的问题。
MASQUERADE，是SNAT的一种特殊形式，适用于像adsl这种临时会变的ip上

- `DNAT`:目标地址转换。和SNAT相反，IP包经过route之前，重新修改目标地址，源地址不变，在本机建立NAT表项，当数据返回时，根据NAT表将源地址修改为数据发送过来时的目标地址，并发给远程主机。可以隐藏后端服务器的真实地址。（感谢网友提出之前这个地方与SNAT写反了）
- `REDIRECT`：是DNAT的一种特殊形式，将网络包转发到本地host上（不管IP头部指定的目标地址是啥），方便在本机做端口转发。

- `LOG`：在/var/log/messages文件中记录日志信息，然后将数据包传递给下一条规则。

除去最后一个LOG，前3条规则匹配数据包后，该数据包不会再往下继续匹配了，所以编写的规则顺序极其关键。


## iptables编写规则

命令格式：

![](iptables-cli.png)

- `[-t 表名]`：该规则所操作的哪个表，可以使用filter、nat等，如果没有指定则默认为filter
- `-A`：新增一条规则，到该规则链列表的最后一行
- `-I`：插入一条规则，原本该位置上的规则会往后顺序移动，没有指定编号则为1
- `-D`：从规则链中删除一条规则，要么输入完整的规则，或者指定规则编号加以删除
- `-R`：替换某条规则，规则替换不会改变顺序，而且必须指定编号。
- `-P`：设置某条规则链的默认动作
- `-nL`：-L、-n，查看当前运行的防火墙规则列表
- `chain名`：指定规则表的哪个链，如INPUT、OUPUT、FORWARD、PREROUTING等
- `[规则编号]`：插入、删除、替换规则时用，--line-numbers显示号码
- `[-i|o 网卡名称]`：i是指定数据包从哪块网卡进入，o是指定数据包从哪块网卡输出
- `[-p 协议类型]`：可以指定规则应用的协议，包含tcp、udp和icmp等
- `[-s 源IP地址]`：源主机的IP地址或子网地址
- `[--sport 源端口号]`：数据包的IP的源端口号
- `[-d目标IP地址]`：目标主机的IP地址或子网地址
- `[--dport目标端口号]`：数据包的IP的目标端口号
- `-m`：extend matches，这个选项用于提供更多的匹配参数，如：
    - -m state –state ESTABLISHED,RELATED
    - -m tcp –dport 22
    - -m multiport –dports 80,8080
    - -m icmp –icmp-type 8
- `<-j 动作>`：处理数据包的动作，包括ACCEPT、DROP、REJECT等

具体实例请参考 iptables常用实例备查。
