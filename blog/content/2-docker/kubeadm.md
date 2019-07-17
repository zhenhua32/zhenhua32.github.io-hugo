+++
title = "Kubeadm"
date =  2019-07-17T19:39:16+08:00
weight = 1
+++

## 腾讯云上使用 kubeadm

我在腾讯云上有台 2h8g 的机器, 平时就用来吃灰, 偶尔实践一下 linux 上的各种操作.
这次就来尝试 kubeadm 在腾讯云上安装 kubernetes.

因为腾讯云默认是 unbuntu 账户, 不是 root 账户, 所以基本所有命令都要加上 sudo.

### 安装 kubeadm 软件

```bash
sudo apt-get update && apt-get install -y apt-transport-https curl

# 失败
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
# 使用 alibaba 的镜像 https://opsx.alibaba.com/mirror?lang=zh-CN
curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | sudo apt-key add -

# 其实就是 将 deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
# 这句话写到文件 /etc/apt/sources.list.d/kubernetes.list 中
sudo bash -c 'cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
EOF'

sudo apt-get update

sudo apt-get install -y kubelet kubeadm kubectl

# 标记为不被自动更新
sudo apt-mark hold kubelet kubeadm kubectl
```

### 设置集群

首先必须寻找 gcr.io 里的镜像的国内加速版本.

## 参考

[install-kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
