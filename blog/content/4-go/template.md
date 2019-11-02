+++
title = "Template 笔记"
date =  2019-11-02T14:33:53+08:00
weight = 2
+++

## 简介

包名 `text/template` , [文档](https://golang.org/pkg/text/template/)

实现了数据驱动的模版, 用于生成文本输出.

要在生成 html 文件, 可以使用包 `html/template` .

## 语法

模版中的注解引用数据结构的元素来控制执行, 获取值并显示. 数据结构通常是一个 struct 中的 field 或者一个 map 中的 key. 执行模版时遍历结构并设置光标 使用一个前缀 `.` 表示, 叫做 `dot`,  作为执行过程中当前位置的值.

数据执行或者控制语句都是有 `{{` 和 `}}` 包围的.

    type Inventory struct {
    	Material string
    	Count    uint
    }
    sweaters := Inventory{"wool", 17}
    tmpl, err := template.New("test").Parse("{{.Count}} items are made of {{.Material}}")
    if err != nil { panic(err) }
    err = tmpl.Execute(os.Stdout, sweaters)
    if err != nil { panic(err) }

使用 `{{-` 会删除在它之前的所有尾随空格, `-}}` 会删除它之后的所有尾随空格. 

    "{{23 -}} < {{- 45}}"
    
    "23<45"

### Actions

所有 Actions 的用法说明.

    {{/* 评论 */}}
    {{- /* a comment with white space trimmed from preceding and following text */ -}}
    	评论会被丢弃, 可能包含换行符.
    	评论不能嵌套, 必须以分隔符开始并结束.
    
    {{pipeline}}
    	默认的文本表示 (和 fmt.Print 打印的结果一样) , pipeline 的值会被复制到输出中.
    
    {{if pipeline}} T1 {{end}}
    	如果 pipeline 是空值, 不会产生任何东西;
    	否则, T1 会执行. 空值是 false, 0, 任何 nil 指针或 interface 值, 
    	任何长度为 0 的 array, slice, map, 或 string.
    	dot 没影响.
    
    {{if pipeline}} T1 {{else}} T0 {{end}}
    	如果 pipeline 是空值, T0 会执行;
    	否则, T1 会执行. dot 没影响.
    
    {{if pipeline}} T1 {{else if pipeline}} T0 {{end}}
    	简化 if-else 链, 一个 if 的 else 可能直接包含另一个 if.
    	和下面的语句效果一样
    		{{if pipeline}} T1 {{else}}{{if pipeline}} T0 {{end}}{{end}}
    
    {{range pipeline}} T1 {{end}}
    	pipeline 的值必须是一个 array, slice, map, 或 channel.
    	如果 pipeline 的值长度为 0, 什么都不会输出;
    	否者, dot 会设置为 array, slice, or map 中的每一个元素, 
    	然后执行 T1. 如果值是一个 map 且
    	它的 keys 是基础 type 且有一个定义好的顺序 ("可比较的"), 
    	元素们会按定义好的顺序访问.
    
    {{range pipeline}} T1 {{else}} T0 {{end}}
    	pipeline 的值必须是一个 array, slice, map, or channel.
    	如果 pipeline 的值长度为 0, dot 没影响, 并且
    	T0 会被执行; 否者, dot 会被设置为
    	array, slice, or map 中的每一个元素, 且 T1 会被执行.
    
    {{template "name"}}
    	名字为 name 的模版会被执行, 使用 nil 作为模版的参数.
    
    {{template "name" pipeline}}
    	名字为 name 的模版会被执行, 并将 dot 设置为 pipeline 的值, 作为模版参数.
    
    {{block "name" pipeline}} T1 {{end}}
    	一个 block 是一个快捷方式, 定义一个如下的模版
    		{{define "name"}} T1 {{end}}
    	并且就地执行
    		{{template "name" pipeline}}
    	典型用法是定义一组根模版, 然后通过重写 block 模版来自定义.
    
    {{with pipeline}} T1 {{end}}
    	如果 pipeline 是空的, 什么都不会产生;
    	否者, dot 被设置为 pipeline 的值, 且 T1 会被执行.
    
    {{with pipeline}} T1 {{else}} T0 {{end}}
    	如果 pipeline 是空的, dot 不受影响且 T0 会被执行;
    	否则 dot 被执行为 pipeline 的值, 且 T1 会被执行.

### Arguments

一个 argument 是一个简单的值, 由以下之一表示:

    - 一个 boolean, string, character, integer, floating-point, imaginary
      or complex constant in Go syntax. 这些就像是 Go 的无类型常量.
      注意, 和 Go 一样, 当分配或传递给一个函数时, 是否发生大整数溢出取决于
    	主机的 int 是 32 还是 64 位的.
    - 关键字 nil, 表示一个无类型的 Go nil.
    - 字符 '.' (点号):
    	.
      结果是 dot 的值.
    - 一个变量名, 它可能是一个 (可能为空的) 字母数字 string, 
    	有一个美元前缀, 比如
    	$piOver2
      or
    	$
      结果是变量的值.
      变量在下面描述.
    - data 中的一个 field 的名字, data 必须是一个 struct, 
    	有一个点前缀, 比如
    	.Field
      结果是 field 的值. Field 是可以链式调用的:
        .Field1.Field2
      Fields 也可以在变量上调用, 包括链式调用:
        $x.Field1.Field2
    - data 中的一个 key 的名字, data 必须是一个 map, 
    	有一个点前缀, 比如
    	.Key
      结果是 map 中 key 对应的值.
      Key 调用可以是链式的, 也可以无限组合 field:
        .Field1.Key1.Field2.Key2
      虽然 key 必须是一个字母数字标识符, 但不需要像 field 一样
    	必须以大写字母开头.
      Keys 也可以在变量上执行, 包括链式调用:
        $x.key1.key2
    - data 的一个 niladic 方法的名字, 
    	有一个点前缀, 比如:
    	.Method
      结果是使用 dot 作为接收者调用方法后的值, dot.Method(). 
    	这个方法必须有一个访问值 (任何类型)或 者两个返回值, 第二个返回值是 error.
      如果有两个返回值, 返回的 error 是 non-nil, 执行会中断, 
      一个 error 会作为执行的结果返回给调用者.
      方法调用可以链式或者组合 fields 和 keys, 在任何层级上:
        .Field1.Key1.Method1.Field2.Key2.Method2
      方法也能在变量上执行, 包括链式调用:
        $x.Method1.Field
    - 一个 niladic 函数的名字, 比如
    	fun
    	结果是调用这个函数的返回值, fun(). 返回类型和返回值和 methods 一样.
      Functions 和 function 名称在下面讲述.
    - 一个带有括号的上述实例, 用于分组. 
    	结果可以像 field 或者 map key 一样调用.
    	print (.F1 arg1) (.F2 arg2)
    	(.StructValuedMethod "arg").Field

### Pipelines

一个 pipeline 是一组链式的命令. 一个命令是一个简单值(argument) 或者一个可能使用多个参数的函数或方法调用.

    Argument
    	结果是执行 argument 后的值.
    .Method [Argument...]
    	method 可以是单独的或者 chain 的最后一个,
    	但是不像在chain 中的 method, 这两种方式可以使用参数.
    	结果是使用参数调用方法后的值:
    		dot.Method(Argument1, etc.)
    functionName [Argument...]
    	结果是使用 name 调用函数后的值:
    		function(Argument1, etc.)
    	Functions 和 function 名称在下面讲述.

一个 pipeline 可能被管道字符 `|` 分隔的一系列命令链接起来. 在一个链接的 pipeline 中, 每一个命令的结果会作为最后一个参数传递到后续的命令中. pipeline 中的最后一个命令的输出作为 pipeline 的值.

命令的输出可能是一个值或者两个值, 第二个值是 error 类型. 如果第二个参数存在, 且是 non-nil, 执行会终止, 且 error 会返回给调用者.

### Variables

一个 action 中的 pipeline 可能初始化一个变量来保存结果. 初始化有这样的语法:

    $variable := pipeline

`$variable` 是变量的名字. 一个声明了变量的 action 没有输出.

先前声明的变量也重新分配, 使用语句:

    $variable = pipeline

如果一个 range action 初始化一个变量, 变量设置为每一次迭代中的连续元素. range 可能声明两个元素, 通过逗号分隔:

    range $index, $element := pipeline

$index and $element 会被设置为 array/slice 的索引和值, map 的 key 和 value. 注意, 如果只有一个变量, 它会被设置为元素(而不是索引或 key), 这和 Go range 语句的用法相反.

一个变量的范围直到声明它的控制结构 ("if", "with", or "range") 中的 end action 为止. 如果没有控制结构, 则直到模版的结尾为止. 一个模版调用不会从它的调用点继承变量.

当执行开始时, $ 被设置为 data argument 传递给 Execute, 也就是 dot 的起始值.

### Examples

这里有一些单行的模版演示了 pipeline 和变量. 所有都会产生 `"output"`

    {{"\"output\""}}
    	一个 string 常量.
    {{`"output"`}}
    	一个 raw string 常量.
    {{printf "%q" "output"}}
    	一个函数调用.
    {{"output" | printf "%q"}}
    	一个函数调用, 它的最后一个参数来自于前一个命令.
    {{printf "%q" (print "out" "put")}}
    	一个括号内的参数.
    {{"put" | printf "%s%s" "out" | printf "%q"}}
    	一个更复杂的调用.
    {{"output" | printf "%s" | printf "%q"}}
    	一个更长的 chain.
    {{with "output"}}{{printf "%q" .}}{{end}}
    	一个使用 dot 的 action.
    {{with $x := "output" | printf "%q"}}{{$x}}{{end}}
    	一个创建并使用变量的 action.
    {{with $x := "output"}}{{printf "%q" $x}}{{end}}
    	一个使用另一个 action 中的变量的 action.
    {{with $x := "output"}}{{$x | printf "%q"}}{{end}}
    	和上面相同, 但是使用 pipeline.

### Functions

在执行期间, 函数可以在两个 function maps 中找到: 第一个在模版中, 第二个在全局的 function map 中. 默认的, 没有函数被定义在模版中, 但是可以使用 Funcs method 添加它们.

预定义的全局函数的命名如下:

    and
    	对它的参数们进行布尔 AND 运算, 返回第一个空参数或者最后一个参数,
    	"and x y" 表现得像是 "if x then y else x". 
    	所有的参数都会被执行.
    call
    	返回第一个参数调用后的结果, 第一个参数必须是函数, 其他的参数作为它的参数.
    	因此 "call .X.Y 1 2" 在 Go 调用中就是 dot.X.Y(1, 2),
    	Y 是一个 func-valued field, map entry, 或者类似的.
    	第一个参数必须是 function 类型的值(不同于预定义的函数, 比如 print).
    	这个函数必须返回一个或两个值, 第二个值的类型是 error. 
    	如果参数不匹配函数的要求, 或者返回的值 error 是 non-nil, 执行会终止.
    html
    	返回它的参数的转义过的 HTML 文本表示.
    	除了一些例外, 这个函数在 html/template 是不可用的.
    index
    	返回第一个参数的索引, 通过其他参数作为索引.
    	因此 "index x 1 2 3" 在 Go 语法中就是 x[1][2][3]. 
    	每一个索引值必须是 map, slice, 或 array.
    js
    	返回它的参数的转义过的 JavaScript 文本表示.
    len
    	返回它的参数的长度.
    not
    	返回它的单个参数的布尔相反类型.
    or
    	对它的参数们进行布尔 NOT 运算, 返回第一个非空参数或者最后一个.
    	"or x y" 表现得像是 "if x then x else y". 
    	所有的参数都会被执行.
    print
    	fmt.Sprint 的别名.
    printf
    	fmt.Sprintf 的别名.
    println
    	fmt.Sprintln 的别名.
    urlquery
    	返回参数们的 URL query 形式, 并对每个参数进行转义后的文本表示.
    	除了一些例外, 这个函数在 html/template 是不可用的.

布尔函数将任何零值设置为 false, 非零值设置为 true.

还有一组二元的比较运算符被定义为函数:

    eq
    	Returns the boolean truth of arg1 == arg2
    ne
    	Returns the boolean truth of arg1 != arg2
    lt
    	Returns the boolean truth of arg1 < arg2
    le
    	Returns the boolean truth of arg1 <= arg2
    gt
    	Returns the boolean truth of arg1 > arg2
    ge
    	Returns the boolean truth of arg1 >= arg2

为了简化多元相等比较, eq 支持两个或多个参数, 会将第一个参数和其他参数比较, 等价于:

    arg1==arg2 || arg1==arg3 || arg1==arg4 ...

(不像 Go 中的 || , eq 是一个函数调用, 所有的参数都会被执行).

比较函数只适用于基本类型(或者基本类型的别名 比如 "type Celsius float32"). 它们实现了 Go 比较值的规则, 除了忽略大小和确切的类型, 所以任何整型, 有符号还是无符号的, 都可以和其他整型比较. (算术值比较, 而不是 bit 匹配, 所以所有的负整数小于所有的无符号整数). 但是, 和以前一样, 整型不能和 float32 之类的浮点数比较.

### Associated templates

每个模版都在创建时通过一个字符串命名. 每个模版都可以关联零个或多个其他的模版,, 并通过名字调用 所以关联是可以传递的, 并形成了一个模版的命名空间.

一个模版可能使用一个模版调用来实例化另一个关联的模版, 参见上面 template action 的说明.  name 必须是与包含调用的模版有关联的模版.

### Nested template definitions

当解析一个模版时, 可能定义另一个模版, 并与正在解析的模版相关联. 模版定义必须出现在模版的最顶层, 就像是 Go 程序中的全局变量.

这种定义的语法是使用 define action 和 end action 包围每一个模版的定义.

define action 通过提供一个字符串常量来命名模版. 这里有个简单的例子:

    `{{define "T1"}}ONE{{end}}
    {{define "T2"}}TWO{{end}}
    {{define "T3"}}{{template "T1"}} {{template "T2"}}{{end}}
    {{template "T3"}}`

这定义了两个模版, T1 和 T2. 第三个模版 T3 在执行的时候调用了它们. 最后, 调用了 T3. 执行这个模版会生成文本:

    ONE TWO

通过构造, 一个模版可能驻留在一个关联中. 如果有必要让模版在多个关联中可被寻址, 模版定义必须被解析多次来创建一个不同的 *Template 值, 或者必须听过 Clone 或 AddParseTree 方法复制.

解析可能被调用多次来组合不同关联的模版. 查看 ParseFiles 和 ParseGlob 函数和方法, 它们提供了解析存储在文件中的模版的简单方式.

一个模版可能直接执行或者通过 ExecuteTemplate, 后者执行 name 标识的模版. 为了调用我们在上面的例子, 我们可以写成:

    err := tmpl.Execute(os.Stdout, "no data needed")
    if err != nil {
    	log.Fatalf("execution failed: %s", err)
    }

或者基于特定的名字来执行模版:

    err := tmpl.ExecuteTemplate(os.Stdout, "T2", "no data needed")
    if err != nil {
    	log.Fatalf("execution failed: %s", err)
    }
