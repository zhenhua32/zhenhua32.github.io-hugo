+++
title = "Gitlab"
date =  2019-07-29T20:42:29+08:00
weight = 2
+++

## 简介

gitlab 不仅是一个 git 代码托管平台, 更是 DevOps 平台.
这点是我最喜欢的, 所以迫切想要实践一下.

## 安装

对我而言, 主要有两种安装方式: [docker](https://docs.gitlab.com/omnibus/docker/)
和 [kubernetes](https://docs.gitlab.com/charts/).

当然, 装完主体之后, 还需要安装 [gitlab runner](https://docs.gitlab.com/runner/install/).

**TODO: 经过我一段时间的摸索之后, 还是有点问题**

以下的安装方式都是基于 docker-compose 的

### 安装 gitlab 主体

首先, 安装之前, 我们需要确定以下几点.

- 确定 external_url, 这个是用户可以访问的外部链接, 参考
  [这个链接](https://docs.gitlab.com/omnibus/settings/configuration.html#configuring-the-external-url-for-gitlab)
- 是否使用内置的 nginx, 如果使用外部的 nginx, 可以参考
  [这个链接](https://docs.gitlab.com/omnibus/settings/nginx.html#using-a-non-bundled-web-server)
- 是否使用 HTTPS, 参考 [这个链接](https://docs.gitlab.com/omnibus/settings/nginx.html#enable-https)

这其中的几点对我来说非常致命, 因为我手头没有备案的域名, 所以我在腾讯云上部署就非常蛋疼.

如果你只是想要一个 ip 地址显示的 gitlab, 那么还是挺容易的.

```yaml
# docker-compose.yml
version: "3.7"

services:
  gitlab:
    image: "gitlab/gitlab-ce:12.1.1-ce.0"
    restart: "no"
    hostname: "gitlab"
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://x.x.x.x:3080'
        # nginx['enable'] = false
        gitlab_rails['gitlab_shell_ssh_port'] = 3022
        web_server['external_users'] = ['nginx', 'www-data']
        # Add any other gitlab.rb configuration here, each on its own line
    ports:
      - "3080:80"
      # - '3043:443'
      - "3022:22"
    volumes:
      # - "/srv/gitlab/data/gitlab-workhorse:/var/opt/gitlab/gitlab-workhorse"
      - "/srv/gitlab/config:/etc/gitlab"
      - "/srv/gitlab/logs:/var/log/gitlab"
      - "/srv/gitlab/data:/var/opt/gitlab"
    networks:
      - git_net

networks:
  git_net:
    name: git_net
```

简单介绍一下, 上面这个 docker-compose.yml 只有一个叫做 gitlab 的服务,
要修改的是里面的 **external_url**, 将它修改为自己的 ip 地址加映射的主机端口就行了,
上面文件中映射到了 3080 端口.

同时, 也将数据都保存在了本机的 `/srv/gitlab` 目录中. 分别是配置文件, 日志和内部数据.
主配置文件叫做 `gitlab.rb`, 官方的配置文档请看
[这个链接](https://docs.gitlab.com/omnibus/settings/configuration.html#enable-https).

然后, 你就能访问了.

### 启用 HTTPS

要使用 HTTPS, 文档中介绍了两种方式, 自动的和手动的.

自动的方式使用了 Let's Encrypt, 可以参考
[这个链接](https://docs.gitlab.com/omnibus/settings/ssl.html#lets-encrypthttpsletsencryptorg-integration).

手动的方式是要复制证书到指定的位置.

两种方式都要修改的一个选项是 `external_url`, 将域名设置为 https 开头的就行了.

当然, 在国内, 如果你的域名没有备案过, letsencrypt 的验证会失败. 因为验证被拦截了.

### 使用外部 nginx

如果要使用内部的服务器, 先启用配置中的 `nginx['enable'] = false`.

然后是创建 nginx 的配置文件. 我对这一块不太熟, 反正我创建出来的网站有点问题.

有两个地方可以参考
[1](https://gitlab.com/gitlab-org/gitlab-recipes/blob/master/web-server/nginx/gitlab-omnibus-ssl-nginx.conf)
和
[2](https://gitlab.com/gitlab-org/gitlab-ce/blob/master/lib/support/nginx/gitlab-ssl).

在使用外部 nginx 之后, 容器暴露出的 80 就会没有用.

```nginx
## GitLab
##
## Modified from nginx http version
## Modified from http://blog.phusion.nl/2012/04/21/tutorial-setting-up-gitlab-on-debian-6/
## Modified from https://raymii.org/s/tutorials/Strong_SSL_Security_On_nginx.html
##
## Lines starting with two hashes (##) are comments with information.
## Lines starting with one hash (#) are configuration parameters that can be uncommented.
##
##################################
##        CONTRIBUTING          ##
##################################
##
## If you change this file in a Merge Request, please also create
## a Merge Request on https://gitlab.com/gitlab-org/omnibus-gitlab/merge_requests
##
###################################
##         configuration         ##
###################################
##
## See installation.md#using-https for additional HTTPS configuration details.

upstream gitlab-workhorse {
  # GitLab socket file,
  # for Omnibus this would be: unix:/var/opt/gitlab/gitlab-workhorse/socket
  server unix:/srv/gitlab/data/gitlab-workhorse/socket fail_timeout=0;
}

map $http_upgrade $connection_upgrade_gitlab_ssl {
  default upgrade;
  ''      close;
}


## NGINX 'combined' log format with filtered query strings
log_format gitlab_ssl_access $remote_addr - $remote_user [$time_local] "$request_method $gitlab_ssl_filtered_request_uri $server_protocol" $status $body_bytes_sent "$gitlab_ssl_filtered_http_referer" "$http_user_agent";

## Remove private_token from the request URI
# In:  /foo?private_token=unfiltered&authenticity_token=unfiltered&feed_token=unfiltered&...
# Out: /foo?private_token=[FILTERED]&authenticity_token=unfiltered&feed_token=unfiltered&...
map $request_uri $gitlab_ssl_temp_request_uri_1 {
  default $request_uri;
  ~(?i)^(?<start>.*)(?<temp>[\?&]private[\-_]token)=[^&]*(?<rest>.*)$ "$start$temp=[FILTERED]$rest";
}

## Remove authenticity_token from the request URI
# In:  /foo?private_token=[FILTERED]&authenticity_token=unfiltered&feed_token=unfiltered&...
# Out: /foo?private_token=[FILTERED]&authenticity_token=[FILTERED]&feed_token=unfiltered&...
map $gitlab_ssl_temp_request_uri_1 $gitlab_ssl_temp_request_uri_2 {
  default $gitlab_ssl_temp_request_uri_1;
  ~(?i)^(?<start>.*)(?<temp>[\?&]authenticity[\-_]token)=[^&]*(?<rest>.*)$ "$start$temp=[FILTERED]$rest";
}

## Remove feed_token from the request URI
# In:  /foo?private_token=[FILTERED]&authenticity_token=[FILTERED]&feed_token=unfiltered&...
# Out: /foo?private_token=[FILTERED]&authenticity_token=[FILTERED]&feed_token=[FILTERED]&...
map $gitlab_ssl_temp_request_uri_2 $gitlab_ssl_filtered_request_uri {
  default $gitlab_ssl_temp_request_uri_2;
  ~(?i)^(?<start>.*)(?<temp>[\?&]feed[\-_]token)=[^&]*(?<rest>.*)$ "$start$temp=[FILTERED]$rest";
}

## A version of the referer without the query string
map $http_referer $gitlab_ssl_filtered_http_referer {
  default $http_referer;
  ~^(?<temp>.*)\? $temp;
}


## Redirects all HTTP traffic to the HTTPS host
server {
  ## Either remove "default_server" from the listen line below,
  ## or delete the /etc/nginx/sites-enabled/default file. This will cause gitlab
  ## to be served if you visit any address that your server responds to, eg.
  ## the ip address of the server (http://x.x.x.x/)
  listen 0.0.0.0:80;
  listen [::]:80 ipv6only=on;
  server_name blog.iftodo.com; ## Replace this with something like gitlab.example.com
  server_tokens off; ## Don't show the nginx version number, a security best practice
  return 301 https://$http_host$request_uri;
  access_log  /var/log/nginx/gitlab_access.log gitlab_ssl_access;
  error_log   /var/log/nginx/gitlab_error.log;
}

## HTTPS host
server {
  listen 0.0.0.0:443 ssl;
  listen [::]:443 ipv6only=on ssl http2;
  server_name blog.iftodo.com; ## Replace this with something like gitlab.example.com
  server_tokens off; ## Don't show the nginx version number, a security best practice

  ## Strong SSL Security
  ## https://raymii.org/s/tutorials/Strong_SSL_Security_On_nginx.html & https://cipherli.st/
  ssl on;
  ssl_certificate /etc/letsencrypt/live/blog.iftodo.com/fullchain.pem; # managed by Certbot
  ssl_certificate_key /etc/letsencrypt/live/blog.iftodo.com/privkey.pem; # managed by Certbot
  # include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
  ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

  # GitLab needs backwards compatible ciphers to retain compatibility with Java IDEs
  ssl_ciphers "ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA:ECDHE-RSA-AES128-SHA:ECDHE-RSA-DES-CBC3-SHA:AES256-GCM-SHA384:AES128-GCM-SHA256:AES256-SHA256:AES128-SHA256:AES256-SHA:AES128-SHA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!MD5:!PSK:!RC4";
  ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
  ssl_prefer_server_ciphers on;
  ssl_session_cache shared:SSL:10m;
  ssl_session_timeout 5m;

  ## See app/controllers/application_controller.rb for headers set

  ## [Optional] If your certficate has OCSP, enable OCSP stapling to reduce the overhead and latency of running SSL.
  ## Replace with your ssl_trusted_certificate. For more info see:
  ## - https://medium.com/devops-programming/4445f4862461
  ## - https://www.ruby-forum.com/topic/4419319
  ## - https://www.digitalocean.com/community/tutorials/how-to-configure-ocsp-stapling-on-apache-and-nginx
  # ssl_stapling on;
  # ssl_stapling_verify on;
  # ssl_trusted_certificate /etc/nginx/ssl/stapling.trusted.crt;
  # resolver 208.67.222.222 208.67.222.220 valid=300s; # Can change to your DNS resolver if desired
  # resolver_timeout 5s;

  ## [Optional] Generate a stronger DHE parameter:
  ##   sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 4096
  ##
  # ssl_dhparam /etc/ssl/certs/dhparam.pem;

  ## [Optional] Enable HTTP Strict Transport Security
  # add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

  ## Real IP Module Config
  ## http://nginx.org/en/docs/http/ngx_http_realip_module.html
  real_ip_header X-Real-IP; ## X-Real-IP or X-Forwarded-For or proxy_protocol
  real_ip_recursive off;    ## If you enable 'on'
  ## If you have a trusted IP address, uncomment it and set it
  # set_real_ip_from YOUR_TRUSTED_ADDRESS; ## Replace this with something like 192.168.1.0/24

  ## Individual nginx logs for this GitLab vhost
  access_log  /var/log/nginx/gitlab_access.log gitlab_ssl_access;
  error_log   /var/log/nginx/gitlab_error.log;

  location / {
    client_max_body_size 0;
    gzip off;

    ## https://github.com/gitlabhq/gitlabhq/issues/694
    ## Some requests take more than 30 seconds.
    proxy_read_timeout      300;
    proxy_connect_timeout   300;
    # proxy_redirect          off;

    proxy_http_version 1.1;

    proxy_set_header    Host                $http_host;
    proxy_set_header    X-Real-IP           $remote_addr;
    proxy_set_header    X-Forwarded-Ssl     on;
    proxy_set_header    X-Forwarded-For     $proxy_add_x_forwarded_for;
    proxy_set_header    X-Forwarded-Proto   $scheme;
    proxy_set_header    Upgrade             $http_upgrade;
    proxy_set_header    Connection          $connection_upgrade_gitlab_ssl;

    proxy_pass http://gitlab-workhorse;
  }

  error_page 404 /404.html;
  error_page 422 /422.html;
  error_page 500 /500.html;
  error_page 502 /502.html;
  error_page 503 /503.html;
  location ~ ^/(404|422|500|502|503)\.html$ {
    # Location to the GitLab's public directory,
    # for Omnibus this would be: /opt/gitlab/embedded/service/gitlab-rails/public
    root /home/git/gitlab/public;
    internal;
  }
}
```

我这里使用的是 2 中的文件, 主要修改的地方是:

- server_name 替换为自己的域名
- access_log 的位置
- error_log 的位置
- upstream gitlab-workhorse 中 server 的位置, 容器内是在 /var/opt/gitlab/gitlab-workhorse
- 注释掉了 proxy_redirect

其实, 我觉得这个不太对, 需要修改, 做个精简版出来.

### 自己的困惑

我这边遇到的问题呢, 有以下几点.

因为是基于 docker 安装的, 所以要使用域名, 外部必须有 nginx.
因为内部的 nginx 在 `external_url` 被设置为 https 之后会自动启用 letsencrypt.
除非使用这个设置 `letsencrypt['enable'] = false`.
简单来说, 使用外部 nginx 了, 内部就不用再开了, 跳转两次也挺浪费的.
然后, 未备案的域名会被劫持, 所以必须在外部启用 HTTPS.

一顿操作之后, 我们发现网站虽然建立起来了, 但总是有几个请求会失败.
常见的失败请求有

- https://blog.iftodo.com/root/aa/refs/master/logs_tree/?format=js
- https://blog.iftodo.com/root/aa/commits/master/signatures

常见的错误是 `An error occurred while loading commit signatures`.

这让我非常痛苦, 如果直接使用域名访问, 却没有问题.

### 安装 runner

对我来说, 安装 gitlab 的主要目的是想使用它内置的 CI&CD.
所以, 必须安装 runner.

首先, 登录自己的 gitlab 网站, 第一次是修改管理员的密码, 管理员的名字是 root.
登录之后, 在 https://blog.iftodo.com/admin/runners 里找到加入 runner 的必要参数.

分别是

- URL
- registration token

runner 的官方文档是 [https://docs.gitlab.com/runner/](https://docs.gitlab.com/runner/).

在 runner 启动之前必须在先配置一番, 因为我这里使用的是 docker-compose,
所以安装文档看的是 docker 安装方式.

要配置 runner 和 gitlab 的链接, 使用的命令是 `sudo gitlab-runner register`.

你可以直接在 docker 容器内使用上面的命令相互式运行并生产文件, 然后复制到外部.
这里, 为了方便, 我选择使用非交互式的一步完成, 命令有点长, 不过写在文件中却还行.

```yaml
# docker-compose.yml
version: "3.7"

services:
  runner:
    image: "gitlab/gitlab-runner:latest"
    restart: "no"
    depends_on:
      - gitlab
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
      - "./gitlab/ruuner:/etc/gitlab-runner"
    # extra_hosts:
    #   - 'gitlab:172.25.0.2'
    networks:
      - git_net

  # run before runner to get config, gitlab must have start
  runner-config:
    image: "gitlab/gitlab-runner:latest"
    restart: "no"
    command: |
      register
      --non-interactive
      --url="http://gitlab"
      --registration-token="TsBj3wds5uiteVYZUmXF"
      --executor="docker"
      --docker-image="alpine:latest"
      --docker-privileged="true"
      --docker-pull-policy="if-not-present"
      --docker-network-mode="git_net"
      --description="docker-runner"
      --tag-list="docker"
      --run-untagged="true"
      --locked="false"
      --access-level="not_protected"
    volumes:
      - "./gitlab/ruuner:/etc/gitlab-runner"
    networks:
      - git_net

networks:
  git_net:
    name: git_net
```

这个文件和安装 gitlab 时的配置文件是同一个, 为了简单, 省略了 gitlab 的部分,
自行合起来吧.

首先, 在自建的 gitlab 网站获取 URL 和 registration token 之后, 替换掉文件中
`--url "http://gitlab"` 和 `--registration-token="TsBj3wds5uiteVYZUmXF"`.
`--url "http://gitlab"` 其实不用改, 因为可以靠 docker-compose 的子网通讯.

然后, 运行 `docker-compose run runner-config`, 这样配置文件就保留到主机了.
需要注意的一点是, 多次运行这个命令后, 配置文件会整合起来, 这样就会在配置文件中
生成多个 runner 了. 所以, 建议最好在运行之前删除 `./gitlab/ruuner` 目录.

生成配置文件之后, 就可以使用开启 runner 服务了, `docker-compose up -d runner`.

## 配置文件

{{% attachments title="配置文件" /%}}
