---
title: go io
date: 2018-08-22 12:33:48
categories: coding
tags: [go]
---

go 语言的标准库 io 包主要定义了常用的 io接口，具体如如下：

```go
// 读取接口
type Reader interface {
    Read(p []byte) (n int, err error)
}

// 写接口
type Writer interface {
    Write(p []byte) (n int, err error)
}

// 关闭读写
type Closer interface {
    Close() error
}

// 指定位置
type Seeker interface {
    Seek(offset int64, whence int) (int64, error)
}

// 指定位置读取
type ReaderAt interface {
    ReadAt(p []byte, off int64) (n int, err error)
}

// io 包还提供了一些组合接口
type ReadSeeker interface {
    Reader
    Seeker
}

type WriteCloser interface {
    Writer
    Closer
}

type WriteSeeker interface {
    Writer
    Seeker
}

type ReadWriter interface {
    Reader
    Writer
}

type ReadWriteCloser interface {
    Reader
    Writer
    Closer
}

type ReadWriteSeeker interface {
    Reader
    Writer
    Seeker
}
```

实现了上面接口的包如下：

- strings.Reader 实现了 io.Reader
- os.File 同时实现了 io.Reader 和 io.Writer
- net.conn 实现了 io.Reader, io.Writer, io.Close
- bufio.Reader/Writer 分别实现了io.Reader 和 io.Writer
- bytes.Buffer 同时实现了 io.Reader 和 io.Writer
- bytes.Reader 实现了io.Reader

ioutil

```go
// 读取所有数据
func ReadAll(r io.Reader) ([]byte, error)
```
