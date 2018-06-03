---
title: go 结构体
date: 2018-04-18 12:14:02
categories: coding
tags: [go]
---

## 结构体声明

```go
type Employee struct {
    ID        int
    Name      string
    Address   string
    DoB       time.Time
    Position  string
    Salary    int
    ManagerID int
}
```

<!-- more -->

## 对象声明及初始化
```go
// 这个时候 dibert 已经初始化并可以使用了，所有值使用零值初始化
var dilbert Employee

// e1, e3 返回的是指针类型
e1 := new(Employee)
e2 := Employee{ID: 1, Name: "Lee"}
e3 := &Employee{1,  "lee"}

初始化的时候如果使用 `k: v` 可以打乱顺序，如果是 `v1, v2` 则必须和结构体声明顺序一致。
```
```go
// 指针类型
// 直接声明指针是没有初始化的
// 直接访问变量会报 panic: runtime error: invalid memory address or nil pointer dereference
var e4 *Employee
```

## 属性访问
```go
fmt.Println(dilbert.Name)
```

## 方法定义
go 的 struct 有点类似其它语言的 class, 但是又有些差异。

```go
func (e *Employee) Print() {
    fmt.Println(e.Name)
}

// 使用
dibert.Print()
```

## 匿名字段
声明一个结构体可以只写类型，不写 value，最常见的就是锁的使用，eg:

```go
type Node struct {
    sync.RWMutex
    Name string
}

// 使用匿名字段
var node Node
node.Lock // 调用的是 sync.RWMutex.Lock()
```

## 匿名结构体

```go
a := &struct{}{}
```