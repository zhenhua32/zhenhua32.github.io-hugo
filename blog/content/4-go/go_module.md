+++
title = "使用 Go 模块"
date =  2019-08-24T13:08:05+08:00
weight = 1
+++

## 简介

Go 终于要有自己的模块了, 以前只有包, 而模块是包的上一级.

以下是阅读官网上的两篇文章的总结.

- https://blog.golang.org/using-go-modules
- https://blog.golang.org/migrating-to-go-modules

## 使用 Go 模块

一个模块是存储在文件树中的一系列的 Go 包的集合, 根目录有一个 `go.mod` 文件.

`go.mod` 文件定义了模块的 _module path_, 这也是用于根目录的导入路径.
还定义了 _dependency requirements_, 这是构建需要的外部模块.

## 模块的常见操作

### 创建一个新的模块

在 `$GOPATH/src` 之外, 创建一个目录, 并添加文件 `hello.go`:

```go
package hello

func Hello() string {
    return "Hello, world."
}
```

添加一个测试文件, `hello_test.go`:

```go
package hello

import "testing"

func TestHello(t *testing.T) {
    want := "Hello, world."
    if got := Hello(); got != want {
        t.Errorf("Hello() = %q, want %q", got, want)
    }
}
```

到这里, 该目录包含一个包, 但还不是一个模块, 因为还没有 `go.mod` 文件.

如果在该目录下运行 `go test`:

```bash
$ go test
PASS
ok      _/home/gopher/hello    0.020s
$
```

最后一行总结了所有的包的测试. 因为我们在 `$GOPATH` 目录外, 也在任何模块之外,
所有 `go` 命令对当前目录不知道任何导入路径, 这会制造一个假的基于当前目录名的模块:
`_/home/gopher/hello`.

现在, 使用 `go mod init` 将该目录初始化为一个模块, 并重新运行 `go test`.

```bash
$ go mod init example.com/hello
go: creating new go.mod: module example.com/hello
$ go test
PASS
ok      example.com/hello    0.020s
$
```

这样, 就创建一个 Go 模块, 并运行了测试. 注意到, 模块名字已经变成了 `example.com/hello`.

`go mod init` 命令产生了一个 `go.mod` 的文件.

```bash
$ cat go.mod
module example.com/hello

go 1.12
$
```

`go.mod` 文件只出现在模块的根目录.
在子目录中的包的导入路径为 模块路径 加上 子目录 路径.
如果我们创建了一个叫做 `world` 的子目录, 这个包会自动被识别为
模块 `example.com/hello`的一部分, 它的导入路径为 `example.com/hello/world`.

### 添加一个依赖

Go 模块的主要动力是提高代码被其他开发者作为依赖的体验.

更新 `hello.go`, 导入 `rsc.io/quote` 并使用它来实现 Hello 函数.

```go
package hello

import "rsc.io/quote"

func Hello() string {
    return quote.Hello()
}
```

重新运行测试:

```bash
$ go test
go: finding rsc.io/quote v1.5.2
go: downloading rsc.io/quote v1.5.2
go: extracting rsc.io/quote v1.5.2
go: finding rsc.io/sampler v1.3.0
go: finding golang.org/x/text v0.0.0-20170915032832-14c0d48ead0c
go: downloading rsc.io/sampler v1.3.0
go: extracting rsc.io/sampler v1.3.0
go: downloading golang.org/x/text v0.0.0-20170915032832-14c0d48ead0c
go: extracting golang.org/x/text v0.0.0-20170915032832-14c0d48ead0c
PASS
ok      example.com/hello    0.023s
$
```

`go` 命令使用在 `go.mod` 中列出的特定依赖来解析导入.
当它遇到任何不在 `go.mod` 中的 `import` 导入的包时,
go 命名会自动查找包含这个包的模块, 并将它添加到 `go.mod` 文件中,
并使用最新的版本号.

```bash
$ cat go.mod
module example.com/hello

go 1.12

require rsc.io/quote v1.5.2
$
```

再次运行 `go test` 不会重复上面的过程, 因为 `go.mod` 是最新的,
而且下载的模块已经缓存在本地了, 在 `$GOPATH/pkg/mod`目录下.

添加一个直接的依赖通常会带来一些间接的依赖, 命令 `go list -m all`
列出当前模块和它的所有依赖.

```bash
$ go list -m all
example.com/hello
golang.org/x/text v0.0.0-20170915032832-14c0d48ead0c
rsc.io/quote v1.5.2
rsc.io/sampler v1.3.0
$
```

