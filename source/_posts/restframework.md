---
title: rest framework 学习
date: 2019-06-04 11:18:50
tags: [django]
categories: python
---

rest framework 是 Django 的 api 框架。

<!-- more -->

## 参数获取

```python
# 获取 QueryString
query_params = self.request.query_params
only_latest = query_params.get('latest', False)  # get 返回的是 str 类型
```



## APIView

![](APIView.png)

