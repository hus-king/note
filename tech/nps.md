# 挂载nps内网穿透服务
你运行的是 **nPC 客户端**（配合 nPS 服务器使用的内网穿透工具），并且已经成功连接到服务器 `8.148.69.99:8024`，用于穿透本机的 SSH（22 端口）服务。

现在你想实现：**开机自动启动这个 npc 客户端**。

---

## ✅ 目标
让以下命令在 Jetson 开机时自动运行：

```bash
~/nps/npc -server=8.148.69.99:8024 -vkey=4e1gpbx9x966nup0 -type=tcp
```

---

## ✅ 推荐方法：使用 `systemd` 服务（Ubuntu/Linux 标准方式）

### 步骤 1：创建 systemd 服务文件

```bash
sudo nano /etc/systemd/system/npc.service
```

### 步骤 2：写入以下内容（根据你的路径和命令修改）

```ini
[Unit]
Description=NPC Client for NPS
After=network.target

[Service]
Type=simple
User=jetson
WorkingDirectory=/home/jetson/nps
ExecStart=/home/jetson/nps/npc -server=8.148.69.99:8024 -vkey=4e1gpbx9x966nup0 -type=tcp
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

> 🔍 注意事项：
> - `User=jetson`：替换为你的用户名（你当前是 `jetson`，正确）
> - `WorkingDirectory`：npc 和 conf 所在目录
> - `ExecStart`：完整命令，不要加 `sudo` 或 `~`

---

### 步骤 3：保存并启用服务

按 `Ctrl+O` → 回车（保存）→ `Ctrl+X`（退出 nano）

然后执行：

```bash
# 重载 systemd 配置
sudo systemctl daemon-reexec
sudo systemctl daemon-reload

# 启用开机自启
sudo systemctl enable npc.service

# 立即启动服务（测试）
sudo systemctl start npc.service

# 查看运行状态
sudo systemctl status npc.service
```

如果看到 `active (running)`，说明成功！

---

### 步骤 4：检查日志（如有问题）

```bash
sudo journalctl -u npc.service -f
```

可以实时查看日志输出，确认是否连接成功。

---

## ✅ 可选优化：使用配置文件（更规范）

你也可以把参数写进 `conf/npc.conf`，然后启动时指定配置文件。

### 示例 `conf/client.cfg`：

```ini
[common]
server_addr=8.148.69.99:8024
vkey=4e1gpbx9x966nup0
type=tcp
```

然后命令改为：

```bash
ExecStart=/home/jetson/nps/npc -config=conf/client.cfg
```

这样更清晰、安全（避免密钥暴露在命令行历史中）。

---

## ✅ 禁用自启（如需）

```bash
sudo systemctl disable npc.service
sudo systemctl stop npc.service
```

---

## ✅ 验证是否开机自启

重启测试：

```bash
sudo reboot
```

重启后等几十秒，运行：

```bash
systemctl status npc.service
```

如果显示 `active (running)`，说明自启成功 ✅

---

## 🔐 安全提醒

- `vkey` 是你的客户端密钥，请勿泄露。
- 建议使用配置文件 + 权限控制（`chmod 600 conf/client.cfg`）保护密钥。

---

如果你还希望穿透多个服务（比如 HTTP、VNC 等），也可以在配置文件中添加 `tcp` 映射，欢迎继续问我！

祝你内网穿透顺利！🚀