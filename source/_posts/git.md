---
title: git 常用命令
date: 2017-04-08 10:32:49
categories: tools
tags: [git]
---

这并不是一篇讲解 git 的文章，这里主要记录一些实用但是可能不常用的 git 命令，方便自己查阅。

<!-- more -->

## submodule
Git 子模块功能允许你将一个Git仓库当作另外一个Git仓库的子目录。这允许你克隆另外一个仓库到你的项目中并且保持你的提交相对独立。

```bash
# 添加子模块
git submodule add 仓库地址 路径

# 下载子模块
git submodule update --init --recursive
```

## orphan 使用

当我们需要创建一个全新的分支时，而又不希望继承任何其它分支，可以使用 --orphan 参数, eg:

```shell
git checkout --orphan dev
```

此时新创建的分支会有原始分支的代码，直接删除即可，然后添加我们新的代码。

## 查看配置信息
```bash
git config --global --list
```

## 设置信息
```bash
git config --global user.name "lee"
git config --global user.email "lee@test.com"

# 代理
git config --global http.proxy http://proxy.com:80
```

## 获取最后一次提交信息
```bash
# 最后一次所有信息
git log -1
# 最后一次commit id
git rev-parse HEAD
# 最后一个commit信息
git log -1 --pretty=%B
```

## cherry pick使用
有时候他们需要在多个分支上提交相同的代码，如果每一个都改一遍就太麻烦了。
这时候可以使用cherry pick，具体操作如下：


例如你现在 dev分支合入代码，并且已经提交。
1. git log 查看你提交的commit 号
```bash
commit 3e54a734e42bb8f9e2c32c193de741432f544d28
Author: lee <lee@test.com>
Date:   Fri Apr 29 14:13:16 2016 +0800

    614005245543 upgrade librados2* librbd1*
```
2. git checkout 其它分支
3. git cherry-pick 查询到的commit号（例如上面的3e54a734e42bb8f9e2c32c193de741432f544d28）
4. 这个时候你用git status 命令查看，切换的分支代码是已经add和commit的，由于不同的分支我们使用的EC单号不同，这个时候我们需要修改commit信息
5. 使用git commit --amend 这个时候git会自动调用vi打开你的commit信息，你编辑成新的就可以了。
6. 使用git push origin 远程分支名 提交代码