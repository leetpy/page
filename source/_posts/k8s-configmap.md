---
title: k8s学习之configmap
date: 2018-11-21 09:56:37
categories: PaaS
tags: [k8s]
---

很多生产环境中的应用程序较为复杂，可能需要多个 config 文件，命令行参数和环境变量的组合。并且这些配置信息应该从镜像中解耦出来，以保证镜像的可移植性以及配置信息不被泄漏。社区使用 ConfigMap 满足这一需求。

ConfigMap 包含了一系列键值对，用于存储被 pod 或者系统组件（如 controller 等）访问的信息。

<!-- more -->


## 创建 ConfigMap

### 通过文件创建

`from-file` 的参数可以是单个文件，也可以是目录，如果多个文件可以使用多个 `--from-file`参数。

```
kubectl create configmap <name> --from-file=<file>
```

## 使用 ConfigMap 中的信息

### 通过环境变量调用

假设已经创建了一个 ConfigMap, 信息如下：

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: special-config
  namespace: default
data:
  special.how: very
  special.type: charm
```

定义 pod

```
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
    - name: test-container
      image: busybox
      command: ["/bin/sh", "-c", "env"]
      env:
        - name: SPECIAL_LEVEL_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.how
        - name: SPECIAL_TYPE_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.type
  restartPolicy: Never
```

pod 启动后会输出所有的环境变量信息，其中包括:

```
SPECIAL_LEVEL_KEY=very
SPECIAL_TYPE_KEY=charm
```

### 设置命令行参数

configmap 还可以通过命令行注入，用户可以通过 `$(VAR_NAME)`方式调用：

```
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
    - name: test-container
      image: busybox
      command: ["/bin/sh", "-c", "echo $(SPECIAL_LEVEL_KEY) $(SPECIAL_TYPE_KEY)"]
      env:
        - name: SPECIAL_LEVEL_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.how
        - name: SPECIAL_TYPE_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.type
  restartPolicy: Never
```


### volume plugin

这是 configmap 最核心的用法，最基本的是通过文件名指定：

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-conf
data:
  nginx.conf: |
    user nginx;
    worker_processes  3;
    error_log  /var/log/nginx/error.log;
    events {
      worker_connections  10240;
    }
    http {
      log_format  main
              'remote_addr:$remote_addr\t'
              'time_local:$time_local\t'
              'method:$request_method\t'
              'uri:$request_uri\t'
              'host:$host\t'
              'status:$status\t'
              'bytes_sent:$body_bytes_sent\t'
              'referer:$http_referer\t'
              'useragent:$http_user_agent\t'
              'forwardedfor:$http_x_forwarded_for\t'
              'request_time:$request_time';
      access_log	/var/log/nginx/access.log main;
      server {
          listen       80;
          server_name  _;
          location / {
              root   html;
              index  index.html index.htm;
          }
      }
      include /etc/nginx/virtualhost/virtualhost.conf;
    }
    virtualhost.conf: |
      upstream app {
        server localhost:8080;
        keepalive 1024;
      }
      server {
        listen 80 default_server;
        root /usr/local/app;
        access_log /var/log/nginx/app.access_log main;
        error_log /var/log/nginx/app.error_log;
        location / {
          proxy_pass http://app/;
          proxy_http_version 1.1;
        }
      }
```

pod 定义：

```
apiVersion: apps/v1beta1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
        volumeMounts:
        - mountPath: /etc/nginx # mount nginx-conf volumn to /etc/nginx
          readOnly: true
          name: nginx-conf
      volumes:
      - name: nginx-conf
        configMap:
          name: nginx-conf # place ConfigMap `nginx-conf` on /etc/nginx
          items:
            - key: nginx.conf
              path: nginx.conf
            - key: virtualhost.conf
              path: virtualhost/virtualhost.conf # dig directory
```
