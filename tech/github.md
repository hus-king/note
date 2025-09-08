# Ubuntu配置github认证

## 一、解决网络问题

1. 安装 shadowsocks-rust
```bash
sudo snap install shadowsocks-rust
```
2. 配置服务
```bash
sudo systemctl edit snap.shadowsocks-rust.sslocal-daemon.service
```
在打开的编辑器中，输入以下内容:

```
[Service]
ExecStart=
ExecStart=/usr/bin/snap run shadowsocks-rust.sslocal-daemon -b "127.0.0.1:1080" --server-url "ss://aes-256-cfb:hesiqi668@49.51.249.199:8388"
```

3、启用并启动服务
```bash
sudo snap start --enable shadowsocks-rust.sslocal-daemon
sudo systemctl restart snap.shadowsocks-rust.sslocal-daemon.service
```

4、终端代理使用
```bash
export ALL_PROXY=socks5://127.0.0.1:1080
```

5、配置git
```bash
# 强制 git 使用 HTTPS 直连
git config --global --unset http.proxy
git config --global --unset https.proxy
```

## 二、配置GitHub CLI
使用 Snap 安装
```bash
sudo snap install gh
```

安装完成后，运行登录命令：
```bash
gh auth login
```

之后用gh替换git的默认认证方式
```bash
git config --global 'credential.https://github.com.helper' ''
git config --global --add 'credential.https://github.com.helper' '!gh auth git-credential'
```