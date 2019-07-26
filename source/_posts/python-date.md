---
title: python 时间日期
date: 2019-07-23 10:01:52
tags: [python]
---

时间和日期常常会在编程中使用。

<!-- more -->



## 字符串和日期转换

- `strptime` = "string parse time"
- `strftime` = "string format time"

```python
from datetime import datetime


# str 转 datetime
datetime_obj = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')


# datetime 转 str
date_str = datetime.strftime(datetime_obj, '%b %d %Y %I:%M%p')
```



## datetime 转 date

使用 `date` 函数转换

```python
from datetime import datetime

date_str = '2019.01.22'
index_date = datetime.strptime(date_str, "%Y.%m.%d").date()
```



## 常用函数

```python
# 获取当前日期
today = datetime.date.today()

# 昨天
yesterday = today + datetime.timedelta(-11)

# 明天
tomorrow = today + datetime.timedelta(1)
```



## 日期比较

```python
# date 类型比较
days = (today - tomorrow).days()


# datetime 类型比较
datetime1 > datetime2
```