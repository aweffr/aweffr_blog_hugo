---
title: "延长ssh连接时间"
date: 2020-12-31T23:48:45+08:00
draft: false
categories: ["Ops"]
summary: "如何延长ssh云服务器的静默断开时间"
---

# Linux下，延长SSH的连接超时时间

修改配置文件: `vim /etc/ssh/sshd_config`

每60秒往客户端发送会话请求, 保持连接, 最多重试5次。

```bash
ClientAliveInterval 60
ClientAliveCountMax 5
```

生效方法:
```bash
systemctl status sshd && systemctl restart sshd
```
