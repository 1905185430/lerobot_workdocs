# PPIO 云服务器 LeRobot 训练部署指南

> 服务器：PPIO GPU 实例（美国加州圣克拉拉，DigitalOcean）
> GPU：NVIDIA RTX 4090 (24GB)
> RAM：1TB | 磁盘：130GB
> OS：Ubuntu 22.04.3 LTS

---

## 一、连接服务器

```bash
ssh -p 52073 root@proxy.us-ca-nas-2.gpu-instance.ppinfra.com
# 密码见 PPIO 控制台
```

> 注意：端口和地址每次创建实例可能不同，以 PPIO 控制台为准。

---

## 二、环境部署

### 2.1 删除清华源（海外服务器不需要）

PPIO 镜像可能预配了清华源，海外直连 PyPI 更快，需删除：

```bash
# 查看当前 pip 配置
pip config list -v

# 删除清华源配置（通常在 ~/.config/pip/pip.conf）
rm ~/.config/pip/pip.conf

# 验证已清除
pip config list  # 应无输出
```

### 2.2 安装 Miniconda

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b
~/miniconda3/bin/conda init bash
source ~/.bashrc
```

> 如果服务器已有 conda（PPIO 镜像通常自带 `/root/anaconda3`），跳过此步。

### 2.3 创建 conda 环境

```bash
conda create -n lerobot python=3.10 -y
conda activate lerobot
```

### 2.4 克隆 LeRobot（Seeed Fork）

```bash
cd ~
git clone https://github.com/Seeed-Projects/lerobot.git
cd lerobot
```

### 2.5 安装 LeRobot 及依赖

```bash
# 基础安装 + SmolVLA 支持
pip install -e ".[smolvla]"
```

> 这会自动安装 torch、transformers、accelerate 等依赖。

### 2.6 安装系统依赖

```bash
apt update && apt install -y ffmpeg tmux
```

- **ffmpeg**：torchcodec 解码视频帧必需，否则训练时 `DataLoader` 报 `RuntimeError: Could not load libtorchcodec`
- **tmux**：保持训练在后台运行，SSH 断开不中断

### 2.7 登录 HuggingFace

```bash
pip install huggingface_hub
huggingface login
# 粘贴 HF token（从 https://huggingface.co/settings/tokens 获取）
```

### 2.8 登录 WandB（可选但推荐）

```bash
pip install wandb
wandb login
# 粘贴 WandB API key（从 https://wandb.ai/authorize 获取）
```

---

## 三、训练

### 3.1 用 tmux 保持训练不断

```bash
tmux new -s train           # 创建会话
# 在 tmux 中运行训练命令
# Ctrl+B, D 断开（训练继续）
# 重连：tmux attach -t train
```

### 3.2 SmolVLA 训练命令

```bash
lerobot-train \
  --policy.path=lerobot/smolvla_base \
  --policy.repo_id=Ready321/my_smolvla \
  --dataset.repo_id=Ready321/vla_grab_redcube \
  --dataset.revision=v0.5.2 \
  --batch_size=64 \
  --steps=10000 \
  --save_freq=2000 \
  --output_dir=outputs/train/my_smolvla_v3 \
  --job_name=my_smolvla_training \
  --policy.device=cuda \
  --wandb.enable=true \
  --rename_map='{"observation.images.top": "observation.images.camera1", "observation.images.wrist": "observation.images.camera2"}' \
  --policy.empty_cameras=1
