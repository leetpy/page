---
title: django 数据库读写分离
date: 2018-12-14 14:48:19
categories: python
tags: [django, database]
---

使用数据库读写分离可以提高网站的性能，吞吐率。

<!-- more -->

## 配置数据库
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'user',
        'HOST': '192.168.2.100',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': '123456',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'user',
        'HOST': '192.168.2.101',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': '123456',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
```

## 设置读写分离

### 手动设置

在使用数据库时，通过.using(db_name)来手动指定要使用的数据库.

```python
from django.shortcuts import HttpResponse
from . import models

def write(request):
    models.User.objects.using('default').create(username='lina', password='123')
    return HttpResponse('写入成功')

def read(request):
    obj = models.User.objects.filter(id=1).using('slave').first()
    return HttpResponse(obj.username)
```


### 自动设置

- 定义router

  ```python
  # 一主一从
  class Router(object):
      def db_for_read(self, model, **hint):
          return 'slave'
  
      def db_for_wirte(self, model, **hints):
          return 'default'

  # 一主多从
  class Router(object):
      def db_for_read(self, model, **hint):
          import random
          return random.choice(['slave1', 'slave2', 'slave3'])
  
      def db_for_wirte(self, model, **hints):
          return 'default'
  ```

- settings.py 加入DATABASE_ROUTERS设置
  ```python
  DATABASE_ROUTERS = ['myrouter.Router',]  
  ```


