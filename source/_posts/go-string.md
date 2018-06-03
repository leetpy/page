---
title: go string 连接性能测试
date: 2018-04-28 12:33:48
categories: coding
tags: [go]
---

我们常使用字符串拼接，当比较小时，使用哪种方式都差不多，但是当拼接数比较大时，不同的方法效率会相差很大。

<!-- more -->

go 提供了如下几种方式连接字符串:

* strings.Join
* fmt.Sprintf
* +=
* strings.Builder (go 1.10 提供)

我们先简单测试下：

```go
package main

import (
    "fmt"
    "time"
    "strings"
)

func main() {
    var sz int  = 100000

    // += 方式
    t0 := time.Now()
    var s string
    for i := 0; i < sz; i ++ {
        s += "a"
    }
    d0 := time.Since(t0)
    fmt.Printf("time of [+=]: %v\n", d0)


    // strings.Join 方式
    t1 := time.Now()
    var s1 string
    for i := 0; i < sz; i++ {
        s1 = strings.Join([]string{s1, "a"}, "")
    }
    d1 := time.Since(t1)
    fmt.Printf("time of Join: %v\n", d1)

    // Sprintf
    t2 := time.Now()
    var s2 string
    for i := 0; i < sz; i++ {
        s2 = fmt.Sprintf("%s%s", s2, "a")
    }
    d2 :=  time.Since(t2)
    fmt.Printf("time of Sprintf: %v\n", d2)

    // string.Builder
    t3 := time.Now()
    var b strings.Builder
    for i :=0; i < sz; i++ {
        b.WriteString("a")
    }
    d3 := time.Since(t3)
    fmt.Printf("time of Builder: %v\n", d3)
}
```

结果:

```
time of [+=]: 1.1500289s
time of Join: 1.1507809s
time of Sprintf: 1.5668042s
time of Builder: 1.992ms
```

可以看出 +=, strings.Join, fmt.Sprintf 效率相差不大，但是 strings.Builder 的效率却高了 1000倍。为什么 strings.Builder 如此变态，我们看下实现：

* strings.Join 底层是用 += 和 copy 实现的，所以效率和 += 差不多
* strings.Builder 使用 []type 数组实现;


### strings.Builder 实现

Builder 可以用最小的内存拷贝来构建字符串。先看下 Builder 的简单实现:

```go
type Builder struct {
    addr *Builder // of receiver, to detect copies by value
    buf  []byte
}

func (b *Builder) copyCheck() {
    if b.addr == nil {
        // This hack works around a failing of Go's escape analysis
        // that was causing b to escape and be heap allocated.
        // See issue 23382.
        // TODO: once issue 7921 is fixed, this should be reverted to
        // just "b.addr = b".
        b.addr = (*Builder)(noescape(unsafe.Pointer(b)))
    } else if b.addr != b {
        panic("strings: illegal use of non-zero Builder copied by value")
    }
}

func (b *Builder) WriteString(s string) (int, error) {
    b.copyCheck()
    b.buf = append(b.buf, s...)
    return len(s), nil
}
```

可以看出 Builder 底层是用 []byte 实现的，每次添加字符串时，都是直接向数组最后插入值完成的，减少了不必要的内存拷贝，所以效率比较搞。