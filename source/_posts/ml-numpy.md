---
title: numpy
date: 2019-05-05 11:26:16
tags:
---

numpy 主要用来做数据分析。

<!-- more -->

## 生成测试数据

```python
# 随机洗牌
import numpy as np

# permutation 会返回新的数组，shuffle 是在原来的数组上洗牌
shuffled_indices = np.random.permutation(len(data))
test_set_size = int(len(data) * test_ratio)
```

Scikit-learn 也提供了分割子集的方式：

```python
from sklearn.model_selection import train_test_split

train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)
```



分层采样



## 画图

### 散点图

```python
# housing 是 dataForm 对象
housing.plot(kind="scatter", x="longtitude", y="latitude")

# 通过设置 alpha 可以方面的看出密度
housing.plot(kind="scatter", x="longtitude", y="latitude", alpha=0.1)
```



