# Jetson AGX Orin 连接与使用教程

> 日期：2026-04-16
> 适用对象：需要在 Jetson AGX Orin 上进行机器人推理评估的同学
> 关联文档：[Jetson_AGX_Orin部署SmolVLA可行性分析](../03_技术调研/Jetson_AGX_Orin部署SmolVLA可行性分析.md)、[SmolVLA本地部署评估报告](../02_模型训练与部署/SmolVLA本地部署评估报告_20260415.md)

---

## 一、Jetson 基本信息

| 项目 | 信息 |
|------|------|
| 型号 | NVIDIA Jetson AGX Orin |
| 架构 | aarch64 (ARM64) |
| 统一内存 | 61.4 GB（CPU/GPU 共享） |
| JetPack | R36.4.7 (L4T 36.4.7) |
| CUDA | 12.6 |
| 局域网 IP | 192.168.18.149 |
| SSH 用户 | orin-1 |
| SSH 密码 | a |
| conda 环境 | lerobot (Python 3.10) |
| lerobot 路径 | ~/lerobot |
| lerobot 版本 | 0.4.4 (Seeed fork, editable) |
| PyTorch | 2.5.0a0 (NVIDIA Jetson 定制版) |

---

## 二、SSH 连接

### 2.1 基本连接

```bash
ssh orin-1@192.168.18.149
# 密码：a
```

### 2.2 免密登录（推荐）

```bash
# 在本机生成密钥（如果还没有）
ssh-keygen -t ed25519

# 将公钥复制到 Jetson
ssh-copy-id orin-1@192.168.18.149

# 之后直接 ssh 即可，无需输入密码
ssh orin-1@192.168.18.149
```

### 2.3 配置 SSH 别名

在本机 `~/.ssh/config` 中添加：

```
Host jetson
    HostName 192.168.18.149
    User orin-1
```

之后只需：

```bash
ssh jetson
```

### 2.4 连接排障

| 问题 | 原因 | 解决 |
|------|------|------|
| `Connection refused` | Jetson 未开机 / SSH 服务未启动 | 检查电源、网线，Jetson 上执行 `sudo systemctl start sshd` |
| `Connection timed out` | 不在同一网段 / IP 变了 | `ping 192.168.18.149`，检查本机 IP 是否在 192.168.18.x 网段 |
| `Host key verification failed` | Jetson 重装系统后指纹变了 | `ssh-keygen -R 192.168.18.149`，再重新连接 |

---

## 三、网络配置

### 3.1 HuggingFace 镜像（必配）

Jetson 无法直连 huggingface.co（DNS 解析失败），必须配置国内镜像：

```bash
# 已写入 bashrc，新连接自动生效
# 如未配置，手动执行：
export HF_ENDPOINT=https://hf-mirror.com

# 永久生效：
echo 'export HF_ENDPOINT=https://hf-mirror.com' >> ~/.bashrc
source ~/.bashrc
```

### 3.2 pip 源

Jetson 为 ARM 架构，部分包需从源码编译，清华源可能缺 aarch64 wheel。建议：

- 默认用 PyPI 官方源（Jetson 在国内网络下 pip 通常可用）
- 如遇超时再配清华源

### 3.3 局域网文件传输

Jetson 与本机在同一局域网时，scp 速度约 24MB/s：

```bash
# 本机 → Jetson
scp -r ~/下载/my_smolvla orin-1@192.168.18.149:~/my_smolvla

# Jetson → 本机
scp -r orin-1@192.168.18.149:~/my_smolvla ~/下载/

# 传输 VLM 主干缓存（从 Jetson 拷到本机，省下载时间）
scp -r orin-1@192.168.18.149:/home/orin-1/.cache/huggingface/hub/models--HuggingFaceTB--SmolVLM2-500M-Video-Instruct \
  ~/.cache/huggingface/hub/
```

---

## 四、Jetson 环境说明

### 4.1 conda 环境

```bash
# 激活 lerobot 环境
conda activate lerobot

# 查看已安装包
pip list | grep -E "lerobot|torch|transformers"
```

关键依赖版本：

| 包 | 版本 |
|----|------|
| Python | 3.10 |
| PyTorch | 2.5.0a0 (Jetson 定制版, nv24.08) |
| torchvision | 0.21.0 |
| transformers | 4.53.3 |
| accelerate | 1.13.0 |
| lerobot | 0.4.4 (editable, Seeed fork) |
| huggingface-hub | 0.35.3 |
| safetensors | 0.7.0 |

### 4.2 为什么不能升级 lerobot 到 0.5.x

