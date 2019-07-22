---
title: elasticsearch 笔记
date: 2019-07-16 10:17:28
tags: [elasticsearch]
---



记录下ES的常用操作，方便查看。

<!-- more -->



## painless

ES 使用的是 `painless` 语言。

## 更新数组

```json

```



## 索引操作

**删除单个索引**

```
DELETE /index_name
```



**删除所有索引**

```
# 两张选其一即可
DELETE /_all
DELETE /*
```

**索引复制**

```
POST /_reindex?wait_for_completion=false

{
  "source": {
    "index": "source_index"
  },
  "dest": {
    "index": "target_index"
  }
}
```



## 文档操作

**删除单个文档**

```
DELETE /index/_doc/id
```



**文档重建**

```
PUT /index/type/id

{
    "ip": "10.10.10.10",
    "name": "lina"
}
```



## 显示版本信息

ES文档都一个_version的计数器，用来记录文档的变更情况。需要注意的是ES并没有保存历史文档，_version只是一个计数器。需要查看version, 增加查询参数: `version=true`

## 查询

根据 `_id`查询

```
{
    "query": {
        "bool": {
            "must": [
                {
                    "terms": {
                        "_id": [
                            "12345678",
                            "12345679"
                        ]
                    }
                }
            ]
        }
    }
}
```

指定时间范围，这里的 `date` 是文档中的字段

```
{
    "query": {
        "range" : {
            "date" : {
                "gte" : "2019-05-01T00:00:00",
                "lte" : "2019-05-01T23:59:59"
            }
        }
    }
}
```

