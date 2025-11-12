# Tailscale 自建 DERP 节点部署指南

### ✅ 部署步骤（最小化流程）

#### 1. 安装 Tailscale 客户端（用于身份校验）

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# 按提示完成浏览器登录授权，确保该服务器加入你的 Tailnet
```

> 🔑 必须完成 `tailscale up` 并在线，否则后续无法校验客户端合法性。

---

#### 2. 创建 `docker-compose.yml`

```yaml
services:
  derper:
    image: ghcr.nju.edu.cn/yangchuansheng/ip_derper:latest
    container_name: derper
    restart: always
    ports:
      - "12345:12345" # 这里的12345请改成你自己想要的10000以上的高位端口
      - "3478:3478/udp" # 3478 为stun端口，如果不冲突请勿修改
    volumes:
      - /var/run/tailscale/tailscaled.sock:/var/run/tailscale/tailscaled.sock # 映射本地 tailscale 客户端验证连接，用来验证是否被偷
    environment:
      - DERP_ADDR=:12345 # 此处需要与上面的同步修改
      - DERP_CERTS=/app/certs
      - DERP_VERIFY_CLIENTS=true # 启动客户端验证，这是防偷的最重要的参数
```

> ✅ 端口 `12345` 可按需替换为任意高位端口（如 `30000`, `45678`）  
> ✅ 推荐使用 `ghcr.nju.edu.cn` 镜像源（国内加速）
> ⚠️ 端口不能与之前的重复，不能都是12345

---

#### 3. 启动服务

```bash
docker compose up -d
```

---

#### 4. 配置 ACL 启用自定义 DERP 节点

进入 [Tailscale ACL 编辑页](https://login.tailscale.com/admin/acls) → JSON 模式，在根对象添加：

```json
"derpMap": {
    "OmitDefaultRegions": false, // 可以设置为 true，这样不会下发官方的 derper 节点，测试或者实际使用都可以考虑打开
    "Regions": {
        "900": {
            "RegionID":   900, // tailscale 900-999 是保留给自定义 derper 的
            "RegionCode": "abc1",
            "RegionName": "abcc1",// 这俩随便命名
            "Nodes": [
                {
                    "Name":             "fff",
                    "RegionID":         900,
                    "IPv4":             "1.1.1.1", // 你的VPS 公网IP地址
                    "DERPPort":         12345, //上面 12345 你自定义的端口
                    "InsecureForTests": true, // 因为是自签名证书，所以客户端不做校验
                },
            ],
        },
        "901": {
            "RegionID":   901, // 加入新 derp 的时候记得修改
            "RegionCode": "abc2",
            "RegionName": "abcc2",
            "Nodes": [
                {
                    "Name":             "kkk",
                    "RegionID":         901,
                    "IPv4":             "8.8.8.8", // 你的VPS 公网IP地址
                    "DERPPort":         4000, //上面 12345 你自定义的端口
                    "InsecureForTests": true, // 因为是自签名证书，所以客户端不做校验
                },
            ],
        },
    },
},
```

> ⚠️ `DERPPort` 必须与 `docker-compose.yml` 中暴露的端口一致  
> ⚠️ `InsecureForTests: true` 是必须的（因使用自签名证书）

---

✅ 部署完成。客户端将在 P2P 失败时自动 fallback 到此中继，且仅允许你的 Tailnet 成员使用（防偷）。