| 依赖 | 0.5.x 要求 | Jetson 现状 | 状态 |
|------|-----------|------------|------|
| Python | >= 3.12 | 3.10 | 不可升级 |
| PyTorch | >= 2.7 | 2.5.0 | NVIDIA 未发布 Jetson 版 |

Jetson 的 PyTorch 是 NVIDIA 定制版，绑定 JetPack 版本，不能随意 pip install 升级。

### 4.3 重要限制

- **不要尝试 `pip install torch==2.7`**：会安装 x86 通用版，aarch64 上无法运行
- **不要尝试创建 Python 3.12 conda 环境**：NVIDIA 定制 PyTorch 只有 3.10 wheel
- 如需 0.5.x 推理功能，需手动移植代码（方案C，工作量大）

---

## 五、摄像头

### 5.1 设备号

Jetson 上的摄像头设备号**与本机不同**：

| 设备 | Jetson | 本机 | 用途 |
|------|--------|------|------|
| camera1（俯视） | /dev/video0 | /dev/video2 | 俯视摄像头 |
| camera2（腕部） | /dev/video6 | /dev/video10 | 腕部摄像头 |

### 5.2 检查摄像头

```bash
# 查看所有视频设备
ls /dev/video*

# 测试摄像头是否可用（需 cv2）
python3 -c "
import cv2
for i in [0, 6]:
    cap = cv2.VideoCapture(i)
    ok, frame = cap.read()
    print(f'video{i}: {"OK" if ok else "FAIL"}, shape={frame.shape if ok else "N/A"}')
    cap.release()
"
```

### 5.3 lerobot 中的摄像头配置

Jetson 上摄像头支持 MJPG fourcc，可以指定：

```yaml
cameras:
  camera1:
    type: opencv
    index_or_path: 0
    width: 640
    height: 480
    fps: 30
    fourcc: "MJPG"
  camera2:
    type: opencv
    index_or_path: 6
    width: 640
    height: 480
    fps: 30
    fourcc: "MJPG"
```

> 注意：本机摄像头**不要**指定 fourcc（会报 buf.empty 错误），Jetson 上可以指定。

---

## 六、SmolVLA 模型推理评估

### 6.1 模型传输到 Jetson

**方案一：从本机 scp（推荐，速度快）**

```bash
# 先在本机下载好模型
HF_ENDPOINT=https://hf-mirror.com hf download Ready321/my_smolvla --local-dir ~/下载/my_smolvla

# scp 到 Jetson
scp -r ~/下载/my_smolvla orin-1@192.168.18.149:~/my_smolvla
```

**方案二：Jetson 上用镜像直接下载**

```bash
HF_ENDPOINT=https://hf-mirror.com hf download Ready321/my_smolvla --local-dir ~/my_smolvla
```

### 6.2 VLM 主干下载

推理时还需要 SmolVLM2-500M-Video-Instruct（~2GB）：

```bash
HF_ENDPOINT=https://hf-mirror.com hf download HuggingFaceTB/SmolVLM2-500M-Video-Instruct
```

### 6.3 推理前必要修复

**(1) 删除 config.json 中的 use_peft 字段**

0.5.x 训练写入的字段，0.4.4 不认识：

```bash
python3 -c "
import json
path = '$HOME/my_smolvla/config.json'  # 改为你的模型路径
with open(path) as f:
    d = json.load(f)
d.pop('use_peft', None)
with open(path, 'w') as f:
    json.dump(d, f, indent=2)
print('Done: removed use_peft')
"
```

**(2) 确认 SmolVLA 已注册**

```python
from lerobot.configs.policies import PreTrainedConfig
print('smolvla' in PreTrainedConfig._choice_registry)  # 应为 True
```

如果为 False，需在 `lerobot_record.py` 中加一行 import：

```python
# ~/lerobot/src/lerobot/scripts/lerobot_record.py
# 在 from lerobot.configs.policies import PreTrainedConfig 后面加：
from lerobot.policies.smolvla.configuration_smolvla import SmolVLAConfig  # noqa: F401
```

**(3) 安装 num2words**

```bash
pip install num2words
```

### 6.4 Jetson 推理评估命令

```bash
conda activate lerobot

# 清除旧缓存
rm -rf ~/.cache/huggingface/lerobot/Ready321/eval_grab_redcube_test

HF_ENDPOINT=https://hf-mirror.com lerobot-record \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM0 \
  --robot.id=so101_cong_left \
  --robot.cameras='{ camera1: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30, fourcc: "MJPG"}, camera2: {type: opencv, index_or_path: 6, width: 640, height: 480, fps: 30, fourcc: "MJPG"} }' \
  --dataset.single_task="Grab the red cube to the white cup" \
  --dataset.repo_id=Ready321/eval_grab_redcube_test \
  --dataset.episode_time_s=50 \
  --dataset.num_episodes=10 \
  --dataset.push_to_hub=false \
  --policy.path=/home/orin-1/my_smolvla \
  --policy.empty_cameras=1 \
  --display_data=false
```

