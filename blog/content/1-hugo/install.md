+++
title = "安装启动"
date = 2019-06-22T18:57:32+08:00
weight = 1
+++

## 快速安装

Hugo 虽然是基于 go 语言的项目, 但最懒的方式还是去 [releases](https://github.com/gohugoio/hugo/releases) 页面
手动下载预编译的二进制包.

解压出来也只有单个的二进制文件, 如果想全局使用, 就添加到环境变量中吧. 但对我的博客项目来说, 没什么必要,
直接新建一个 bin 目录丢进去就行. 直接放在根目录也是行的, 甚至更方便.

## 必要假设

接下来运行的命令都基于以下假设

- 根目录下有个 bin 文件, 里面是名为 hugo 的二进制程序
- 运行路径是根目录
- 因为都是在根目录运行的, 所以运行 hugo 时, 需要指定选项 `-s ./blog`

## 新建站点

新建一个站点, 取名为 `blog`, 这个是网站的根目录名称.

```shell
./bin/hugo new site blog
```

## 添加主题

这里我使用的是 [HUGO LEARN THEME](https://learn.netlify.com/en/) 主题.

```shell
git submodule add https://github.com/matcornic/hugo-theme-learn.git blog/themes/hugo-theme-learn
echo 'theme = "hugo-theme-learn"' >> blog/config.toml
```

使用 git 的 submodule 添加, 目的地路径是 `blog/themes/hugo-theme-learn`.

同时, 修改配置文件 `config.toml` 中的选项, 将 `theme` 的值改为对应的主题, 必须跟 `blog/themes/` 目录下
的主题名称一致.

## 添加文章

添加文章的基础命令是 `hugo new`, 但因为涉及到主题相关的内容, 在后面介绍.

```shell
./bin/hugo new posts/doc.md -s ./blog
```

## 启动

```shell
./bin/hugo server -D -s ./blog
```

## 生成静态网站

先去配置文件中修改一下导出目录, 这里我设置为根目录下 public 目录, 添加如下配置

```toml
publishdir = "../public"
```

运行命令

```shell
./bin/hugo -s ./blog
```
