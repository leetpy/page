---
title: go_http
date: 2018-04-20 12:16:38
categories: coding
tags: [go]
---

先看一个简单的 tcp 连接:

<!-- more -->

```go
// server
ln, err := net.Listen("tcp", ":8000")
if err != nil {}
for {
    conn, err := ln.Accept()
    if err != nil {
        continue
    }
    go handleConnection(conn)
}

// client
conn, err := net.Dial("tcp", ":8000")
if err != nil {}
status, err := bufio.NewReader(conn).ReadString('\n')
```


## http server
起一个 http server 有两种方式，分别是 `http.Server.ListenAndServe()` 和 `http.ListenAndServe()`,
两者在本质上是相同的。

监听 http
```go
// 创建 tcp 连接
s := &http.Server{}
s.ListenAndServe()

// 这里会创建一个 http.Server，然后调用 ListenAndServe
http.ListenAndServe(":80808", nil)
```