---
title: django ORM
date: 2019-07-04 14:59:39
tags: Django
categories: python
---

这里先记录下常用的操作，后续整理。

<!-- more -->

## 数据库更新

django 有一个 **django_migrations** 用于记录每一次更新。结构如下：

```
> desc django_migrations;
+---------+--------------+------+-----+---------+----------------+
| Field   | Type         | Null | Key | Default | Extra          |
+---------+--------------+------+-----+---------+----------------+
| id      | int(11)      | NO   | PRI | NULL    | auto_increment |
| app     | varchar(255) | NO   |     | NULL    |                |
| name    | varchar(255) | NO   |     | NULL    |                |
| applied | datetime(6)  | NO   |     | NULL    |                |
+---------+--------------+------+-----+---------+----------------+

> select * from django_migrations;
+----+------+--------------+----------------------------+
| id | app  | name         | applied                    |
+----+------+--------------+----------------------------+
|  1 | site | 0001_initial | 2019-05-16 10:56:28.313479 |
+----+------+--------------+----------------------------+
```

app 是表的名字， name 前面的序号是变更次数；

Migrations 步骤如下：

1.  修改数据库模型；
2. `pyhton manage.py makemigrations my_model`, 如果没有改动，使用 `—empty` 参数;
3. `python manage.py migrate`.

需要注意的是`migrate`并不是原子操作，也不会加锁，例如在k8s多个pod中执行，`django_migrations`表中可能会出现多条记录。

我们也可以在migartions 中执行脚本，例如：

```python
from django.db import migrations

def update_site(apps, schema_editor):
    Site = apps.get_model('site', 'Site')

    do something...

class Migration(migrations.Migration):

    dependencies = [
        ('site', '0001_auto_20190705_1027'),
    ]

    operations = [
        migrations.RunPython(update_site)
    ]
```



## 数据获取

```python
# 获取所有对象
Model.objects.all()

# 根据条件过滤
Model.objects.filter(name="lina")
```



### 特殊操作

- 大于: `__gt`
- 大于等于: `__gte`

- 小于: `__lt`
- 小于等于: `__lte`

- 包含: `__contains`

- 开头是: `__startswith`

- 结尾是: `__endswith`

- 其中之一: `__in`

- 范围： `__range`

```python
# in
Model.object.filter(name__in=["line", "Alice"])
```



## 创建

```python
# 更新或者创建
# 前面的是 filter, defaults 是更新
Industry.objects.update_or_create(
            industry_id=industry_id,
            name=industry_name[INDUSTRY_NAME_CHN],
            defaults={'name_en': industry_name[INDUSTRY_NAME_EN]},
)
```

