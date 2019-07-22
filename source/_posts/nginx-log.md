---
title: nginx_log
date: 2019-01-08 14:51:31
tags:
---

nginx 日志需要自己进程转储。

<!-- more -->

## crontab 方式

```
mv access.log access.log.0
kill -USR1 `cat master.nginx.pid`
sleep 1
gzip access.log.0    # do something with access.log.0
```

[Log Rotation](https://www.nginx.com/resources/wiki/start/topics/examples/logrotation/)

## logrotate

在 /etc/logrotate.d/nginx 文件中添加：

```
/var/log/nginx/access/access.log { 
rotate 3
size=50G
missingok
notifempty
compress
delaycompress
sharedscripts
    postrotate
    /usr/sbin/nginx -s reload > /dev/null 2>&1
endscript
}
```
