---
title: sklearn学习
date: 2019-05-29 14:41:04
tags:
---

Sklearn 笔记

<!-- more -->

## 安装

```bash
# pip 安装
pip install -U scikit-learn

# conda 安装
conda install scikit-learn
```



## 模型优化

## 分类器

### 随机森林

```python
from sklearn.ensemble import RandomForestClassifier

forest_clf = RandomForestClassifier(random_state=42)
forest_clf.fit(X_train, Y_train)
```

### 随机梯度

```python
from sklearn.linear_model import SGDClassifier

sgd_clf = SGDClassifier(random_state=42)
sgd_clf.fit(X_train, Y_train)
```



## 误差分析

### 混淆矩阵

```python
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix

# 使用交叉验证做出预测
y_train_pred = cross_val_predict(sgd_clf, X_train, y_train, cv=3)

# 获取混淆矩阵
conf_mx = confusion_matrix(Y_train, y_train_pred)
```

查看结果

```python
# 画图
import matplotlib.pyplot as plt
%matplotlib inline
plt.matshow(conf_mx, cmap=plt.cm.gray)
plt.show()
```



![](conf_mx.png)

有时候我们仅关注误差数据图像呈现。

```python
row_sums = conf_mx.sum(axis=1, keepdims=True)
norm_conf_mx = conf_mx / row_sums # 混淆矩阵每一列除以每种类型数量

np.fill_diagonal(norm_conf_mx, 0)  # 对角线用0填充
plt.matshow(norm_conf_mx, cmap=plt.cm.gray)
plt.show()
```

![](conf_mx_norm.png)



说明下，这里行代表实际类别，列代表预测的类别。颜色越亮说明分错概率越高。

### 准确率



### 召回率

