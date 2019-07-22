---
title: Docker 常用命令
date: 2017-05-08 10:32:49
categories: PaaS
tags: [Docker]
---

记录 docker 常用命令。
<!-- more -->

## image

- 查看创建信息

  ```shell
  $ sudo docker histroy <image_id>
  ```

## network


- 查看容器 IP

  ```shell
  $ docker inspect --format='{{.NetworkSettings.IPAddress}}' $CONTAINER_ID
  ```

## container


### 创建容器


- 启动参数:

  * -i: interactive 交互模式;
  * -t: tty;
  * -d: 后台运行;

  ```shell
  # tty 登录
  docker run -i -t <images_id> /bin/bash
  ```


- 进入后台运行的容器

  ```shell
  # 使用 name
  docker attach <name>

  # 使用 id
  docker attach <id>

  # 使用 name
  docker exec -it <name> /bin/bash

  # 使用 id
  docker exec -it <id> /bin/bash
  ```

  attach 和 exec 的区别在于 exec 执行 exit 时不会 stop 容器，而 attach 会 stop 容器。

- 重命名

  ```shell
  $ docker rename <current_name> <new_name>
  ```

- 删除容器

  ```shell
  # 删除所有
  docker rm -f $(docker ps -a -q)
  ```

## 文件拷贝

```shell
# host -> container
docker cp <host_path> <containerID>:<container_path>

# container -> host
docker cp <containerID>:<container_path> <host_path>
```

## 查看容器信息

```shell
$ sudo docker inspect tox
```