通常第一行是主模块, 下面都是它的依赖, 按模块路径排序.

`golang.org/x/text` 的版本是 `v0.0.0-20170915032832-14c0d48ead0c`,
这是一个 _伪版本(pseudo-version)_, 这是 go 命令对没有标签的提交的版本语法.

除了 `go.mod` 之外, go 命令还维护了一个叫做 `go.sum` 的文件,
包含每一个特定版本的模块的内容的加密哈希.

```bash
$ cat go.sum
golang.org/x/text v0.0.0-20170915032832-14c0d48ead0c h1:qgOY6WgZO...
golang.org/x/text v0.0.0-20170915032832-14c0d48ead0c/go.mod h1:Nq...
rsc.io/quote v1.5.2 h1:w5fcysjrx7yqtD/aO+QwRjYZOKnaM9Uh2b40tElTs3...
rsc.io/quote v1.5.2/go.mod h1:LzX7hefJvL54yjefDEDHNONDjII0t9xZLPX...
rsc.io/sampler v1.3.0 h1:7uVkIFmeBqHfdjD+gZwtXXI+RODJ2Wc4O7MPEh/Q...
rsc.io/sampler v1.3.0/go.mod h1:T1hPZKmBbMNahiBKFy5HrXp6adAjACjK9...
$
```

go 命令通过使用 `go.sum` 文件来未来的下载和第一次下载一样, 有相同的 bit.
保证你的项目依赖的模块不会发生意外的变化. 这两个文件 `go.mod` 和 `go.sum`
都应该保存在版本控制之中.

### 升级依赖

使用 Go 模块, 版本号使用语义版本标签. 一个语义版本有三个部分: 主版本, 次版本,
补丁版本.

因为前面通过 `go list -m all` 看到 `golang.org/x/text` 使用了一个未标记的版本,
让我们升级到最新的版本, 并测试一切都正常.

```bash
$ go get golang.org/x/text
go: finding golang.org/x/text v0.3.0
go: downloading golang.org/x/text v0.3.0
go: extracting golang.org/x/text v0.3.0
$ go test
PASS
ok      example.com/hello    0.013s
$
```

一切正常, 重新看看 `go list -m al` 的输出, 以及 `go.mod` 文件.

```bash
$ go list -m all
example.com/hello
golang.org/x/text v0.3.0
rsc.io/quote v1.5.2
rsc.io/sampler v1.3.0
$ cat go.mod
module example.com/hello

go 1.12

require (
    golang.org/x/text v0.3.0 // indirect
    rsc.io/quote v1.5.2
)
$
```

`golang.org/x/text` 包已经升级到最新版本了. `go.mod` 文件也更新了.
`indirect` 注释表示这不是一个直接被该模块使用的依赖, 而是间接依赖.

让我们试图更新 `rsc.io/sampler` 的次要版本, 使用相同的方式, 并运行测试:

```bash
$ go get rsc.io/sampler
go: finding rsc.io/sampler v1.99.99
go: downloading rsc.io/sampler v1.99.99
go: extracting rsc.io/sampler v1.99.99
$ go test
--- FAIL: TestHello (0.00s)
    hello_test.go:8: Hello() = "99 bottles of beer on the wall, 99 bottles of beer, ...", want "Hello, world."
FAIL
exit status 1
FAIL    example.com/hello    0.014s
$
```

测试失败了, 这个版本不兼容我们的用例. 看一看这个模块有哪些版本:

```bash
$ go list -m -versions rsc.io/sampler
rsc.io/sampler v1.0.0 v1.2.0 v1.2.1 v1.3.0 v1.3.1 v1.99.99
$
```

换个版本试试, 我们已经使用 `1.3.0` 了, 或许 `1.3.1` 可以兼容.

```go
$ go get rsc.io/sampler@v1.3.1
go: finding rsc.io/sampler v1.3.1
go: downloading rsc.io/sampler v1.3.1
go: extracting rsc.io/sampler v1.3.1
$ go test
PASS
ok      example.com/hello    0.022s
$
```

通过在 `go get` 中指明版本号, 默认是 `@latest`.

### 添加对新的主版本的依赖

添加一个新的功能, 修改 `hello.go` 文件:

```go
package hello

import (
    "rsc.io/quote"
    quoteV3 "rsc.io/quote/v3"
)

func Hello() string {
    return quote.Hello()
}

func Proverb() string {
    return quoteV3.Concurrency()
}
```

