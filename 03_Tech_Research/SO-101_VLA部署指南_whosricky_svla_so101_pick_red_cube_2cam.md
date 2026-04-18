# whosricky/svla-so101-pick-red-cube-2cam 部署指南

> 模型：https://huggingface.co/whosricky/svla-so101-pick-red-cube-2cam
> 基础模型：lerobot/smolvla_base（https://huggingface.co/lerobot/smolvla_base）
> 论文：https://arxiv.org/abs/2506.01844
> 更新日期：2026-04-16

---

## 一、模型关键参数

| 参数 | 值 | 说明 |
|------|-----|------|
| 策略类型 | smolvla | |
| 摄像头 | `gripper`（腕部）、`top`（俯视） | **注意：不是 camera1/camera2** |
| 状态维度 | [6] | 6个电机 |
| 动作维度 | [6] | 6个动作（包含夹爪） |
| chunk_size | 50 | 每次输出50个动作 |
| 数据集 | whosricky/so101_pick_mixed_cubes_2cams | 抓取混合颜色方块，2摄像头 |

---

## ⚠️ 重要兼容性警告

**你的 SO-101 是 5-DOF（电机ID 1-5，无夹爪 motor6）**，但该模型输出 6 维动作（包含夹爪）。

部署后可能出现问题：夹爪动作会被忽略，或报维度不匹配错误。如果遇到，需修改 `policy_postprocessor.json` 去除夹爪维度，或重新训练一个 5-DOF 版本。

---

## 二、部署步骤

### Step 1：下载模型

```bash
# 设置 HF 镜像（国内必需）
export HF_ENDPOINT=https://hf-mirror.com

# 下载微调模型（约1.2GB）
hf download whosricky/svla-so101-pick-red-cube-2cam --local-dir ~/下载/svla-so101-pick-red-cube-2cam

# 或通过 lerobot 下载
HF_ENDPOINT=https://hf-mirror.com lerobot-record \
  --policy.path=whosricky/svla-so101-pick-red-cube-2cam \
  --policy.repo_id=whosricky/svla-so101-pick-red-cube-2cam
```

### Step 2：修复 config.json（如果使用 lerobot-seeed 0.4.x）

模型用 lerobot 0.5.x 训练，若在 0.4.x 环境运行，需删除 `use_peft` 字段：

```bash
python3 -c "
import json
with open('~/下载/svla-so101-pick-red-cube-2cam/config.json') as f:
    d = json.load(f)
d.pop('use_peft', None)
with open('~/下载/svla-so101-pick-red-cube-2cam/config.json', 'w') as f:
    json.dump(d, f, indent=2)
"
```

### Step 3：测试摄像头

确认摄像头设备号和名称：

```bash
python3 -c "
import cv2
for i in range(16):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f'video{i}: OK, shape={frame.shape}')
        cap.release()
"
```

本机摄像头：`video2`（俯视）→ 对应 `top`，`video10`（腕部）→ 对应 `gripper`

### Step 4：修复 SmolVLA 注册 Bug（lerobot-seeed 0.4.x 必需）

lerobot-seeed 的 `lerobot_record.py` 不会自动注册 SmolVLA，需手动 import：

```python
# 在 lerobot_record.py 中找到：
from lerobot.configs.policies import PreTrainedConfig

# 在其下方添加：
from lerobot.policies.smolvla.configuration_smolvla import SmolVLAConfig  # noqa: F401
```

验证：
```python
from lerobot.configs.policies import PreTrainedConfig
from lerobot.policies.smolvla.configuration_smolvla import SmolVLAConfig
print('smolvla' in PreTrainedConfig._choice_registry)  # 应输出 True
```

### Step 5：运行评估/推理

使用 lerobot-record 推理：

```bash
HF_ENDPOINT=https://hf-mirror.com lerobot-record \
  --robot.type=so100_follower \
  --robot.port=/dev/ttyACM0 \
  --robot.id=so101_cong_left \
  --robot.cameras='{ gripper: {type: opencv, index_or_path: 10, width: 640, height: 480, fps: 30}, top: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30} }' \
  --dataset.repo_id=whosricky/so101_pick_mixed_cubes_2cams \
  --dataset.episode_time_s=50 \
  --dataset.num_episodes=5 \
  --dataset.push_to_hub=false \
  --dataset.single_task="pick the red cube" \
  --policy.path=/home/xuan/下载/svla-so101-pick-red-cube-2cam \
  --policy.empty_cameras=1 \
  --teleop.type=so100_leader \
  --teleop.port=/dev/ttyACM1 \
  --teleop.id=so101_zhu_left
```

**参数说明：**

| 参数 | 值 | 说明 |
|------|-----|------|
| `--robot.type` | `so100_follower` | lerobot 0.5.x 中 SO-101 使用此类型 |
| `--robot.port` | `/dev/ttyACM0` | 从臂端口 |
| `--robot.id` | `so101_cong_left` | 从臂ID（按你的配置） |
| `--robot.cameras` | 见上 | **摄像头名必须是 `gripper` 和 `top`** |
| `--policy.path` | 绝对路径 | 必须是绝对路径，不能用 `~/` |
| `--policy.empty_cameras` | 1 | 2摄像头，模型训练时可能有3个 |
| `--teleop.*` | | 主臂遥操作，复位时用 |

---

## 三、摄像头名称映射

| 你的摄像头 | 视频设备 | 模型期望名称 |
|-----------|---------|------------|
| 俯视摄像头 | video2 | `top` |
| 腕部摄像头 | video10 | `gripper` |

**注意**：本模型摄像头名是 `gripper` 和 `top`，**不是** `camera1`/`camera2` 或 `front`/`wrist`。

---

## 四、常见错误

| 错误 | 原因 | 解决方法 |
|------|------|---------|
| `KeyError: 'smolvla'` | SmolVLAConfig 未注册 | 添加 explicit import（见 Step 4） |
| `use_peft` 字段报错 | 0.5.x config 在 0.4.x 运行 | 删除 config.json 中的 `use_peft` |
| 动作维度不匹配 | 5-DOF 臂 + 6-DOF 模型 | 修改 postprocessor 或重新训练 5-DOF 模型 |
| `HFValidationError: '~'` | 路径用了 `~/` | 用绝对路径 `/home/xuan/...` |
| 摄像头画面卡住/黑屏 | fourcc 不兼容 | 本机不指定 fourcc，删除该参数 |

---

## 五、替代方案

如果该模型因 6-DOF 问题无法使用，可以考虑：

1. **使用其他 SO-101 微调模型**（需检查是否 5-DOF）：
   - `yathAg/pi05_so101_pick_place_fp16`（ACT算法）
   - `lerobot-edinburgh-white-team/smolvla_svla_so101_pickplace`

2. **用你自己的数据集微调 SmolVLA**：
   - 基础模型：https://huggingface.co/lerobot/smolvla_base
   - 数据集格式参考：`whosricky/so101_pick_mixed_cubes_2cams`

---

## 六、相关链接

- 模型：https://huggingface.co/whosricky/svla-so101-pick-red-cube-2cam
- 基础模型 SmolVLA：https://huggingface.co/lerobot/smolvla_base
- 训练数据集：https://huggingface.co/datasets/whosricky/so101_pick_mixed_cubes_2cams
- LeRobot 官方：https://github.com/huggingface/lerobot
- SmolVLA 论文：https://arxiv.org/abs/2506.01844
