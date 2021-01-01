---
title: "部署 gitea"
date: 2020-12-31T23:58:29+08:00
draft: false
categories: ["Ops"]
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

        ssl_ciphers 'ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:ECDHE-ECDSA-DES-CBC3-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:DES-CBC3-SHA:!DSS';

        # 启用 session resumption 提高HTTPS性能
        # http://vincent.bernat.im/en/blog/2011-ssl-session-reuse-rfc5077.html
        ssl_session_cache shared:SSL:50m;
        ssl_session_timeout 1d;
        ssl_session_tickets off;

        # DHE密码器的Diffie-Hellman参数, 推荐 2048 位
        ssl_dhparam certs/aweffr.com/dhparam.pem;

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
