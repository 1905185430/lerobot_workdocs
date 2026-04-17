# Seeed Studio 维护版 LeRobot 安装记录

> 日期：2026-04-15
> 环境：Ubuntu 22.04 / conda lerobot-seeed / Python 3.10
> 仓库：https://github.com/Seeed-Projects/lerobot

---

## 核心结论

- Seeed 维护的 fork 版本号 **0.4.3**（官方同期为 0.5.1），是 Seeed 验证过的稳定版
- conda 环境名 `lerobot-seeed`，与官方 `lerobot` 环境并存互不干扰
- 同样需要修改 `feetech.py` 波特率为 500000（CH9101F 芯片硬件限制）

---

## 一、与官方环境对比

| 项目 | 官方 lerobot | Seeed lerobot-seeed |
|------|-------------|---------------------|
| conda 环境名 | `lerobot` | `lerobot-seeed` |
| Python 版本 | 3.12 | 3.10（Seeed 推荐） |
| 仓库地址 | huggingface/lerobot | Seeed-Projects/lerobot |
| 本地路径 | ~/lerobot | ~/lerobot-seeed |
| LeRobot 版本 | 0.5.1 | 0.4.3 |
| 波特率修改 | 需要 | 需要（同理） |

---

## 二、安装步骤

### 2.1 创建 conda 环境

```bash
conda create -y -n lerobot-seeed python=3.10
conda activate lerobot-seeed
```

### 2.2 克隆 Seeed 仓库

```bash
# 直连 GitHub 可能超时，用镜像加速
git clone https://gitclone.com/github.com/Seeed-Projects/lerobot.git ~/lerobot-seeed
```

> 踩坑：直接 `git clone https://github.com/Seeed-Projects/lerobot.git` 超时断连，
> `ghfast.top` 和 `mirror.ghproxy.com` 也 TLS 失败，`gitclone.com` 成功。

### 2.3 安装 ffmpeg

```bash
# conda install ffmpeg 遇到 SSL 错误，改用系统包
sudo apt install ffmpeg -y
```

> 踩坑：conda-forge 的 ffmpeg 在国内下载时 SSL 报错
> `CondaSSLError: [SSL: DECRYPTION_FAILED_OR_BAD_RECORD_MAC]`，系统 apt 装的已满足需求。

### 2.4 安装 LeRobot

```bash
cd ~/lerobot-seeed
pip install -e ".[feetech]"
```

### 2.5 修改波特率（必须）

原因：USB 转串口芯片 CH9101F 在 1Mbps 下通信不稳定，详见 [SO101通信失败修复记录.md](SO101通信失败修复记录.md)

```bash
# 修改 ~/lerobot-seeed/src/lerobot/motors/feetech/feetech.py
# 第37行：
# 原：DEFAULT_BAUDRATE = 1_000_000
# 改：DEFAULT_BAUDRATE = 500_000
```

editable 安装模式，修改后立即生效，无需重装。

### 2.6 验证安装

```bash
conda activate lerobot-seeed

# 检查命令可用
which lerobot-teleoperate   # /home/xuan/anaconda3/envs/lerobot-seeed/bin/lerobot-teleoperate
which lerobot-calibrate     # /home/xuan/anaconda3/envs/lerobot-seeed/bin/lerobot-calibrate
which lerobot-record        # /home/xuan/anaconda3/envs/lerobot-seeed/bin/lerobot-record
which lerobot-train         # /home/xuan/anaconda3/envs/lerobot-seeed/bin/lerobot-train

# 检查版本
python -c "import lerobot; print(lerobot.__version__)"  # 0.4.3
```

---

## 三、使用方式

激活环境后，命令用法与官方完全一致：

```bash
conda activate lerobot-seeed

# 遥操作
lerobot-teleoperate \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM0 \
    --robot.id=so101_cong_left \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM1 \
    --teleop.id=so101_zhu_left \
    --robot.cameras '{"top": {"type": "opencv", "index_or_path": "/dev/video8", "fps": 30, "width": 640, "height": 480}, "wrist": {"type": "opencv", "index_or_path": "/dev/video10", "fps": 30, "width": 640, "height": 480}}'

# 校准
lerobot-calibrate --robot.type=so101_follower --robot.port=/dev/ttyACM0 --robot.id=so101_cong_left
lerobot-calibrate --teleop.type=so101_leader --teleop.port=/dev/ttyACM1 --teleop.id=so101_zhu_left
```

---

## 四、注意事项

1. **git pull 风险**：更新 Seeed 仓库时可能覆盖波特率修改，pull 后需重新检查 `feetech.py`
2. **两环境并存**：`lerobot`（官方 0.5.1）和 `lerobot-seeed`（Seeed 0.4.3）互不干扰，使用前确认激活了正确的环境
3. **版本差异**：Seeed 0.4.3 功能上可能落后官方 0.5.1，但 Seeed 声称更稳定；若需新功能（如新版训练 API）用官方环境
4. **Seeed 独有功能**：DepthCameraSupport 分支（Orbbec/RealSense 深度相机）、Seeed_RoboController 校准工具
5. **校准文件**：两个环境的校准文件共享同一目录 `~/.cache/lerobot/calibration/`，如果两版本校准逻辑不同可能需重新校准

---

## 五、参考

- Seeed 教程：https://wiki.seeedstudio.com/lerobot_so100m_new/
- Seeed 仓库：https://github.com/Seeed-Projects/lerobot
- 教程对比文档：[../03_技术调研/Seeed_vs_LeRobot_SO101教程对比.md](../03_技术调研/Seeed_vs_LeRobot_SO101教程对比.md)
- 波特率问题详解：[SO101通信失败修复记录.md](SO101通信失败修复记录.md)
