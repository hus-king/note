# 部署 Overleaf 服务器（2025）

## 目录

1. 前提说明

2. Prerequisite（前置要求）

3. 测试日志(2025.09.19)

4. 团队部署建议

5. 安装

6. 安装完整的 texlive

7. 此处遇到的问题（2025.03.27）

8. 登录

9. 用户管理

10. 可能有用的 docker 命令

11. 卸载服务

## 一、前提说明

如果你只有一台电脑，我不建议你部署 Overleaf，老老实实去用 TexLive. 如果你有两台电脑或者有云服务器，我强烈推荐.

Overleaf 有 Community Edition 、 Server Pro 两种，我们用免费的社区版

官方文档地址：[https://github.com/overleaf/toolkit/blob/master/doc/quick-start-guide.md](https://github.com/overleaf/toolkit/blob/master/doc/quick-start-guide.md)

chatGPT 是一个好帮手

## 二、Prerequisite（前置要求）

### 服务器硬件要求

- 内存越多越好，最少4g

- 硬盘空间，越多越好，最少 15g 空闲空间

- 服务器的内存都很贵，你可以用硬盘当虚拟内存，变相扩展内存

### 软件与环境要求

- docker 需要提前安装

- 演示使用的版本：docker 27.3.1

- 保证网络可以正常拉取 docker 镜像和 github 仓库，或者有等价的替代方案

- 会基本的 linux 和 docker 操作

这四项搞不定，不必往下看，浪费时间.

## 三、测试日志(2025.09.19)

这里很无聊，可以直接跳过不看
本文首发于 2024年.

2025.05.19 进行了第五次测试安装.

一切正常，同时对文章进行了细微调整.

测试编译了 《Attention Is All You Need》，几乎是秒编译

arXiv 地址：[https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)

## 四、团队部署建议

个人用户，这部分直接跳过，这是给有团队部署需求的人看的
我并非专业的运维，这里只是一点点建议

### 预算底线

overleaf团队价格，每人每年233刀

你们的预算，不应该超过这个，除非是为了数据安全考虑

### 硬件资源

- 每个人最少应该分配一个 cpu 核心，1GB内存，1-2G存储

- overleaf 本体运行，最少应该2cpu核心，4GB+内存

- 编译应该需要一些硬盘空间当缓存，最起码每三个人再多加5g的空闲空间，用于缓存

### 内网部署 VS 云服务器

国内服务器贵的就是带宽，流量，电费

根据团队人数评估一下，你们需要硬件资源

评估装机的钱和每月电费

再去看云服务厂商提供的同等机型的每月租金(云服务器，有不带，带宽的机型)

假设你们有运维能力，就是使用上没问题(如果有，这一项也得考虑)

综合下来你们觉得可行，那就内网装机，如果不行那就云服务器

内网部署，最大的成本是电费

云服务器，最大的成本是流量

公网访问，先用那个流量计费(带宽可以拉满到100MB大小，但只根据流量来收费)

用户少的情况下，一般这个是最划算的

跑一到三个月，看一下你们每个月开销到底有多少

根据开销再作调整

## 五、安装

### 下载 overleaf-toolkit

overleaf-toolkit 是官方提供的服务器搭建项目，简单易用

```bash

git clone --depth=1 https://github.com/overleaf/toolkit.git ./overleaf-toolkit && cd ./overleaf-toolkit
```

overleaf-toolkit 目录下，你只需要关注三个地方

- doc 目录下是更详细的文档，几乎所有问题，都可以在这里找到答案.

- config 目录用于配置项目

- bin 目录，存放一些命令

**NB**：随着版本更迭，这个博客的内容可能会失效，所以一定要浏览官方文档
最好，先用虚拟机测试搭建

### 生成配置文件

```bash

# 运行命令，生成配置文件
bin/init

# 检查
bin/doctor

# 此时，会在 config 目录下生成三个文件
# 一般情况下，我们只需要更改 overleaf.rc 就行了
overleaf.rc  variables.env  version
```

### 修改配置

```bash

# 配置文件 overleaf.rc 根据你的需求修改

# 主机数据文件夹，存放数据，用于持久化
OVERLEAF_DATA_PATH=/home/hall/apps/overleaf/data

# 0.0.0.0 表示接受来自任意 ip 的访问
OVERLEAF_LISTEN_IP=0.0.0.0

# 服务端口
OVERLEAF_PORT=5207
```

其余的文件都不需要改动

### 防火墙

把该放开的端口都放开

### 启动

bin/up 是对 docker-compose 命令的封装，它俩的用法是一样的

```bash

bin/up -d # 后台运行
bin/docker-compose -d
bin/up # 临时启动
```

它会创建三个容器，一个 docker 网络

```bash

docker ps -a
CONTAINER ID   IMAGE                         COMMAND                  CREATED          STATUS                   PORTS                  NAMES
13a5d9a62ffd   sharelatex/sharelatex:5.2.1   "/sbin/my_init"          32 minutes ago   Up 7 minutes             0.0.0.0:5207->80/tcp   sharelatex
56b2f2e95ad1   redis:6.2                     "docker-entrypoint.s…"   32 minutes ago   Up 8 minutes             6379/tcp               redis
93fe60ddccee   mongo:6.0                     "docker-entrypoint.s…"   33 minutes ago   Up 8 minutes (healthy)   27017/tcp              mongo

docker network ls
NETWORK ID     NAME               DRIVER    SCOPE
4f1fdade7e94   bridge             bridge    local
d147463e297d   host               host      local
343b1468a006   none               null      local
4a117aceb573   overleaf_default   bridge    local
```

## 六、安装完整的 texlive

这一步，可能会花费大量的时间，请耐心等待
社区版使用的 texlive 是最小安装的 texlive ，我们需要将其升级到完整版。

在这里找一个 CTAN 镜像源：[https://ctan.org/mirrors/](https://ctan.org/mirrors/)

选一个你认为最快的，同时能用的源

```bash

# 进入容器
bin/shell
# 查看版本
tlmgr --version
# 更换镜像源，我用腾讯云的镜像
tlmgr option repository http://mirrors.cloud.tencent.com/CTAN/systems/texlive/tlnet
# 查看
tlmgr option show repository
# 先更新
tlmgr update --self --all 

# 安装完整的包，可能要花挺长一段时间，尽量选速度快的源
tlmgr install scheme-full

# 重启容器
bin/stop 
bin/start
```

如果出现问题，先排查网络

```bash

# 假如你用的是 mirrors.tuna.tsinghua.edu.cn
curl -I https://mirrors.tuna.tsinghua.edu.cn
# 响应结果中 200 是正常的
```

```text

HTTP/2 200 
server: nginx/1.22.1
date: Thu, 18 Sep 2025 17:36:25 GMT
content-type: text/html
content-length: 22350
last-modified: Tue, 09 Sep 2025 11:34:49 GMT
vary: Accept-Encoding
etag: "68c010d9-574e"
strict-transport-security: max-age=31536000
x-tuna-mirror-id: neomirrors
accept-ranges: bytes
```

## 七、此处遇到的问题（2025.03.27）

2025.05.04 overleaf 已经将容器更新到 2025 ，此处 bug 暂时消除，但我想明年，这里应该还会有 bug.

远程仓库是2025年的版本，容器里的texlive是2024年的

```text

tlmgr update --self --all

tlmgr: Local TeX Live (2024) is older than remote repository (2025).
Cross release updates are only supported with
  update-tlmgr-latest(.sh/.exe) --update
See https://tug.org/texlive/upgrade.html for details.
```

升级 tlmgr 就可以了

```bash

# 进入容器
cd ~

# 在你选择的镜像站里，找到升级脚本
wget http://mirrors.cloud.tencent.com/CTAN/systems/texlive/tlnet/update-tlmgr-latest.sh

chmod +x update-tlmgr-latest.sh
./update update-tlmgr-latest.sh
```

## 八、登录

先访问 http://ip:port/launchpad 创建管理员 再访问 http://ip:port/login 登录

```text

# 比如
http://111.211.66.77:5207/launchpad
http://111.211.66.77:5207/login
```

没启用 https ，因为仅仅只是自己一个人用，也可以再折腾折腾，启用 https

## 九、用户管理

第一次登录，会提示你注册管理员账号.

用户管理面板链接，类似下面这样

```text

http://111.211.66.77:5207/admin/register
```

输入注册用户的邮箱，点击注册，就会弹出一个设置密码的链接.

把链接修改成下面这样，就可以让用户访问设置了.

```text

http://111.211.66.77:5207/user/activate?token=dd561853aed8b32b5118f38689ff247b3f25741ec9f997bdb15c11c40c4ccb7d&user_id=6778b95d389ef2099e34f319
```

这样用户账号，就注册完毕了.

## 十、可能有用的 docker 命令

```bash

docker stop $(docker ps -q)
docker network ls
docker system prune -a --volumes
# 清理构建缓存
docker builder prune 
rm -rf /home/hall/apps/overleaf/data
```

## 十一、卸载服务

卸载 overleaf 服务

```bash

bin/stop 
# 所有不使用的 dangling 资源都会被删除，谨慎操作
docker system prune -a --volumes 
# 清理构建缓存
docker builder prune
```




> （注：文档部分内容可能由 AI 生成）