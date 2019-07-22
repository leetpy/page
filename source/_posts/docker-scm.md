---
title: docker 三剑客
date: 2018-11-18 11:27:04
categories: PaaS
tags: [docker]
---

如果仅仅使用容器，在线上部署或者线下调试都需要耗费大量的时间。因此需要容器编排工具。例如 k8s, 但是k8s 比较重，安装管理复杂。docker 公司自己的swarm可以完成类似的工作。

<!-- more -->

docker-machine 用于创建 swam 节点，docker-compose 用户管理和部署。

# 创建服务
```
docker service create --replicas 2 --name hello app

# 通过 docker-compose 文件部署
docker stack deploy -c docker-compose.yml hello
```



# 更新
```
# 服务规模调整
docker service scale hello=3

# 镜像更新
docker service update --image nginx:latest hello
```



# 关闭服务
```
docker stack rm hello

#  删除服务
docker service rm hello
```

## 查看日志

```
docker service log hello --raw
```



# 离开集群
```
docker swarm leave --force
```



# 容器运行节点
docker stack ps


volume + bind mounts

# 设置节点状态

```
# 禁用
docker node update --availability drain work1
# 启用
docker node update --availability active worker1
```

# 查看 Token
```
docker swarm join-token worker/manager
```



# docker config 配置


docker network create --attachable --driver overlay oneta

```
version: "3"
networks:
  mynet:
    driver: overlay
    attachable: true
services:
```