**参数说明**：

| 参数 | 值 | 说明 |
|------|----|------|
| `--robot.cameras` | camera1(0), camera2(6) | 摄像头名必须匹配训练时的 camera1/camera2 |
| `index_or_path` | 0, 6 | Jetson 摄像头设备号（不是本机的 2, 10！） |
| `fourcc` | "MJPG" | Jetson 摄像头支持 MJPG |
| `--policy.path` | /home/orin-1/my_smolvla | 必须绝对路径，不能用 ~ |
| `--policy.empty_cameras` | 1 | 训练时有3个摄像头，实际2个，第3个填空帧 |
| `--dataset.push_to_hub` | false | 不推送到 HF |
| `--display_data` | false | Jetson 通常无显示器，关闭显示 |

---

## 七、Jetson vs 本机 对照表

| 项目 | Jetson AGX Orin | 本机 (RTX 4060 Laptop) |
|------|----------------|----------------------|
| 架构 | aarch64 | x86_64 |
| GPU 显存 | 61.4 GB 统一内存 | 8 GB 独立显存 |
| Python | 3.10 | 3.10 / 3.12 |
| PyTorch | 2.5.0 (NVIDIA 定制) | 2.7+ |
| lerobot 版本 | 0.4.4 (Seeed) | 0.4.4 (Seeed) / 0.5.1 (官方) |
| 摄像头 camera1 | /dev/video0 | /dev/video2 |
| 摄像头 camera2 | /dev/video6 | /dev/video10 |
| 摄像头 fourcc | 可用 "MJPG" | 不指定（会报错） |
| HF 连接 | 需镜像 hf-mirror.com | 需镜像或直连 |
| 推理显存占用 | ~5GB / 61GB（充足） | ~7.2GB / 8GB（紧张） |
| SSH | orin-1@192.168.18.149 | N/A |
| conda 环境 | lerobot | lerobot-seeed / lerobot |

---

## 八、常见问题

### Q1: SSH 连不上

1. 确认 Jetson 已开机（电源指示灯亮）
2. 确认网线已连接，本机与 Jetson 在同一网段
3. `ping 192.168.18.149` 测试网络
4. 检查本机 IP：`ip addr`，应类似 192.168.18.x

### Q2: pip install 很慢或失败

Jetson (aarch64) 部分包没有预编译 wheel，需从源码编译，耗时较长。如果清华源缺 aarch64 包，去掉镜像用官方源：

```bash
pip install <package> --no-cache-dir
```

### Q3: 摄像头打不开

- 确认设备号正确：Jetson 是 video0 和 video6
- 检查是否有其他进程占用：`fuser /dev/video0`
- 试试不加 fourcc 参数

### Q4: 模型加载报 use_peft 错误

参见 6.3 节，删除 config.json 中的 use_peft 字段。

### Q5: policy 静默失败，机械臂空转

SmolVLA 注册 bug，参见 6.3 节第(2)步，手动加 import。

### Q6: 内存不足 (OOM)

Jetson 有 61GB 统一内存，SmolVLA 推理仅需 ~5GB，一般不会 OOM。如出现：
- 关闭其他占用内存的程序
- 检查是否有僵尸进程：`nvidia-smi` 或 `htop`

---

## 九、快速操作速查

```bash
# 连接
ssh jetson

# 激活环境
conda activate lerobot

# 检查摄像头
ls /dev/video*

# 检查 GPU 状态
nvidia-smi

# 检查磁盘
df -h

# 传输模型（本机执行）
scp -r ~/下载/my_smolvla jetson:~/my_smolvla

# 运行推理评估（Jetson 上执行）
cd ~/lerobot
HF_ENDPOINT=https://hf-mirror.com lerobot-record \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM0 \
  --robot.id=so101_cong_left \
  --robot.cameras='{ camera1: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30, fourcc: "MJPG"}, camera2: {type: opencv, index_or_path: 6, width: 640, height: 480, fps: 30, fourcc: "MJPG"} }' \
  --dataset.single_task="Grab the red cube to the white cup" \
  --dataset.repo_id=Ready321/eval_grab_redcube_test \
  --dataset.episode_time_s=50 \
  --dataset.num_episodes=10 \
  --dataset.push_to_hub=false \
  --policy.path=/home/orin-1/my_smolvla \
  --policy.empty_cameras=1 \
  --display_data=false
```