然后添加一个新的测试, 在 `hello_test.go` 中:

```go
func TestProverb(t *testing.T) {
    want := "Concurrency is not parallelism."
    if got := Proverb(); got != want {
        t.Errorf("Proverb() = %q, want %q", got, want)
    }
}
```

然后, 重新测试:

```bash
$ go test
go: finding rsc.io/quote/v3 v3.1.0
go: downloading rsc.io/quote/v3 v3.1.0
go: extracting rsc.io/quote/v3 v3.1.0
PASS
ok      example.com/hello    0.024s
$
```

注意到, 我们的模块现在依赖 `rsc.io/quote` 和 `rsc.io/quote/v3`.

```bash
$ go list -m rsc.io/q...
rsc.io/quote v1.5.2
rsc.io/quote/v3 v3.1.0
$
```

每一个 GO 模块的主要版本, 都会使用一个不同的路径: 从 v2 开始, 路径必须以主版本号结尾.
比如 `rsc.io/quote` 的 v3 版本, 不再是 `rsc.io/quote`, 而是独立的名字 `rsc.io/quote/v3`.
这种用法叫做 **语义导入版本化**, 它给了不兼容的包(不同主版本的包)一个不同的名字.

go 命令允许构建包含任何特定模块路径的至多一个版本, 意味着每一个主版本最多一个路径:
一个 `rsc.io/quote`, 一个 `rsc.io/quote/v2`, 一个 `rsc.io/quote/v3`等等.
这给予了模块作者一个清晰的规则, 一个模块路径是否可能出现副本: 一个程序不可能同时使用
`rsc.io/quote v1.5.2` 和 `rsc.io/quote v1.6.0`. 同时, 一个模块的不同主版本允许共存,
能帮助模块的消费者可以渐进地升级到新的主版本上.

在这个例子中, 我们想要使用 `rsc/quote/v3 v3.1.0` 中的 `quote.Concurrency`, 但我们还没
做好准备迁移对 `rsc.io/quote v1.5.2` 的使用.

在大型程序或代码库中, 逐步迁移的能力尤其重要.

### 升级依赖到新的主版本

让我们继续完成迁移, 开始只使用 `rsc.io/quote/v3`. 因为主版本的改变, 我们预计到某些 APIs
可能已经被移除, 重命名, 或者以其他不兼容的方式改变了.

通过阅读文档, 我们发现 `Hello` 已经变成了 `HelloV3`:

```bash
$ go doc rsc.io/quote/v3
package quote // import "rsc.io/quote/v3"

Package quote collects pithy sayings.

func Concurrency() string
func GlassV3() string
func GoV3() string
func HelloV3() string
func OptV3() string
$
```

我们通过升级将 `hello.go` 中的 `quote.Hello()` 改变为 `quoteV3.HelloV3()`.

```go
package hello

import quoteV3 "rsc.io/quote/v3"

func Hello() string {
    return quoteV3.HelloV3()
}

func Proverb() string {
    return quoteV3.Concurrency()
}
```

在这个节点上, 我们无需重命名导入了, 所以可以这样做:

```go
package hello

import "rsc.io/quote/v3"

func Hello() string {
    return quote.HelloV3()
}

func Proverb() string {
    return quote.Concurrency()
}
```

重新运行测试, 一切正常.

### 移除未使用的依赖

我们已经移除了对 `rsc.io/quote` 的使用, 但它依然出现在 `go list -m all`
和 `go.mod` 文件中.

为什么? 因为 `go build` 和 `go test` 可以轻易告诉我们某些东西丢失了,
需要添加, 但无法告诉我们某些东西可以安全地被移除.

移除一个依赖, 只有在检查过模块中的所有包, 和这些包所有可能的构建标签组合
之后才能确定. 一个普通的构建命令是不会加载这些信息的, 所以它不能安全地移除依赖.

`go mod tidy` 可以清除这些未使用的包.

## 结论

在 Go 中 Go 模块是依赖管理的未来. 模块功能在所有支持的 Go 版本中是可用的了(GO 1.11 之后).

总结一下使用 Go 模块的工作流:

- `go mod init` 创建一个新的模块, 初始化 `go.mod` 文件
- `go build, go test` 和其他的包构建命令会添加必要的依赖到 `go.mod` 文件中
- `go list -m all` 打印出当前模块的依赖
- `go get` 改变一个依赖的必要版本
- `go mod tidy` 移除未使用的依赖
