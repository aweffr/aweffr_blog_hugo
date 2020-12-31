---
title: "操作记录: acme.sh + nginx 实现 https + 自动续期"
date: 2021-01-01T00:02:04+08:00
draft: false
categories: ["Ops"]
summary: "acme.sh + nginx 快速参考"
---

先配好DNS，本文以本站 aweffr.com 为例。

1. 安装

网络情况好的情况下
```bash
# 最新版
curl https://get.acme.sh | sh
```

网络不好时[下载](/assets/acme.sh-2.8.8.tar.gz)
```bash
tar zxvf acme.sh-2.8.8.tar.gz && cd acme.sh-2.8.8 && ./acme.sh --install
```

安装好后acme的程序和后续配置，证书都在`~/.acme.sh`

安装nginx
```bash
sudo apt install nginx-full
```

创建用于nginx访问let's encrypt challenge的目录
```bash
mkdir -p /var/www/le_root/.well-known/acme-challenge
chown -R root:www-data /var/www/le_root
```

创建文件 `/etc/nginx/includes/letsencrypt-webroot`
```nginx
# /etc/nginx/includes/letsencrypt-webroot

location /.well-known/acme-challenge/ {
    alias /var/www/le_root/.well-known/acme-challenge/;
}
```

然后 `vim /etc/nginx/sites-enabled/default`

```nginx
# /etc/nginx/sites-enabled/default

server {
    listen 80;
    server_name aweffr.com;

    # ....

    # Let's Encrypt webroot
    include includes/letsencrypt-webroot;
}
```

重启 nginx 生效 `systemctl reload nginx.service`

然后签发证书

```bash
acme.sh --issue -d aweffr.com -d www.aweffr.com -d git.aweffr.com -w /var/www/le_root --keylength ec-256

# ...
# [Fri 01 Jan 2021 12:21:40 AM CST] Cert success.
# [Fri 01 Jan 2021 12:21:40 AM CST] Your cert is in  /root/.acme.sh/aweffr.com/aweffr.com.cer
# [Fri 01 Jan 2021 12:21:40 AM CST] Your cert key is in  /root/.acme.sh/aweffr.com/aweffr.com.key
# [Fri 01 Jan 2021 12:21:40 AM CST] The intermediate CA cert is in  /root/.acme.sh/aweffr.com/ca.cer
# [Fri 01 Jan 2021 12:21:40 AM CST] And the full chain certs is there:  /root/.acme.sh/aweffr.com/fullchain.cer
```
实际签发就是 aweffr.com 一张证书，里面dns记录包含aweffr.com, www.aweffr.com, git.aweffr.com。

然后告诉acme.sh如何install这个cert，它就会定时拷贝文件到/etc/nginx目录, 并自动reload nginx。
```bash
mkdir -p /etc/nginx/certs/aweffr.com
acme.sh --install-cert --ecc -d aweffr.com --cert-file /etc/nginx/certs/aweffr.com/cert --key-file /etc/nginx/certs/aweffr.com/key --fullchain-file /etc/nginx/certs/aweffr.com/fullchain --reloadcmd "systemctl reload nginx.service"
```

生成 dbparam:
```bash
openssl dhparam -dsaparam -out /etc/nginx/certs/aweffr.com/dhparam.pem 4096
```

最后往nginx的site里添加ssl配置
```nginx
server {
    ...
    
	# SSL configuration
	#
	listen 443 ssl;
    ssl_certificate         certs/aweffr.com/fullchain;
    ssl_certificate_key     certs/aweffr.com/key;
    ssl_trusted_certificate certs/aweffr.com/fullchain;

    ssl_ciphers 'ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:ECDHE-ECDSA-DES-CBC3-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:DES-CBC3-SHA:!DSS';

    # 启用 session resumption 提高HTTPS性能
    # http://vincent.bernat.im/en/blog/2011-ssl-session-reuse-rfc5077.html
    ssl_session_cache shared:SSL:50m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # DHE密码器的Diffie-Hellman参数
    ssl_dhparam certs/aweffr.com/dhparam.pem;
    
    ...
}
```

参考链接
1. [https://www.rmedgar.com/blog/using-acme-sh-with-nginx](https://www.rmedgar.com/blog/using-acme-sh-with-nginx)



