# 📋 Shadowsocks-Rust 服务端 Docker 部署清单

#### 1. 准备工作：创建配置目录和文件
首先，我们需要告诉服务端怎么运行（端口、密码、加密方式）喵。

```bash
# 创建配置目录
sudo mkdir -p /etc/shadowsocks-rust

# 创建并编辑配置文件
sudo nano /etc/shadowsocks-rust/config.json
```

在编辑器中填入以下内容（已根据你的要求预填好参数）：

```json
{
    "server": "0.0.0.0",
    "server_port": 58399,
    "password": "********",
    "method": "aes-256-cfb",
    "timeout": 300,
    "fast_open": true,
    "mode": "tcp_and_udp"
}
```
*操作提示：按 `Ctrl + O` 回车保存，然后 `Ctrl + X` 退出喵。*

---

#### 2. 启动 Docker 容器
使用以下一行命令启动服务。这条命令包含了**后台运行**、**开机自启**和**端口映射**喵。

```bash
docker run -d \
    --name ss-server \
    --restart always \
    -p 58399:58399/tcp \
    -p 58399:58399/udp \
    -v /etc/shadowsocks-rust/config.json:/etc/shadowsocks-rust/config.json \
    ghcr.io/shadowsocks/ssserver-rust:latest \
    ssserver -c /etc/shadowsocks-rust/config.json
```

*   `--restart always`: 确保服务器重启后自动恢复服务喵。
*   `-v ...`: 把刚才创建的配置文件挂载到容器里喵。

---

#### 3. 配置防火墙 (UFW)
如果不放行端口，外网是连不进来的喵。

```bash
# 放行 TCP 和 UDP 端口
sudo ufw allow 58399/tcp
sudo ufw allow 58399/udp

# 重载防火墙规则
sudo ufw reload
```

---

#### 4. 验证服务状态
检查容器是否正常运行，以及查看是否有报错日志喵。

```bash
# 查看容器运行状态 (应该看到 STATUS 为 Up)
docker ps | grep ss-server

# 查看实时日志 (确认没有 Error)
docker logs ss-server
```

---

### 💡 常用维护命令备忘

| 需求 | 命令 |
| :--- | :--- |
| **查看日志** | `docker logs ss-server` |
| **重启服务** | `docker restart ss-server` |
| **停止服务** | `docker stop ss-server` |
| **更新镜像** | `docker pull ghcr.io/shadowsocks/ssserver-rust:latest` 然后重启容器 |
| **查看自启状态** | `docker inspect ss-server \| grep RestartPolicy` |
