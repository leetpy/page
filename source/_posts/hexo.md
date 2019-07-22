---
title: hexo 配置
date: 2015-01-01 08:03:31
tags:
---

hexo 是一个静态博客生成框架，采用nodejs编写，可以把markdown文件编译成html，并提交到git服务器。

<!-- more -->

我采用的是Next主题，这里记录下用到的各种配置。

## 新建导航项

例如在导航栏加一个`reading`模块，效果如下：

![](navigation.jpg)

添加步骤：

1. 编辑`themes/next/_config.yml`文件，添加如下内容：
   ```
   menu:
   home: / || home
   reading: /reading || book
   tags: /tags/ || tags
   categories: /categories/ || th
   archives: /archives/ || archive
   ```
   `||`后面的单词指定要使用的图标，使用的是 [Font Awesome](https://fontawesome.com/icons) 库
2. 使用`hexo new page reading`新建一个page；
3. 编辑新建的page，定制自己的内容。

## 参考文献

[1] [https://theme-next.iissnan.com/getting-started.html](https://theme-next.iissnan.com/getting-started.html)

