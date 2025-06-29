# 测试ssh连接质量

## 🔹 一、测试延迟（Latency）

### ✅ 1. `ping` 命令
这是最简单也是最常用的测试网络延迟的方法。

```bash
ping <目标IP地址>
```

例如：
```bash
ping 192.168.1.100
```

- 它会显示从本机到目标主机的往返时间（RTT），单位为毫秒（ms）。
- 可以帮助你判断连接是否稳定、延迟是否高。

> ⚠️ 注意：有些系统或防火墙可能会屏蔽 ICMP 协议（即 ping 使用的协议），这时 `ping` 不通不代表不能建立 SSH 连接。

---

## 🔹 二、测试带宽（Bandwidth）

### ✅ 1. 使用 `iperf3` 工具

`iperf3` 是一个专门用于测量网络带宽的工具，非常适合测试局域网内的吞吐量。

#### 步骤如下：

##### 在一台设备上启动 `iperf3` 服务器模式：
```bash
iperf3 -s
```

##### 在另一台设备上运行客户端测试：
```bash
iperf3 -c <服务器IP地址>
```

例如：
```bash
iperf3 -c 192.168.1.100
```

输出示例：
```
[ ID] Interval           Transfer     Bitrate
[  4] 0.0-10.0 sec        1.12 GBytes    962 Mbits/sec
```

这表示在这段时间内平均带宽为 962 Mbps。

> 📌 提示：如果你没有安装 `iperf3`，可以通过包管理器安装，比如：
> - Ubuntu/Debian: `sudo apt install iperf3`
> - macOS (Homebrew): `brew install iperf3`
> - Windows: 下载官方版本 https://iperf.fr/

---


## 🔹 三、其他可选方法

### ✅ 使用 `mtr` 替代 `traceroute` + `ping`（查看路径和延迟）
```bash
mtr 192.168.1.100
```

适用于分析整个链路中的延迟问题。

