---
title: 记一次elasticsearch 索引迁移
date: 2018-12-20 13:57:32
tags: [elasticsearch]
---

由于公司机房调整，需要将ES数据从一个集群迁移到另一集群。两个集群ES都是5.x版本，小版本存在差异，目标集群版本更低。数据由多个索引构成，每个索引大概1TB左右。

<!-- more -->

## 迁移方式

查阅官方资料，提供了三种ES数据迁移方式：[Migrating Your Elasticsearch Data](https://www.elastic.co/guide/en/cloud/current/ec-migrate-data.html)

从资料看，`Restore From a Snapshot` 方式最快，适合备份大量数据，但是这种方式必须要求是相同版本或者是从低版本到高版本迁移，不适用目前场景，所以先排除。再看`Reindex from a remote cluster`, 这种方式也比较灵活，但在使用时需要在目标集群配置 `reindex.remote.whitelist`,由于集群已经上线，且是公用的，所有不能修改配置，排除这种方式。最后只有`Index From the Source`方式可以选择。

这种方式说白了就是通过http请求来完成的，一种方式是把原始索引保存到文件，然后再目标ES集群通过文件恢复。另一种方式是直接从原始ES集群读取请求，然后POST到目标集群。由于这里数据量比较大，保存文件的方式不太现实，只能通过网络发送。

## 问题

如果采用`from + size`方式会有深度分页问题，这里采用`scroll + bulk`方式。

这里可以自己写脚本完成，可以通过 [esm](https://github.com/medcl/esm-abandoned)工具完成。需要注意的是自己写脚本需要有重试机制，否则每次失败都得重来。esm工具不支持后台运行，通过`nohup`和`&`操作并没有效果，如需后台运行，配合`screen`工具使用。

还有一点需要注意的是，如果是跨机房拷贝，工具最好在同一个机房运行，否则会有很大的延时。通过测试esm工具拷贝500GB的索引,配置5个进程大概在2h左右。这里建议不要同时拷贝太多的索引，以免集群扛不住挂掉。

如果失败了，只能重新开始，因为scroll每次的结果并不是一样的，没法从断电继续运行。
