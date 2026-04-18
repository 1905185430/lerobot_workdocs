# SO-101 双臂机器人系统手册

> 适用环境：Ubuntu 22.04 / lerobot conda (Python 3.12, LeRobot 0.5.1) / lerobot-seeed conda (Python 3.10, LeRobot 0.4.3)
>
> 最后更新：2026-04-17

---

## 目录

1. [项目总览](#1-项目总览)
2. [硬件参考](#2-硬件参考)
3. [环境配置](#3-环境配置)
4. [校准](#4-校准)
5. [遥操作](#5-遥操作)
6. [相机与视觉](#6-相机与视觉)
7. [数据采集与回放](#7-数据采集与回放)
8. [故障排查](#8-故障排查)
9. [附录](#9-附录)

---

## 1. 项目总览

### 1.1 文件结构

```
01_SO101硬件与调试/
│
├── README.md                              ← 本文档（系统手册）
│
├── 01_校准/                               # 机械臂校准
│   ├── calibrate_follower_left.py         ← 左从臂校准
│   ├── calibrate_follower_right.py        ← 右从臂校准
│   ├── calibrate_leader_left.py           ← 左主臂校准
│   ├── calibrate_leader_right.py          ← 右主臂校准
│   ├── USB端口映射表.md                    ← 端口映射参考
│   └── SO101工作总结_20260417.md           ← 工作日志
│
├── 02_遥操作/                             # 遥操作程序
│   ├── teleoperate.py                     ← 三模式遥操作（无摄像头）
│   ├── teleoperate_2cam.py                ← 双摄像头遥操作
│   └── teleoperate_3cam.py                ← 三摄像头遥操作
│
├── 03_数据采集/                           # 数据录制
│   ├── record_so101_2cam.py               ← 双摄像头数据采集
│   └── record_so101_3cam.py               ← 三摄像头数据采集
│
├── 04_摄像头工具/                         # 摄像头识别与调试
│   ├── camera_identifier.py               ← 相机识别 GUI
│   ├── camera_capture.py                  ← 摄像头画面采集
│   ├── camera_names.txt                   ← 相机预设名称
│   └── outputs/                           ← 采集输出样图
│
├── 05_故障修复记录/
│   └── SO101通信失败修复记录.md            ← CH9101F 波特率修复
│
├── 06_环境安装记录/
│   └── Seeed版LeRobot安装记录.md           ← Seeed fork 安装记录
│
├── calibration/                           # 校准数据备份（可跨机器迁移）
│   ├── robots/so_follower/
│   │   ├── bimanual_follower_left.json
│   │   └── bimanual_follower_right.json
│   └── teleoperators/so_leader/
│       ├── bimanual_leader_left.json
│       └── bimanual_leader_right.json
│
└── archive/                               # 历史文档归档
    ├── SO101双臂遥操作部署文档.md
    ├── SO101遥操作与校准程序使用说明.md
    └── SO101遥操作运行文档.md
```

### 1.2 操作方式总览

本系统每个核心功能提供两种操作方式：

| 功能 | 终端版 (CLI) | Python版 (Script) |
|---|---|---|
| 校准 | `lerobot-calibrate` | `python so101_xxx.py` |
| 单臂遥操作 | `lerobot-teleoperate` | `python teleoperate.py` 模式1 |
| 双臂遥操作 | `lerobot-teleoperate --robot.type bi_so_follower` | `python teleoperate.py` 模式3 |
| 一对多遥操作 | 不支持 | `python teleoperate.py` 模式2 |
| 数据录制 | `lerobot-record` | `python record_so101_2cam.py` |
| 数据回放 | `lerobot-replay` | 暂不支持 |
| 相机识别 | 手动 `ls /dev/video*` | `python camera_identifier.py` GUI |

**如何选择：**

- 快速调试 / 日常使用 → Python版（交互菜单，免记参数，端口固定）
- 数据录制 / 回放 / 带摄像头 → 终端版（功能更全）
- 首次部署 / 自动化脚本 → 终端版（可脚本化，参数可追溯）

---

## 2. 硬件参考

### 2.1 机械臂

| 臂名称 | 角色 | USB Serial ID | by-id 路径 | 当前映射 |
|---|---|---|---|---|
| so101_cong_left | Follower（从臂） | 5B42073876 | `/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B42073876-if00` | ttyACM3 |
| so101_cong_right | Follower（从臂） | 5B41532613 | `/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B41532613-if00` | ttyACM1 |
| so101_zhu_left | Leader（主臂） | 5B41533034 | `/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B41533034-if00` | ttyACM2 |
| so101_zhu_right | Leader（主臂） | 5B42137834 | `/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B42137834-if00` | ttyACM0 |

> ttyACM 编号在拔插后会变化，by-id 路径始终固定。Python版脚本全部使用 by-id，终端版命令使用 ttyACM（需每次确认）。

### 2.2 相机

| 设备 | by-id 路径 | 当前映射 | 说明 |
|---|---|---|---|
| 笔记本前置 | `/dev/v4l/by-id/usb-Sonix_Technology_..._video-index0` | video0 | 非机械臂相机 |
| 相机1（副摄） | `/dev/v4l/by-id/usb-Sonix_Technology_..._video-index1` | video1 | 同一USB设备不同端点 |

> 同型号相机 Serial 相同时，by-id 无法区分，需用 by-path 或 udev 规则。

### 2.3 硬件清单

双臂完整配置需要：
- 4x SO-101 机械臂（2从2主）
- 4x USB-C 线 + 4x 电源适配器 + 4x 桌夹
- 2x USB 摄像头（俯视 + 腕部，可选）

---

## 3. 环境配置

### 3.1 Conda 环境

| | lerobot（官方） | lerobot-seeed（Seeed fork） |
|---|---|---|
| Python | 3.12 | 3.10 |
| LeRobot 版本 | 0.5.1 | 0.4.3 |
| 本地路径 | ~/lerobot | ~/lerobot-seeed |
| bi_so_follower/leader | 内置 | 无（仅 bi_so100） |
| 推荐用途 | 双臂遥操作、训练 | 单臂调试、Seeed 深度相机 |

```bash
conda activate lerobot       # 日常使用（推荐）
# conda activate lerobot-seeed  # 仅需 Seeed 功能时
```

### 3.2 波特率修复（必须！）

CH9101F USB芯片在 1Mbps 下通信不可靠，必须改为 500000：

```bash
# 查找 feetech.py 并检查
FEETECH_PATH=$(python -c "import lerobot.motors.feetech.feetech as m; print(m.__file__)")
grep "DEFAULT_BAUDRATE" "$FEETECH_PATH"
# 期望输出: DEFAULT_BAUDRATE = 500_000

# 如果仍是 1_000_000，执行修复：
sed -i 's/DEFAULT_BAUDRATE = 1_000_000/DEFAULT_BAUDRATE = 500_000/' "$FEETECH_PATH"
```

> ⚠️ 每次 pip install / git pull / conda update lerobot 后都会覆盖此修改，需重新执行！

详细排查过程见 [05_故障修复记录/SO101通信失败修复记录.md](05_故障修复记录/SO101通信失败修复记录.md)。

### 3.3 串口权限

```bash
# 临时授权（重启后失效）
sudo chmod 666 /dev/ttyACM* /dev/ttyUSB* 2>/dev/null

# 永久授权（需重新登录）
sudo usermod -aG dialout $USER
```

Python版脚本内置了 `sudo chmod 666`，运行时会自动申请权限。

---

## 4. 校准

### 4.1 何时需要校准

| 场景 | 是否需要校准 |
|---|---|
| 首次使用新臂 | 是，交互式校准 |
| 拔插 USB 后 | 否，校准文件仍有效 |
| 提示 "Mismatch between calibration values" | 否，按 Enter 写入即可 |
| 更换电机 | 是，重新校准 |
| 换电脑（同臂迁移） | 否，复制校准文件 + 按 Enter 写入 |
| 波特率修改后 | 是，需重新校准 |

### 4.2 Python版 — 一键校准

每条臂对应一个独立脚本，端口已写死为 by-id 路径，直接运行即可：

```bash
conda activate lerobot

# 从臂
python 01_校准/calibrate_follower_left.py      # 左从臂
python 01_校准/calibrate_follower_right.py     # 右从臂

# 主臂
python 01_校准/calibrate_leader_left.py       # 左主臂
python 01_校准/calibrate_leader_right.py      # 右主臂
```

每个脚本执行流程：
1. 自动 `sudo chmod 666`（需输密码）
2. 连接臂 → 进入交互式校准
3. 将臂移到中间位置 → 按 Enter
4. 依次转动各关节通过完整范围 → 按 Enter 完成
5. 自动断开连接

### 4.3 终端版 — CLI 校准

```bash
conda activate lerobot

# 从臂
lerobot-calibrate \
  --robot.type so101_follower \
  --robot.port /dev/ttyACM0 \
  --robot.id so101_cong_left

# 主臂
lerobot-calibrate \
  --teleop.type so101_leader \
  --teleop.port /dev/ttyACM1 \
  --teleop.id so101_zhu_left
```

> 端口号需先用 `ls /dev/ttyACM*` 或 `lerobot-find-port` 确认。双臂模式下校准 ID 使用 `bimanual_follower_left` 等前缀。

### 4.4 校准不匹配处理

启动遥操作时如果提示 "Mismatch between calibration values"：

- **按 Enter** → 用已有校准文件写入电机（推荐，秒完成）
- **按 c** → 重新交互式校准

### 4.5 校准数据

存储位置：
```
~/.cache/huggingface/lerobot/calibration/
├── robots/so_follower/
│   ├── so101_cong_left.json
│   ├── so101_cong_right.json
│   ├── bimanual_follower_left.json
│   └── bimanual_follower_right.json
└── teleoperators/so_leader/
    ├── so101_zhu_left.json
    ├── so101_zhu_right.json
    ├── bimanual_leader_left.json
    └── bimanual_leader_right.json
```

备份已保存在 `calibration/` 目录，可跨机器迁移（校准数据绑定臂硬件，不绑定电脑）。

迁移方法：
```bash
# 打包
cd ~/.cache/huggingface/lerobot/calibration && tar czf ~/so101_calibration.tar.gz .
# 拷贝到新电脑后
mkdir -p ~/.cache/huggingface/lerobot/calibration && cd $_ && tar xzf ~/so101_calibration.tar.gz
# 首次启动遥操作时按 Enter 写入电机
```

---

## 5. 遥操作

### 5.1 Python版 — 交互式菜单

```bash
conda activate lerobot
python 02_遥操作/teleoperate.py
```

```
==================================================
      🌟 欢迎使用 SO101 遥操作控制系统 🌟
==================================================
请选择你的遥操作模式：
  [1] 一对一遥操作 (单臂控制单主从臂)
  [2] 一对多遥操作 (单主臂同步控制双从臂)
  [3] 双臂遥操作   (双主臂独立控制双从臂)
==================================================
输入选项数字 (1/2/3) 并回车:
```

**模式 1 — 一对一**（单主臂 → 单从臂）

```
选1: 左主臂 → 左从臂
选2: 右主臂 → 右从臂
```
适用：单臂调试、单臂数据采集。

**模式 2 — 一对多**（单主臂 → 双从臂同步）

```
右主臂 → 左从臂 + 右从臂（同步动作）
```
适用：双臂对称任务、单手操控双臂演示。

**模式 3 — 双臂**（双主臂 → 双从臂，独立控制）

```
左主臂 → 左从臂
右主臂 → 右从臂（同时独立运行）
```
适用：双臂协同任务（如交接物体）、双臂数据采集。

退出：**Ctrl+C** 安全断开。

### 5.2 终端版 — CLI 命令

**单臂遥操作：**

```bash
lerobot-teleoperate \
  --teleop.type so101_leader \
  --teleop.port /dev/ttyACM1 \
  --teleop.id so101_zhu_left \
  --robot.type so101_follower \
  --robot.port /dev/ttyACM0 \
  --robot.id so101_cong_left \
  --fps 30
```

**单臂 + 摄像头：**

```bash
lerobot-teleoperate \
  --teleop.type so101_leader \
  --teleop.port /dev/ttyACM1 \
  --teleop.id so101_zhu_left \
  --robot.type so101_follower \
  --robot.port /dev/ttyACM0 \
  --robot.id so101_cong_left \
  --robot.cameras '{"top": {"index_or_path": "/dev/video2", "height": 480, "width": 640}, "wrist": {"index_or_path": "/dev/video10", "height": 480, "width": 640}}' \
  --display_data true \
  --fps 30
```

**双臂遥操作：**

```bash
lerobot-teleoperate \
  --robot.type bi_so_follower \
  --robot.left_arm_config.port=/dev/ttyACM0 \
  --robot.right_arm_config.port=/dev/ttyACM1 \
  --robot.id bimanual_follower \
  --teleop.type bi_so_leader \
  --teleop.left_arm_config.port=/dev/ttyACM2 \
  --teleop.right_arm_config.port=/dev/ttyACM3 \
  --teleop.id bimanual_leader \
  --display_data true \
  --fps 30
```

**双臂 + 摄像头：**

```bash
lerobot-teleoperate \
  --robot.type bi_so_follower \
  --robot.left_arm_config.port=/dev/ttyACM0 \
  --robot.right_arm_config.port=/dev/ttyACM1 \
  --robot.id bimanual_follower \
  --robot.left_arm_config.cameras='{"top": {"type": "opencv", "index_or_path": "/dev/video2", "fps": 30, "width": 640, "height": 480}}' \
  --robot.right_arm_config.cameras='{"wrist": {"type": "opencv", "index_or_path": "/dev/video10", "fps": 30, "width": 640, "height": 480}}' \
  --teleop.type bi_so_leader \
  --teleop.left_arm_config.port=/dev/ttyACM2 \
  --teleop.right_arm_config.port=/dev/ttyACM3 \
  --teleop.id bimanual_leader \
  --display_data true \
  --fps 30
```

> 摄像头名称自动加臂前缀：`left_top`、`right_wrist` 等。

### 5.3 两种方式对比

| | Python版 | 终端版 |
|---|---|---|
| 端口指定 | by-id（固定） | ttyACM（需每次确认） |
| 串口权限 | 自动处理 | 手动 chmod |
| 模式切换 | 选数字 | 重输完整命令 |
| 一对多模式 | 支持 | 不支持 |
| 摄像头 | 暂不支持 | 支持 |
| 数据录制 | 暂不支持 | 支持（lerobot-record） |
| 自动化脚本 | 不便 | 适合（参数可追溯） |
| 底层实现 | SO101Leader + SO101Follower API | bi_so_follower/bi_so_leader 模块 |

---

## 6. 相机与视觉

### 6.1 相机识别 GUI 工具

```bash
pip install PySimpleGUI opencv-python    # 首次安装依赖
python 04_摄像头工具/camera_identifier.py
```

功能：
- 自动检测 /dev/video* 设备
- 实时预览画面，确认身份
- 手动输入或从预设名称选择分配
- 保存 camera_mapping.json + camera_mapping.md + udev 规则

操作流程：
1. 左侧设备列表选择相机 → 右侧实时预览
2. "名称分配"栏输入名称，或点击"预设名称"快捷填入
3. 点击"保存配置" → 生成三个文件

### 6.2 安装 udev 规则

```bash
sudo cp 04_摄像头工具/99-so101-cameras.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
```

安装后相机设备名固定，不再受 video 编号变化影响。

### 6.3 手动确认相机

```bash
# 列出所有视频设备
ls /dev/video*

# 查看设备详细信息
udevadm info -q property -p /sys/class/video4linux/video0
```

---

## 7. 数据采集与回放

> 数据采集与回放目前仅终端版支持。

### 7.1 单臂数据录制

```bash
lerobot-record \
  --teleop.type so101_leader \
  --teleop.port /dev/ttyACM1 \
  --teleop.id so101_zhu_left \
  --robot.type so101_follower \
  --robot.port /dev/ttyACM0 \
  --robot.id so101_cong_left \
  --robot.cameras '{"top": {"index_or_path": "/dev/video2", "height": 480, "width": 640}}' \
  --fps 30 \
  --repo-id Ready321/你的数据集名 \
  --num-episodes 50 \
  --single-branch true
```

### 7.2 双臂数据录制

```bash
lerobot-record \
  --robot.type bi_so_follower \
  --robot.left_arm_config.port=/dev/ttyACM0 \
  --robot.right_arm_config.port=/dev/ttyACM1 \
  --robot.id bimanual_follower \
  --robot.left_arm_config.cameras='{"top": {"type": "opencv", "index_or_path": "/dev/video2", "fps": 30, "width": 640, "height": 480}}' \
  --robot.right_arm_config.cameras='{"wrist": {"type": "opencv", "index_or_path": "/dev/video10", "fps": 30, "width": 640, "height": 480}}' \
  --teleop.type bi_so_leader \
  --teleop.left_arm_config.port=/dev/ttyACM2 \
  --teleop.right_arm_config.port=/dev/ttyACM3 \
  --teleop.id bimanual_leader \
  --fps 30 \
  --dataset.repo-id Ready321/bimanual_so101_handover \
  --dataset.num-episodes 50 \
  --dataset.single-task="Hand over the red cube from left arm to right arm"
```

> 数据中动作/观测 key 自动带 `left_` / `right_` 前缀。

### 7.3 数据回放

```bash
lerobot-replay \
  --robot.type so101_follower \
  --robot.port /dev/ttyACM0 \
  --robot.id so101_cong_left \
  --fps 30 \
  --repo-id Ready321/你的数据集名 \
  --episode 0
```

---

## 8. 故障排查

### 8.1 通信失败

| 症状 | 原因 | 解决 |
|---|---|---|
| "There is no status packet!" | 波特率 1Mbps 不可靠 | 改为 500000（见 3.2 节） |
| "Permission denied: /dev/ttyACM*" | 串口权限不足 | `sudo chmod 666 /dev/ttyACM*` 或加入 dialout 组 |
| 连接后无响应 | USB 线松动 | 重新插拔 USB |
| 升级 lerobot 后连不上 | 波特率被还原 | 重新修改 DEFAULT_BAUDRATE |

### 8.2 校准问题

| 症状 | 解决 |
|---|---|
| "Mismatch between calibration values" | 按 Enter 写入已有校准文件 |
| 校准文件找不到 | 确认 `--robot.id` / `--teleop.id` 正确；bi 模式自动拼接 `_left`/`_right` |
| 需要重新校准 | 按 `c` 进入交互式校准，或删除 `~/.cache/.../校准文件.json` 后重新运行 |

### 8.3 电机问题

| 症状 | 原因 | 解决 |
|---|---|---|
| "Overload error" | 关节受力过大触发保护 | 手动移到安全位 → 插拔 USB → 重写校准 |
| Missing motor ID 6 | 过载或通信异常掉线 | 插拔 USB → chmod → 重写校准 |
| 一条臂掉线影响另一条 | 双臂模式不会互相影响 | 只需恢复掉线臂 |

### 8.4 端口问题

| 症状 | 解决 |
|---|---|
| ttyACM 编号变了 | Python版用 by-id 不受影响；终端版用 `lerobot-find-port` 重新确认 |
| by-id 路径找不到 | `ls /dev/serial/by-id/` 检查，确认 USB 已插入 |
| video 编号变了 | 用相机识别 GUI 工具重新映射，或安装 udev 规则固定 |

### 8.5 训练问题

| 症状 | 解决 |
|---|---|
| "Output directory already exists" | 加 `--resume=true` 继续，或换 `--output_dir` 重新训练 |
| "command not found: lerobot-teleoperate" | `conda activate lerobot`；若仍不行，`cd ~/lerobot && pip install -e ".[feetech]"` |

---

## 9. 附录

### 9.1 API 版本差异速查（0.4.4 → 0.5.1）

| 变更项 | 旧版 (0.4.4) | 新版 (0.5.1) |
|---|---|---|
| motor 配置 | `{'name': (id, 'model')}` | `Motor(id, 'model', MotorNormMode.DEGREES)` |
| feetech 路径 | `lerobot.common.motors.feetech` | `lerobot.motors.feetech` |
| SO101 Robot | `SO101Robot` | `SOFollower` |
| SO101 Leader | 内置在 Robot | `SOLeader` (Teleoperator) |
| 遥操作命令 | `lerobot-control` | `lerobot-teleoperate` |
| 标定命令 | 内嵌于 connect | `lerobot-calibrate` 独立命令 |

### 9.2 架构说明

**Python版底层：**
```
teleoperate.py
├── 模式1: SO101Leader + SO101Follower          (一对一)
├── 模式2: SO101Leader + SO101Follower × 2      (一控多)
└── 模式3: SO101Leader × 2 + SO101Follower × 2  (双臂)
```

**终端版底层：**
```
lerobot-teleoperate CLI
├── 单臂: --robot.type so101_follower + --teleop.type so101_leader
└── 双臂: --robot.type bi_so_follower + --teleop.type bi_so_leader
    ├── BiSOFollower
    │   ├── left_arm: SOFollower  → 前缀 left_
    │   └── right_arm: SOFollower → 前缀 right_
    └── BiSOLeader
        ├── left_arm: SOLeader  → 前缀 left_
        └── right_arm: SOLeader → 前缀 right_
```

### 9.3 快速启动

```bash
# 1. 激活环境
conda activate lerobot

# 2. 校准（首次使用）
python 01_校准/calibrate_follower_left.py
python 01_校准/calibrate_follower_right.py
python 01_校准/calibrate_leader_left.py
python 01_校准/calibrate_leader_right.py

# 3. 遥操作
python 02_遥操作/teleoperate.py

# 4. 相机识别（可选）
python 04_摄像头工具/camera_identifier.py
```

### 9.4 参考资料

- [SO101通信失败修复记录](05_故障修复记录/SO101通信失败修复记录.md) — CH9101F 波特率问题完整排查
- [Seeed版LeRobot安装记录](06_环境安装记录/Seeed版LeRobot安装记录.md) — Seeed fork 0.4.3 安装与对比
- [USB端口映射表](01_校准/USB端口映射表.md) — by-id 端口详细映射
- [SO101工作总结](01_校准/SO101工作总结_20260417.md) — 2026-04-17 工作日志
- [HuggingFace LeRobot SO101 文档](https://huggingface.co/docs/lerobot/so101)
- [HuggingFace LeRobot GitHub](https://github.com/huggingface/lerobot)
