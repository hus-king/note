在 Ubuntu 上通过 VNC 实现**多个完全独立的虚拟桌面**，推荐使用 `TigerVNC`。它会为每个会话创建独立的 X Display，彼此隔离、不共享物理屏幕，且支持自定义分辨率和桌面环境。

以下为详细操作指南（适用于 Ubuntu 20.04/22.04/24.04）：

### 1. 安装必要软件
```bash
sudo apt update
sudo apt install tigervnc-standalone-server tigervnc-common xfce4 xfce4-goodies
```
> 💡 说明：Ubuntu 默认 GNOME 在 VNC 下兼容性较差且资源占用高，推荐轻量稳定的 `XFCE`。若需其他桌面可替换 `exec startxfce4`。

### 2. 设置 VNC 连接密码
```bash
vncpasswd
```
- 输入并确认密码（仅用于 VNC 客户端连接，与系统登录密码无关）
- 提示是否设置只读密码时按需选择 `n`

### 3. 配置会话启动脚本
首次运行会自动生成配置文件：
```bash
vncserver :1
vncserver -kill :1  # 先关闭，以便修改配置
```
编辑 `~/.vnc/xstartup`：
```bash
nano ~/.vnc/xstartup
```
替换为以下内容：
```sh
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
# 可选：设置默认语言/输入法环境变量
# export LANG=zh_CN.UTF-8

exec startxfce4
```
赋予执行权限：
```bash
chmod +x ~/./.vnc/xstartup
```

### 4. 启动多个独立桌面
每个 `:N` 对应一个独立会话，端口为 `5900 + N`：
```bash
# 启动 3 个独立桌面，指定分辨率（按需调整）
vncserver :1 -geometry 1920x1080
vncserver :2 -geometry 1920x1080
vncserver :3 -geometry 1366x768
# 允许远程连接（默认只监听 localhost，非本地客户端连不上）
vncserver :4 -geometry 1920x1080 -localhost no
```
- 查看运行状态：`vncserver -list`
- 查看 X11 socket 确认会话：`ls -l /tmp/.X11-unix/`
- 关闭指定会话：`vncserver -kill :2`
- 各会话完全隔离，拥有独立的窗口管理器、环境变量和进程树。

### 5. systemd 开机自启
配置 systemd 服务，让 VNC 会话在系统启动时自动运行。

创建 `~/.config/systemd/user/vncserver@.service`：
```bash
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/vncserver@.service
```
写入以下内容：
```ini
[Unit]
Description=Remote desktop VNC (TigerVNC) on %i
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/vncserver %i -geometry 1920x1080 -localhost no -fg
ExecStop=/usr/bin/vncserver -kill %i
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```
> 参数 `-fg` 让 vncserver 在前台运行，这是 systemd 服务所必需的。

启用并启动服务：
```bash
# 重新加载用户服务
systemctl --user daemon-reload

# 启动会话 :1
systemctl --user start vncserver@1

# 设置开机自启
systemctl --user enable vncserver@1

# 查看运行状态
systemctl --user status vncserver@1

# 如需多个会话，逐个 enable 即可
systemctl --user enable vncserver@2
```

> 注意：用户级 systemd 服务在用户登录后才会启动。如需在登录前自启，需使用系统级服务（`sudo systemctl enable`），配置路径为 `/etc/systemd/system/vncserver@.service`。

### 6. 防火墙放行
如果开启了 `ufw` 或其他防火墙，需要放行 VNC 端口（每个会话一个端口，`5900 + N`）：
```bash
# 放行单个会话 :1 → 5901
sudo ufw allow 5901/tcp

# 放行多个会话（按需添加）
sudo ufw allow 5902/tcp
sudo ufw allow 5903/tcp

# 或直接放行 5901-5910 范围
sudo ufw allow 5901:5910/tcp

# 查看防火墙状态确认
sudo ufw status
```

### 7. 客户端连接
使用 RealVNC Viewer、TigerVNC Viewer 或 Remmina：
- 地址格式：`<服务器IP>:5901`、`<服务器IP>:5902`...
- 输入第 2 步设置的 VNC 密码即可进入对应桌面。

#### SSH 隧道连接（更安全）
不开放防火墙端口，通过 SSH 隧道加密传输 VNC 流量：
```bash
# 将远程 5901 端口转发到本地 5901
ssh -L 5901:localhost:5901 <用户名>@<服务器IP>
```
保持此 SSH 会话不关闭，然后用 VNC 客户端连接 `localhost:5901`（或 `127.0.0.1:5901`）即可。

优点：全程加密、无需开放防火墙端口、适合不受信任的网络环境。