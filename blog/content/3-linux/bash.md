+++
title = "Bash 脚本使用指南"
date =  2020-06-21T08:30:15+08:00
weight = 5
+++

## 简介

Bash 脚本在 linux 上还是非常有用的. 以前没有仔细用过, 这些结合教程, 好好学习了一遍, 顺便做些笔记, 也当作自己的快速参考指南.

当前所看的教程是 [Bash 脚本教程](https://wangdoc.com/bash/intro.html).

## Shell

Shell 可以理解为与内核交互的环境, 同时也是一个命令解释器.

查看当前时使用的 Shell

```bash
echo $SHELL
```

查看当前系统里已安装的所有 Shell

```bash
cat /etc/shells
```

进入和退出 Bash

```bash
bash

exit
```

查看 Bash 版本

```
bash --version

echo $BASH_VERSION
```

## 基础语法

echo 是一个非常基础的输出命令, 用于在屏幕上输出一行文本.

一些常见的用法如下:

```bash
# 常见用法
echo hello world
# -n 取消行尾的换行符
echo -n hello world
# -e 解释引号中的特殊字符
echo -e "hello\nworld"
```

1. Bash 使用空格(或 Tab)区分不同的参数.
2. 使用分号 `;` 作为命令的结束符. 借助分号可以在一行中使用多个命令.
3. 命令组合符 `&&` 和 `||` 可以控制多个命令的发生关系.
   1. `Command1 && Command2` 在第一个命令成功后, 继续运行第二个命令
   2. `Command1 || Command2` 在第一个命令失败后, 继续运行第二个命令
4. 命令有很多类型, 有些是内置命令, 有些是外部程序. 使用 `type` 获取命令来源.

Bash 中的一些快捷键, **非常基础且实用**, 建议速记:

- Ctrl + L 清除屏幕并将当前行移到页面顶部。
- Ctrl + C 中止当前正在执行的命令。
- Shift + PageUp 向上滚动。
- Shift + PageDown 向下滚动。
- Ctrl + U 从光标位置删除到行首。
- Ctrl + K 从光标位置删除到行尾。
- Ctrl + D 关闭 Shell 会话。
- ↑，↓ 浏览已执行命令的历史记录。

## 模式扩展

模式扩展是指 Bash 会将用户命令中的特殊字符扩展为完整的定义, 然后才继续执行对应的命令. 类似于简化版的 `正则表达式`.

Bash 共有 8 种扩展:

- `~` 字符扩展
- `?` 字符扩展
- `*` 字符扩展
- 方括号扩展
- 大括号扩展
- 变量扩展
- 子命令扩展
- 算术扩展

在 Bash 中打开或关闭扩展

```bash
# 打开模式扩展
set +o noglob
set +f

# 关闭扩展
set -o noglob
set -f
```

1. `~` 会自动扩展为当前用户的主目录
2. `?` 表示文件路径中的任意**单个**字符, 不包括空格
3. `*` 表示文件路径中的**任意数量**的任意字符, 包括零个字符
4. `[...]` 方括号扩展匹配括号中的任意一个字符
5. `[start-end]` 方括号扩展的简写形式, 表示一个连续的范围
6. `{.,.,.}` 大括号扩展表示大括号中的所有值, 使用逗号分隔值. _逗号前后不能有空格._ 可以用于多字符的匹配.
7. `{start..end}` 大括号的简写模式, 表示一个连续的范围. 支持逆序.
8. Bash 将以 `$` 开头的词元视为变量. 变量也可以用 `%{}` 形式.
9. `$(...)` 可以扩展为另一个命令的运行结果.
10. `$((...))` 可以扩展为整数运行的结果.

**用于文件路径匹配时, 需要文件确实存在时才会扩展. 否则会原样输出**
文件名扩展时只适用于单层路径, 不能跨目录匹配. Bash4.0 之后可以用 `**` 匹配零个或多个子目录.

一些示例:

```bash
echo ~
ls ?.txt
ls *.txt
ls [ab].txt
ls [a-c].txt
echo {1,2,3}
echo {a..c}
echo $SHELL
echo $(date)
echo $((2 + 2))
```

`[[:class:]]` 表示一个字符类. 常用的如下:

- `[[:alnum:]]` 匹配任意英文字母与数字
- `[[:alpha:]]` 匹配任意英文字母
- `[[:blank:]]` 空格和 Tab 键。
- `[[:cntrl:]]` ASCII 码 0-31 的不可打印字符。
- `[[:digit:]]` 匹配任意数字 0-9。
- `[[:graph:]]` A-Z、a-z、0-9 和标点符号。
- `[[:lower:]]` 匹配任意小写字母 a-z。
- `[[:print:]]` ASCII 码 32-127 的可打印字符。
- `[[:punct:]]` 标点符号（除了 A-Z、a-z、0-9 的可打印字符）。
- `[[:space:]]` 空格、Tab、LF（10）、VT（11）、FF（12）、CR（13）
- `[[:upper:]]` 匹配任意大写字母 A-Z。
- `[[:xdigit:]]` 16 进制字符（A-F、a-f、0-9）。

量词语法用于控制模式匹配的次数, 只有在 Bash 的 `extglob` 参数打开的情况下使用.

- `?(pattern-list)` 匹配零个或一个模式。
- `*(pattern-list)` 匹配零个或多个模式。
- `+(pattern-list)` 匹配一个或多个模式。
- `@(pattern-list)` 只匹配一个模式。
- `!(pattern-list)` 匹配零个或一个以上的模式，但不匹配单独一个的模式。

`shopt` 可以调整 Bash 的行为.

```bash
# 打开某个参数
$ shopt -s [optionname]

# 关闭某个参数
$ shopt -u [optionname]

# 查询某个参数关闭还是打开
$ shopt [optionname]
```

- dotglob 扩展结果包含隐藏文件(以点开头的文件)
- nullglob 通配符不匹配任何文件名时返回空字符串
- failglob 通配符不匹配任何文件名是, 直接报错
- extglob 使得 Bash 支持一些 ksh 的扩展语法
- nocaseglob 让通配符匹配不区分大小写
- globstar 使用 `**` 可以匹配零个或多个子目录

## 引号和转义

1. 使用 `\` 进行转义.
2. 单引号用于保留字符的字面含义, 各种特殊字符在单引号中都会变成普通字符
3. 双引号会保留大部分特殊字符的含义, 但除了美元符 `$`, 反引号 `` ` ``, 和反斜杆 `\` 会被自动扩展.

使用 `Here 文档` 可以输入多行字符串.

```bash
<< token
text
text
token
```

其中 `<< token` 是开始标记, `token` 是结束标记. Here 文档中会发生变量替换, 同时支持反斜杆转义, 但不支持通配符扩展. `<< token` 中的空格可有可无.

Here 文档的一个变体是 `<<<`, 将字符串通过标准输入传递给命令.

```bash
cat <<< 'hi there'
```

## 变量

使用 `env` 或 `printenv` 显示环境变量

声明变量

```bash
variable=value
myvar="hello world"
```

读取变量: 在变量名前加上 `%` 字符

```bash
foo=bar
echo $foo
```

删除变量, 使用 `unset`.

```bash
unset NAME
```

输出变量, 使用 `export`. `export` 用于向子 Shell 输出环境变量.

```bash
NAME=foo
export NAME
```

特殊变量:

- `$?` 上一个命令的退出码
- `$$` 当前 Shell 的进程 ID
- `$_` 上一个命令的最后一个参数
- `$!` 最近一个后台执行的异步命令的进程 ID
- `$0` 当前 Shell 的名称或脚本名
- `$-` 当前 Shell 的启动参数
- `$@` 和 `$#` 脚本的参数数量
- `$1 - $9` 表示脚本的第 1 - 9 个参数

设置变量的默认值:

- `${varname:-word}` varname 存在且不为空返回 varname, 否则返回 word. (保证有默认值兜底)
- `${varname:=word}` varname 存在且不为空返回 varname, 否则将它设置为 word 并返回 word. (设置变量的默认值)
- `${varname:+word}` varname 存在且不为空返回 word, 否则返回空值. (测试变量是否存在)
- `${varname:?message}` varname 存在且不为空返回 varname, 否则打印出 `varname:message` 并中断脚本执行 (防止变量未定义)

一些其他用于声明变量的命令:

1. `declare` 声明特殊类型的变量.

   ```bash
   declare OPTION VARIABLE=value
   ```

   - `-a` 声明数组变量。
   - `-f` 输出所有函数定义。
   - `-F` 输出所有函数名。
   - `-i` 声明整数变量。
   - `-l` 声明变量为小写字母。
   - `-p` 查看变量信息。
   - `-r` 声明只读变量。
   - `-u` 声明变量为大写字母。
   - `-x` 该变量输出为环境变量。

2. `readonly` 声明一个只读的变量.
3. `let` 声明变量时, 可以直接执行算术表达式

## 字符串操作

1. `${#varname}` 获取字符串长度
2. `${varname:offset:length}` 提取子字符串. offset 从 0 开始计算.
3. 字符串的搜索和替换
4. `${varname^^}` 转换为大写形式
5. `${varname,,}` 转换为小写形式

### 字符串的搜索和替换

1. 字符串头部的模式匹配

检查字符串的开头是否匹配给定的模式. 匹配成功后会删除匹配成功的部分, 返回剩余的部分. 不改变原始变量.

```bash
# 如果 pattern 匹配变量 variable 的开头，
# 删除最短匹配（非贪婪匹配）的部分，返回剩余部分
${variable#pattern}

# 如果 pattern 匹配变量 variable 的开头，
# 删除最长匹配（贪婪匹配）的部分，返回剩余部分
${variable##pattern}
```

2. 字符串尾部的模式匹配

```bash
# 如果 pattern 匹配变量 variable 的结尾，
# 删除最短匹配（非贪婪匹配）的部分，返回剩余部分
${variable%pattern}

# 如果 pattern 匹配变量 variable 的结尾，
# 删除最长匹配（贪婪匹配）的部分，返回剩余部分
${variable%%pattern}
```

3. 任意位置的模式匹配

```bash
# 如果 pattern 匹配变量 variable 的一部分，
# 最长匹配（贪婪匹配）的那部分被 string 替换，但仅替换第一个匹配
${variable/pattern/string}

# 如果 pattern 匹配变量 variable 的一部分，
# 最长匹配（贪婪匹配）的那部分被 string 替换，所有匹配都替换
${variable//pattern/string}
```


## 算术运算

1. `((...))` 整数的算术运算, 使用 `$((...))` 读取算术运算的结果
2. 使用其他进制
    1. `number`  十进制
    2. `0number` 八进制
    3. `0xnumber` 十六进制
    4. `base#number` base 进制
3. `$((...))` 支持二进制的位运算
    - `<<` 位左移运算，把一个数字的所有位向左移动指定的位。
    - `>>` 位右移运算，把一个数字的所有位向右移动指定的位。
    - `&` 位的“与”运算，对两个数字的所有位执行一个AND操作。
    - `|` 位的“或”运算，对两个数字的所有位执行一个OR操作。
    - `~` 位的“否”运算，对一个数字的所有位取反。
    - `^` 位的异或运算（exclusive or），对两个数字的所有位执行一个异或操作。
4. `$((...))` 支持的逻辑运算. 如果表达式为真, 返回 1, 否则返回 0.
    - `<` 小于
    - `>` 大于
    - `<=` 小于或相等
    - `>=` 大于或相等
    - `==` 相等
    - `!=` 不相等
    - `&&` 逻辑与
    - `||` 逻辑或
    - `!` 逻辑否
    - `expr1?expr2:expr3` 三元条件运算符。若表达式expr1的计算结果为非零值（算术真），则执行表达式expr2，否则执行表达式expr3。
5. `$((...))` 可以执行赋值运算.
    - `parameter = value` 简单赋值。
    - `parameter += value` 等价于parameter = parameter + value。
    - `parameter -= value` 等价于parameter = parameter – value。
    - `parameter *= value` 等价于parameter = parameter * value。
    - `parameter /= value` 等价于parameter = parameter / value。
    - `parameter %= value` 等价于parameter = parameter % value。
    - `parameter <<= value` 等价于parameter = parameter << value。
    - `parameter >>= value` 等价于parameter = parameter >> value。
    - `parameter &= value` 等价于parameter = parameter & value。
    - `parameter |= value` 等价于parameter = parameter | value。
    - `parameter ^= value` 等价于parameter = parameter ^ value。
6. `$((...))` 内逗号`,`是求值运算符, 执行前后两个表达式, 并返回后一个表达式的值.
7. `expr` 命令支持算术运算, 可以不使用 `((...))`.

## 行操作

**这一节可以极大加速命令行使用中的操作速度, 建议速记.**

Bash 内置了 Readline 库, 提供了很多行操作.

光标移动

- `Ctrl + a` 移到行首。
- `Ctrl + b` 向行首移动一个字符，与左箭头作用相同。
- `Ctrl + e` 移到行尾。
- `Ctrl + f` 向行尾移动一个字符，与右箭头作用相同。
- `Alt + f` 移动到当前单词的词尾。
- `Alt + b` 移动到当前单词的词首。

清除屏幕使用 `Ctrl + l`, 和 `clear` 命令作用相同.

编辑操作

- `Ctrl + d` 删除光标位置的字符（delete）。
- `Ctrl + w` 删除光标前面的单词。
- `Ctrl + t` 光标位置的字符与它前面一位的字符交换位置（transpose）。
- `Alt + t` 光标位置的词与它前面一位的词交换位置（transpose）。
- `Alt + l` 将光标位置至词尾转为小写（lowercase）。
- `Alt + u` 将光标位置至词尾转为大写（uppercase）。

- `Ctrl + k` 剪切光标位置到行尾的文本。
- `Ctrl + u` 剪切光标位置到行首的文本。
- `Alt + d` 剪切光标位置到词尾的文本。
- `Alt + Backspace` 剪切光标位置到词首的文本。
- `Ctrl + y` 在光标位置粘贴文本。

- `Tab` 完成自动补全。
- `Alt + ?` 列出可能的补全，与连按两次 Tab 键作用相同。
- `Alt + /` 尝试文件路径补全。
- `Ctrl + x /` 先按Ctrl + x，再按/，等同于Alt + ?，列出可能的文件路径- 补全。
- `Alt + !` 命令补全。
- `Ctrl + x !` 先按Ctrl + x，再按!，等同于Alt + !，命令补全。
- `Alt + ~` 用户名补全。
- `Ctrl + x ~ `先按Ctrl + x，再按~，等同于Alt + ~，用户名补全。
- `Alt + $` 变量名补全。
- `Ctrl + x $` 先按Ctrl + x，再按$，等同于Alt + $，变量名补全。
- `Alt + @` 主机名补全。
- `Ctrl + x @` 先按Ctrl + x，再按@，等同于Alt + @，主机名补全。
- `Alt + *` 在命令行一次性插入所有可能的补全。
- `Alt + Tab` 尝试用.bash_history里面以前执行命令，进行补全。

### 操作历史

Bash 会保留用户的操作历史, 退出 Shell 式, 会将操作历史写入都 `~/.bash_history` 中.

```bash
echo $HISTFILE
```

`!e` 表示找出操作历史中, 最近的一条以 `e` 开头的命令并执行.
Bash 会先输出那条命令, 然后直接执行. 

`history` 会显示操作历史. 可以通过定制 `HISTTIMEFORMAT` 来显示每个操作的时间.

- `Ctrl + p` 显示上一个命令，与向上箭头效果相同（previous）。
- `Ctrl + n` 显示下一个命令，与向下箭头效果相同（next）。
- `Alt + <` 显示第一个命令。
- `Alt + >` 显示最后一个命令，即当前的命令。
- `Ctrl + o` 执行历史文件里面的当前条目，并自动显示下一条命令。这对重复执行某个序列的命令很有帮助。

- `!!` 执行上一个命令。
- `!n` 执行历史文件里面行号为n的命令。
- `!-n` 执行当前命令之前n条的命令。
- `!string` 执行最近一个以指定字符串string开头的命令。
- `!?string` 执行最近一条包含字符串string的命令。
- `^string1^string2` 执行最近一条包含string1的命令，将其替换成string2。

- `Ctrl + j` 等同于回车键（LINEFEED）。
- `Ctrl + m` 等同于回车键（CARRIAGE RETURN）。
- `Ctrl + o` 等同于回车键，并展示操作历史的下一个命令。
- `Ctrl + v` 将下一个输入的特殊字符变成字面量，比如回车变成^M。
- `Ctrl + [` 等同于 ESC。
- `Alt + .` 插入上一个命令的最后一个词。
- `Alt + _` 等同于Alt + .。

## 目录堆栈

1. `cd -` 进度前一次的目录
2. `pushd` 进入目录, 并将该目录放入堆栈
3. `popd` 移除堆栈顶部的记录, 并进入新的堆栈顶部目录
4. `dirs` 显示目录堆栈的内容

`pushd` 和 `popd` 支持的参数:

- `-n` 仅操作堆栈, 不改变目录
- `整数参数` 该整数表示堆栈中的指定位置的记录. 从 0 开始.
- `目录参数` pushd 可以接受一个目录作为参数, 表示将目录放到堆栈顶部, 并进入该目录

## 脚本入门

脚本的第一行通常是指定解释器. 这一行以 `#!` 开头, 这个字符被称为 `Shebang`.

```bash
#!/bin/bash
```

脚本通常需要执行权限, 使用 chmod 添加权限

```bash
chmod +x script.sh
```

如果需要脚本在任何地方都能执行,必须加到环境变量 `$PATH` 中.
比如将脚本统一放在 `~/bin` 目录, 然后将其加入到 `$PATH` 中.

```bash
export PATH=$PATH:~/bin
# 可以将上面这行加入到 ~/.bashrc 中, 然后运行下面这句使得生效
source ~/.bashrc
```

`#!/usr/bin/env NAME` 让 Shell 查找环境变量中第一个匹配的 NAME.

使用 `#` 表示注释.

### 脚本参数

调用脚本时, 脚本后面可以带有参数.

- `$0` 脚本文件名，即script.sh。
- `$1~$9` 对应脚本的第一个参数到第九个参数。
- `$#` 参数的总数。
- `$@` 全部的参数，参数之间使用空格分隔。
- `$*` 全部的参数，参数之间使用变量$IFS值的第一个字符分隔，默认为空格，但是可以自定义。
- `${10}` 脚本参数多于 10 以后, 可以用 `${}` 形式

`shift` 可以改变脚本参数, 每次执行都会移除脚本当前的第一个参数, 使得后面的参数前进一位.

`getopts` 可以解析复杂的脚本命令行参数, 获取所有带前置连词线 `-` 的参数.

```bash
getopts optstring name
```

`optstring` 给出脚本的所有连词线参数. 后面有冒号的表示有参数值.
`name` 是一个变量名, 用来保存当前提取到的配置项参数.

```bash
while getopts 'lha:' OPTION; do
  case "$OPTION" in
    l)
      echo "linuxconfig"
      ;;

    h)
      echo "h stands for h"
      ;;

    a)
      avalue="$OPTARG"
      echo "The value provided is $OPTARG"
      ;;
    ?)
      echo "script usage: $(basename $0) [-l] [-h] [-a somevalue]" >&2
      exit 1
      ;;
  esac
done
shift "$(($OPTIND - 1))"
```

`$OPTIND` 在开始执行前是 1, 每次执行都会加 1.
`$OPTIND - 1` 是已经处理的连词线参数的个数, 使用 shift 将这些参数移除.

配置项参数终止符 `--`, 可以让执行变量只能作为实体参数, 而不能作为配置项参数.

```bash
myPath="~/docs"
ls -- $myPath
```

`exit` 用于终止当前脚本的执行, 并向 Shell 返回一个退出值.

命令执行结束后, 有一个返回值. 0 表示成功, 非 0 表示失败.
用 `$?` 可以读取前一个命令的返回值.

`source` 用于执行一个脚本, 通常用于**重载一个配置文件**.

`alias` 可以为一个命令执行别名.

```bash
# 指定别名
alias NAME=DEFINITION

# 列出所有别名
alias

# 解除别名
unalias lt
```

