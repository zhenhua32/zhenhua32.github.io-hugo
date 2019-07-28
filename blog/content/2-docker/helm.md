+++
title = "Helm"
date =  2019-07-28T11:45:49+08:00
weight = 2
+++

## Helm 简介

Helm 是 kubernetes 上的包管理器.

Helm Charts 帮助你定义, 安装, 升级在 kubernetes 上的应用.

## 安装

Helm 分为 client(helm) 和 server(Tiller).

### 安装 client

去 github 上的 [release 页面](https://github.com/helm/helm/releases) 上下载预编译的二进制文件.

解压之后放在 bin 目录下就行, linux 通常可选 `/usr/local/bin/helm`.
windows 就自己建个目录, 然后添加到环境变量 Path 中.

### 安装 server

```bash
# 直接安装会失败, 因为镜像下载不下来
helm init

# 使用 ali 的镜像
helm init --tiller-image=registry.cn-hangzhou.aliyuncs.com/google_containers/tiller:v2.14.2
helm init --upgrade --tiller-image=registry.cn-hangzhou.aliyuncs.com/google_containers/tiller:v2.14.2

# 检查安装结果
kubectl get pods --namespace kube-system
helm version
```

如果前面 `helm init` 失败的话, 使用下面的两种方式之一删除 helm init

```bash
kubectl delete deployment tiller-deploy --namespace kube-system
helm reset
```

## 使用

安装 Helm 主要是为了使用 draft, 所以暂时还没看文档.

## 参考

- [install helm](https://github.com/helm/helm/blob/master/docs/install.md)
- [k8s-for-docker-desktop](https://github.com/AliyunContainerService/k8s-for-docker-desktop)
