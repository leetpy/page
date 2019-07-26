---
title: mysql 笔记
date: 2019-07-25 10:33:59
categories: database
tags: [mysql]
---

<!-- more -->

## host 授权

```sql
-- 通配符设置网段
grant all privileges on <db_name>.* to root@'10.249.149.%' identified by '<pwd>';


flush privileges；
```

