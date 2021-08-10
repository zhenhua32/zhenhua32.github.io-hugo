+++
title= "使用 Github Action"
date= 2021-08-10T20:32:22+08:00
weight = 3
+++

## 简介

以前也为这个仓库设置过 CI. 当时用的是 [buddy](https://buddy.works/).
这个是当时在 github market 中找的, 配置好了用着也挺舒服的.

唯一有点问题的是, 如果你长期不使用自己创建的 CI 流程, 那么基本上过一会时间,
大概是两三个月, 就会收到一封邮件, 提示如果再不登录的话, 就会自动注销账号.

在连续好几次这样的操作后, 终于在前段时间, 因为没有使用, 也没有及时查看邮件, 导致被注销了账号.

所以, 这就引出了这次的主题, [Github Action](https://docs.github.com/cn/actions).

> PS. 被微软收购后, 没想到文档都有中文了.

## 使用

当前仓库使用的文件, 可以在 `.github/workflows/go.yml` 中查看.

```yml
name: Go

on:
  push:
    branches: [master]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          persist-credentials: false # otherwise, the token used is the GITHUB_TOKEN, instead of your personal token
          fetch-depth: 0 # otherwise, you will failed to push refs to dest repo

      - name: Set up Go
        uses: actions/setup-go@v2
        with:
          go-version: 1.16

      - name: Build0
        run: chmod 777 ./bin/hugo

      - name: Build1
        run: git submodule init && git submodule update

      - name: Build2
        run: ./bin/hugo -s ./blog

      - name: Copy CNAME
        run: cp ./CNAME ./public

      - name: Commit
        run: |
          cd ./public
          git init
          git config --local user.email "zhenhua32@gmail.com"
          git config --local user.name "zhenhua32"
          git add .
          git commit -m "init"

      - name: GitHub Push
        uses: ad-m/github-push-action@master
        with:
          github_token: ${{ secrets.ACCESS_TOKEN }}
          repository: "zhenhua32/zhenhua32.github.io"
          branch: master
          force: true
          directory: "./public"
```

基本的概念和通用的 CI CD 流程是相似的,

1. 通过 `jobs` 定义任务列表
2. 在每个 job 中通过 `on` 定义触发条件
3. 在 `steps` 定义运行的步骤

## 问题

在使用的过程中, 也遇到了一些问题.

### 推送到另一个仓库

因为我使用了两个仓库来构建 github page. 当前仓库是原始文本存储库, 每当写完一篇文章后
会使用 hugo 重新生成静态文件, 然后将静态文件提交到另一个仓库中.

这个过程中, 就需要将生成的代码推送到另一个仓库了.

遇到了两个问题:

- push 时提示没有权限
- directory 参数没有效果

Github Action 中有很多别人已经构建好的 action 可以使用, 这里使用了 `ad-m/github-push-action@master`.

一个问题是需要使用密钥才能访问另一个仓库, 所以不能直接使用 `${{ secrets.GITHUB_TOKEN }}`,
而是要用 [personal access token](https://github.com/settings/tokens)

生成完个人密钥后, 要将它添加到环境变量中, 就是添加到运行 action 的仓库中.
具体可以参考这个链接,
[为仓库创建加密密钥](https://docs.github.com/cn/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository)

注意环境变量名不能以`GITHUB_` 开头.

配置完成后, 就可以更新 `github_token` 参数了.

令人沮丧的是, 当时我配置完成后, 每次运行都提示没有权限访问另一个仓库.

```txt
Push to branch master
Missing input "github_token: ${{ secrets.GITHUB_TOKEN }}".
Error: Invalid exit code: 1
    at ChildProcess.<anonymous> (/home/runner/work/_actions/ad-m/github-push-action/master/start.js:29:21)
    at ChildProcess.emit (events.js:210:5)
    at maybeClose (internal/child_process.js:1021:16)
    at Process.ChildProcess._handle.onexit (internal/child_process.js:283:5) {
  code: 1
}
Error: Invalid exit code: 1
    at ChildProcess.<anonymous> (/home/runner/work/_actions/ad-m/github-push-action/master/start.js:29:21)
    at ChildProcess.emit (events.js:210:5)
    at maybeClose (internal/child_process.js:1021:16)
    at Process.ChildProcess._handle.onexit (internal/child_process.js:283:5)
```

后来, 终于在 issue 中翻到了问题根源. 原来是 `actions/checkout@v2` 的问题.
[actions/checkout@v2 的坑](https://github.com/ad-m/github-push-action/issues/44#issuecomment-581706892)

```yaml
- uses: actions/checkout@v2
    with:
    persist-credentials: false # otherwise, the token used is the GITHUB_TOKEN, instead of your personal token
    fetch-depth: 0 # otherwise, you will failed to push refs to dest repo
```

更新后, 就能运行成功了.

另一个问题是, 虽然设置了 `directory` 参数, 但是直接把当前仓库都推送过去了, 而不是推送了指定目录下的问价.

这个问题简单些, 就是没有在目录上初始化 git, 所以把上级目录的 git 仓库推送过去了.

在 push 步骤之前, 运行下初始化仓库就行.

```yml
- name: Commit
  run: |
    cd ./public
    git init
    git config --local user.email "zhenhua32@gmail.com"
    git config --local user.name "zhenhua32"
    git add .
    git commit -m "init"
```
