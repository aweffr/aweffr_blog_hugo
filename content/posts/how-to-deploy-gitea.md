---
title: "部署 gitea 记录"
date: 2020-12-31T23:58:29+08:00
draft: false
categories: ["ops"]
summary: "在 git.aweffr.com 上部署一个私有git服务器的操作记录"
---

安装git
```bash
apt-get install git
```

添加git用户
```bash
adduser git
sudo usermod -aG sudo git
```

添加gitea的目录结构
```bash
cd ~
sudo mkdir -p /var/lib/gitea/{custom,data,indexers,public,log}
sudo chown git:git /var/lib/gitea/{data,indexers,log}
sudo chmod 750 /var/lib/gitea/{data,indexers,log}
sudo mkdir /etc/gitea
sudo chown root:git /etc/gitea
sudo chmod 770 /etc/gitea
```

下载gitea
```bash
sudo wget -O gitea https://dl.gitea.io/gitea/1.13.1/gitea-1.13.1-linux-amd64
sudo chmod +x gitea
sudo cp gitea /usr/local/bin/gitea
```

配置nginx, 预期gitea进程在9000端口启动
```nginx
# /etc/nginx/sites-enabled/git.aweffr.com

server {
        listen        80;
        server_name   git.aweffr.com;
        return 302    https://$host$request_uri;
}


# Default server configuration
server {
  server_name            git.aweffr.com;

  # SSL configuration
  listen                  443 ssl;
  ssl_certificate         certs/aweffr.com/fullchain;
  ssl_certificate_key     certs/aweffr.com/key;
  ssl_trusted_certificate certs/aweffr.com/fullchain;

  ssl_protocols TLSv1.2 TLSv1.3;
  ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
  ssl_prefer_server_ciphers off;

  ssl_session_timeout 1d;
  ssl_session_cache shared:MozSSL:10m;  # about 40000 sessions
  ssl_session_tickets off;

  # HSTS (ngx_http_headers_module is required) (63072000 seconds)
  add_header Strict-Transport-Security "max-age=63072000" always;

  # DHE密码器的Diffie-Hellman参数
  ssl_dhparam certs/aweffr.com/dhparam.pem;

  # OCSP Stapling
  ssl_stapling           on;
  ssl_stapling_verify    on;
  resolver               1.1.1.1 1.0.0.1 8.8.8.8 8.8.4.4 208.67.222.222 208.67.220.220 valid=60s;
  resolver_timeout       3s;

  location / {
    proxy_set_header  X-Real-IP  $remote_addr;
    proxy_pass http://localhost:9000;
  }
}
```

配置项速查表看[gitea config cheat sheet](https://docs.gitea.io/en-us/config-cheat-sheet/#server-server)

启动
```bash
gitea web -p 9000 --custom-path /var/lib/gitea/custom --work-path /var/lib/gitea --config /var/lib/gitea/custom/conf/app.ini
```

第一次启动要配置数据库等，生成的app.ini在 `/var/lib/gitea/custom/conf/app.ini`

启动命令行中无法让gitea进程只绑定127.0.0.1, 需要修改配置。

修改其中的server部分:
```bash
[server]
LOCAL_ROOT_URL   = http://localhost:9000/
SSH_DOMAIN       = git.aweffr.com
DOMAIN           = git.aweffr.com
HTTP_ADDR        = 127.0.0.1
HTTP_PORT        = 9000
ROOT_URL         = https://git.aweffr.com/
DISABLE_SSH      = false
SSH_PORT         = 22
```
