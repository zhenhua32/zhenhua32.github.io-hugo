+++
title = "Hugo New Theme 使用指南"
date =  2019-06-25T19:49:17+08:00
weight = 2
+++

## 简介

这里, 我使用的是 [Hugo New Theme](https://learn.netlify.com/en/) 主题.

这个主题是我在 search 分类下, 一眼就相中的, 可能是紫色太耀眼了.
其实, 我就是想把它作为自己的博客和笔记用, 有个搜索框方便些.
也可能是因为它的结构有点像 Python 很多库所用的文档生成器 Sphinx.

官方的简介里也说了, 这个主题是完全为 _文档_ 设计的.

## 安装配置

前面有介绍过安装主题. 基本上有两种方式:

- 直接下载主题的 zip 包, 然后手动解压到 themes 目录下
- 使用 git submodule 添加依赖

简单介绍下 git submodule 的用法.

```shell
git submodule add https://github.com/matcornic/hugo-theme-learn.git blog/themes/hugo-theme-learn
```

当然, 最后一步是去 config.toml 中配置一下主题.

```toml
theme = "hugo-theme-learn"
```

## 添加内容

这个主题下, 内容结构大致是这样的.

content 下的每个目录都是一个章节, 每个章节都有一个 `_index.md` 文件, 当作是章节的介绍.
然后, 就是普通的文章了.

### 创建章节

```shell
./bin/hugo new 1-hugo/_index.md --kind chapter -s ./blog
```

这里的主要命令格式是 `hugo new chapter/page.md`, new 后面的参数是文章的位置, 位置是相对于 `content` 目录的.
`--kind chapter` 用来指示这应该生成哪种类型的文件, 这里是 `chapter`.
`-s blog` 很常见了, 因为我们的 hugo 站点的根目录是在 blog 里的, 所以需要指定源目录.

### 创建内容页

```shell
./bin/hugo new 1-hugo/install.md -s ./blog
```

基本和上面创建章节页是差不多的, 主要是少了 `--kind chapter` 参数. 默认创建的是内容页.

### 创建自定义的页面

其实, 生成各种类型的页面都是自定义的, 具体内容是在 `archetypes` 目录下.
当然, 具体怎么将布局和页面类型结合起来还是要研究下.

另一点非常重要的是文章的排序. 可以使用 `weight` 排序, 定义在最上面的配置块中.

## 短代码

短代码是为了弥补 markdown 的缺憾而将一些常见的操作表示为自定义格式的简单代码段.
这些操作通常是没有被 markdown 支持的, 但可以使用 html 实现的.
毕竟 markdown 只是单纯用来写文档的, 你让它支持一些 js 操作就不现实了.

### 附件

    {{%/*attachments title="Related files" pattern=".*(pdf|mp4)"/*/%}}

语法看起来是挺简单的, title 是标题, pattern 是正则, 过滤出要显示的文件,
style 是样式, 默认的样式包含 `“orange”, “grey”, “blue” and “green”`.

当然, 你需要将文件放置在指定的目录中才能被检索到.

- 如果页面是 page.md, 那么目录名为 page.files
- 如果页面是文件夹, 那么就要建一个子目录 files

### button

```
{{%/* button href="https://getgrav.org/" */%}}Get Grav{{%/* /button */%}}
{{%/* button href="https://getgrav.org/" icon="fas fa-download" */%}}Get Grav with icon{{%/* /button */%}}
{{%/* button href="https://getgrav.org/" icon="fas fa-download" icon-position="right" */%}}Get Grav with icon right{{%/* /button */%}}
```

按钮没什么好说的, 其实就是一个跳转链接, 只是看起来像按钮,
和 html 中的按钮的功能还是差好多.

### 子目录

这个还是挺实用的, 能列出下级目录的列表, 用在章节首页是挺好的.

    {{%/* children  */%}}

### mermaid

mermaid 也是支持的, 只是我还没仔细看过, 不知道怎么画图. 似乎是用作流程图的神器.

    {{</*mermaid align="left"*/>}}
    graph LR;
    	A[Hard edge] -->|Link text| B(Round edge)
    	B --> C{Decision}
    	C -->|One| D[Result one]
    	C -->|Two| E[Result two]
    {{</* /mermaid */>}}

支持好多种类型的图, 可以去 [官网](https://mermaidjs.github.io/) 观摩一番.

### 警告

```
{{%/* notice note */%}}
A notice disclaimer
{{%/* /notice */%}}
```

警告有很多种类型

- note
- info
- tip
- warning

### 心累

突然发觉要正常显示这些短代码的源代码也是困难的.
最后去看了作者的源码, 有些是空四格, 有些是用 ```.