```

### 3.3 参数说明

| 参数 | 说明 |
|------|------|
| `--policy.path` | 预训练模型起点，smolvla_base (450M) |
| `--policy.repo_id` | 训练完成后推送到 HF 的仓库名 |
| `--dataset.repo_id` | HF 上的数据集名称 |
| `--dataset.revision` | 数据集版本 tag（0.4.x 格式数据集需用修复后的 tag） |
| `--batch_size` | 批大小，RTX 4090 24GB 可跑 64 |
| `--steps` | 训练步数，30ep/12K帧数据建议 5000~10000 |
| `--save_freq` | 每 N 步存一次 checkpoint |
| `--output_dir` | 输出目录，不能与已有目录重名（除非 --resume） |
| `--rename_map` | 将数据集摄像头名映射到策略期望的 camera1/2/3 |
| `--policy.empty_cameras` | 缺少的摄像头数量用空帧填充（SmolVLA 默认期望3个摄像头） |

### 3.4 步数建议

| 数据量 | 建议步数 | 说明 |
|--------|---------|------|
| ~30ep, 12K帧 | 5000~10000 | batch_size=64 时 1 epoch ≈ 200 步 |
| ~50ep | 10000~20000 | 官方推荐起步量 |
| ~100ep+ | 20000+ | 数据充足可跑更多 |

> 20000 步是官方示例值，不是必须。数据少时跑太多会过拟合，建议看 wandb loss 曲线决定。

---

## 四、常见报错及解决

### 4.1 `ValueError: 'policy.repo_id' argument missing`

**原因**：缺少 `--policy.repo_id` 参数。

**解决**：加上 `--policy.repo_id=你的HF用户名/模型名`。

### 4.2 `BackwardCompatibilityError` / `NotImplementedError`

**原因**：数据集由 lerobot 0.4.x 采集，`info.json` 中 `codebase_version` 为 `"v3.0"`，0.5.x 期望 `"v0.5.2"`。

**解决**：用修复后的 revision tag：
```bash
--dataset.revision=v0.5.2
```
如果 tag 不存在，需在 HF 上修改数据集的 `meta/info.json`，将 `codebase_version` 改为 `"v0.5.2"`，补充 `fps`、`video_info`、`next.done` 等字段，然后打 tag：
```python
from huggingface_hub import HfApi
HfApi().create_tag("Ready321/vla_grab_redcube", tag="v0.5.2", repo_type="dataset")
```

### 4.3 `FileExistsError: Output directory already exists`

**原因**：上次训练（即使失败）已创建输出目录。

**解决**：
```bash
rm -rf outputs/train/你的目录名
```
或换个新的 `--output_dir`。

### 4.4 `ValueError: Feature mismatch` / Missing camera1/2/3

**原因**：数据集摄像头名（如 top/wrist）与 SmolVLA 期望的（camera1/2/3）不匹配。

**解决**：加 `--rename_map` 和 `--policy.empty_cameras`：
```bash
--rename_map='{"observation.images.top": "observation.images.camera1", "observation.images.wrist": "observation.images.camera2"}' \
--policy.empty_cameras=1
```

### 4.5 `RuntimeError: Could not load libtorchcodec`

**原因**：缺少 ffmpeg，torchcodec 无法解码视频。

**解决**：
```bash
apt update && apt install -y ffmpeg
```

### 4.6 `wandb.errors.errors.UsageError: No API key configured`

**解决**：
```bash
wandb login
```

---

## 五、训练监控

- **终端日志**：tmux 中直接查看，每 `--log_freq`（默认200）步输出一次
- **WandB 面板**：训练启动后会输出 wandb run URL，浏览器打开即可看 loss 曲线
- **日志格式**：`step:200 smpl:13K ep:30 epch:1.01 loss:0.055 grdn:0.570 lr:3.0e-05 updt_s:0.951 data_s:0.053`

---

## 六、环境信息参考

| 项目 | 版本 |
|------|------|
| OS | Ubuntu 22.04.3 LTS |
| GPU | NVIDIA RTX 4090 (24GB) |
| CUDA | 12.6 |
| Python | 3.10.12 |
| lerobot | 0.4.4 (Seeed fork) |
| PyTorch | 2.7.1 |
| transformers | 4.57.6 |
| accelerate | 1.13.0 |
| torchcodec | 0.5 |
| wandb | 0.24.2 |
| ffmpeg | 8.0.1 |
| LeRobot 来源 | https://github.com/Seeed-Projects/lerobot.git |
