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

# 失败, 替换为下面的 alibaba 镜像
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

### 初始化机器

```bash
# 临时关闭 swap
sudo swapoff -a

sudo sysctl net.bridge.bridge-nf-call-iptables=1
sudo sysctl net.bridge.bridge-nf-call-ip6tables=1

sudo systemctl stop firewalld
sudo systemctl disable firewalld

# 临时关闭 selinux
sudo setenforce 0
```

### 设置集群

首先必须寻找 gcr.io 里的镜像的国内加速版本.

```bash
# 获取配置文件
kubeadm config print init-defaults > init-config.yaml

# 修改其中的 imageRepository 为 registry.cn-hangzhou.aliyuncs.com/google_containers
# 修改其中的 localAPIEndpoint.advertiseAddress 为 0.0.0.0

# 预先下载镜像
kubeadm config images pull --config=init-config.yaml

# 在开始初始化之前, 必须先选择 POD 网络插件, 有些插件需要你 init 的时候传递响应的参数
# 这里使用 Weave Net, 无需特殊设置 init 参数

sudo kubeadm init --config=init-config.yaml

# 根据 init 里的提示操作
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# 假如 worker node
kubeadm join 10.0.1.12:6443 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:9c0c030d9e415e5b1cd1402d4018f0f0c5ce264b44882a3ff31e6fe55052e8e8

# 让 master 也作为 worker node
kubectl taint nodes --all node-role.kubernetes.io/master-

# 安装网络插件 这里使用 Weave Net
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"

# 验证 node status 为 ready 就行了
kubectl get nodes
kubectl get pods -n kube-system
```

### 加入集群

```bash
# 运行 master 集群上 kubeadm init 最后的提示
kubeadm join --token <token> <master-ip>:<master-port> --discovery-token-ca-cert-hash sha256:<hash>

# token 会在 24 小时候过期, 所以需要重新生成
kubeadm token list
kubeadm token create

# 获取 --discovery-token-ca-cert-hash
openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | \
   openssl dgst -sha256 -hex | sed 's/^.* //'
```

### 重置集群

```bash
# 重置器群, 如果发生了任何意想不到的情况
sudo kubeadm reset
sudo iptables -F && sudo iptables -t nat -F && sudo iptables -t mangle -F && sudo iptables -X
```

## 参考

[install-kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
