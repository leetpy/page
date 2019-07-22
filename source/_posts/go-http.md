---
title: go http 使用
date: 2018-04-20 12:16:38
categories: coding
tags: [go]
---

go 最强大的地方在于 goroutine 的实现，goroutine最适合的应用场景就是异步i/o。

<!-- more -->

先看一个简单的 tcp 连接:

## post json

当需要指定 Header 参数时，需要创建一个 http.Client 对象，然后用 http.Client 发起 http 请求。例如 POST 的时候指定 Heaer:

```go
data := map[string]string{}
jsonStr, err := json.Marshal(map[string][]string{"hosts": data})

client := &http.Client{}
req, err := http.NewRequest("POST", url, bytes.NewReader(jsonStr))

// set header
req.Header.Add("Content-Type", "application/json")
resp, err := client.Do(req)
```



## 读取结果和返回码

```go
resp, err := http.Get("http://example.com/")

// 获取返回码
fmt.Println(resp.StatusCode)

defer resp.Body.Close()
body, err := ioutil.ReadAll(resp.Body)
```



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



## Https 非安全访问

```go
tr := &http.Transport{
    TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
}
client := &http.Client{Transport: tr}
resp, err := client.Get(url)
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
