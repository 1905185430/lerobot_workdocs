# Agent Navigation Index

> 本文件供 AI Agent 快速定位相关文档，按关键词→文件路径映射
> 最后更新：2026-04-17

---

## 关键环境信息

| 项目 | 值 |
|------|-----|
| LeRobot官方版本 | 0.5.1 (conda env: `lerobot`, Python 3.12) |
| LeRobot-Seeed版本 | 0.4.4 (conda env: `lerobot-seeed`, Python 3.10) |
| SO101导入路径(v0.5.1) | `so_follower`, `so_leader` |
| SO101导入路径(v0.4.4) | `so101_follower`, `so101_leader` |
| 波特率 | 500000 (非默认1000000, CH9101F芯片需降低) |
| 摄像头索引 | TOP_CAM=10, WRIST_CAM=2, SIDE_CAM=18 |
| 从臂端口(by-id) | `/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B42073876-if00` |
| 主臂端口(by-id) | `/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B41533034-if00` |
| 校准ID | so101_cong_left, so101_cong_right, so101_zhu_left, so101_zhu_right |
| HF数据集 | Ready321/so101_grab_redcube (2cam), Ready321/so101_grab_redcube_3cam (3cam) |
| GitHub | 1905185430/lerobot_workdocs.git (branch main) |

---

## 关键词→文件映射

### 校准 / calibration

| 文件 | 路径 |
|------|------|
| 左从臂校准 | `01_SO101硬件与调试/01_校准/calibrate_follower_left.py` |
| 右从臂校准 | `01_SO101硬件与调试/01_校准/calibrate_follower_right.py` |
| 左主臂校准 | `01_SO101硬件与调试/01_校准/calibrate_leader_left.py` |
| 右主臂校准 | `01_SO101硬件与调试/01_校准/calibrate_leader_right.py` |
| USB端口映射 | `01_SO101硬件与调试/01_校准/USB端口映射表.md` |
| 校准JSON备份 | `01_SO101硬件与调试/calibration/` |

### 遥操作 / teleoperation

| 文件 | 路径 |
|------|------|
| 三模式遥操作(无摄像头) | `01_SO101硬件与调试/02_遥操作/teleoperate.py` |
| 双摄像头遥操作 | `01_SO101硬件与调试/02_遥操作/teleoperate_2cam.py` |
| 三摄像头遥操作 | `01_SO101硬件与调试/02_遥操作/teleoperate_3cam.py` |

### 数据采集 / recording

| 文件 | 路径 |
|------|------|
| 双摄像头采集 | `01_SO101硬件与调试/03_数据采集/record_so101_2cam.py` |
| 三摄像头采集 | `01_SO101硬件与调试/03_数据采集/record_so101_3cam.py` |

### 摄像头 / camera

| 文件 | 路径 |
|------|------|
| 相机识别GUI | `01_SO101硬件与调试/04_摄像头工具/camera_identifier.py` |
| 画面采集工具 | `01_SO101硬件与调试/04_摄像头工具/camera_capture.py` |

### 故障排查 / troubleshooting

| 问题 | 文件 |
|------|------|
| SO101通信失败(波特率) | `01_SO101硬件与调试/05_故障修复记录/SO101通信失败修复记录.md` |
| rerun-cli启动失败 | 用 `conda activate lerobot` 后运行脚本(不要用绝对python路径) |
| 摄像头index_or_path | 必须传字符串路径如`"/dev/video10"`, 不能传整数 |
| 摄像头fourcc报错 | 不要在OpenCVCameraConfig中指定fourcc |
| 数据集FileExistsError | 采集脚本已内置重复检测(--name/--overwrite/自动时间戳) |

### 模型训练 / training

| 文件 | 路径 |
|------|------|
| SmolVLA训练报告 | `02_模型训练与部署/SmolVLA训练部署工作报告_20260415.md` |
| PPIO训练指南 | `02_模型训练与部署/PPIO服务器LeRobot训练部署指南.md` |
| SmolVLA微调效果 | `03_技术调研/SmolVLA小数据集微调效果调研_20260415.md` |

### 模型部署 / deployment

| 文件 | 路径 |
|------|------|
| 本地部署评估 | `02_模型训练与部署/SmolVLA本地部署评估报告_20260415.md` |
| Jetson部署分析 | `03_技术调研/Jetson_AGX_Orin部署SmolVLA可行性分析.md` |
| whosricky模型参考 | `03_技术调研/SO-101_VLA部署指南_whosricky_svla_so101_pick_red_cube_2cam.md` |

### Jetson

| 文件 | 路径 |
|------|------|
| 连接与使用 | `05_Jetson使用/Jetson连接与使用教程.md` |
| 压测报告 | `05_Jetson使用/Jetson_Orin_AGX_压测报告_20260416.md` |
| 重启调查 | `05_Jetson使用/Jetson频繁重启调查报告_20260416.md` |

### 版本兼容 / compatibility

| 文件 | 路径 |
|------|------|
| 数据集版本兼容 | `03_技术调研/LeRobot数据集版本兼容性问题分析.md` |
| Seeed Fork兼容性 | `03_技术调研/SeeedStudio_Fork与官方LeRobot版本兼容性调查.md` |
| 教程对比 | `03_技术调研/Seeed_vs_LeRobot_SO101教程对比.md` |
| Seeed安装记录 | `01_SO101硬件与调试/06_环境安装记录/Seeed版LeRobot安装记录.md` |

### 学习 / learning

| 文件 | 路径 |
|------|------|
| 实验指导书(从零开始) | `01_SO101硬件与调试/SO101_实验指导书.md` |
| Transformer学习 | `03_技术调研/生成式AI学习/Transformer与经典AI架构学习指南.md` |
| VLA学习 | `03_技术调研/生成式AI学习/VLA视觉语言动作模型学习指南.md` |
| 扩散/流匹配学习 | `03_技术调研/生成式AI学习/流匹配与扩散模型学习指南.md` |

### Dobot Nova

| 文件 | 路径 |
|------|------|
| Nova系列调研 | `03_技术调研/Dobot越疆Nova系列/Dobot_Nova系列机械臂调研.md` |

---

## 踩坑速查

| 坑 | 解决方案 | 详情文件 |
|----|----------|----------|
| v0.5.1导入so_follower, v0.4.4导入so101_follower | 用对环境 | 05_故障修复记录/ |
| CH9101F 1Mbps丢包 | 波特率改为500000 | 05_故障修复记录/SO101通信失败修复记录.md |
| OpenCVCameraConfig index_or_path | 传字符串`"/dev/video10"`而非整数`10` | 04_摄像头工具/ |
| OpenCVCameraConfig fourcc | 不指定fourcc参数 | 04_摄像头工具/ |
| rerun RuntimeError | `conda activate lerobot`后运行脚本 | 02_遥操作/脚本注释 |
| 数据集名冲突 | 脚本自动加时间戳, 或--overwrite | 03_数据采集/ |
| SmolVLA需action expert | 模型需SmolVLM2-500M-Video-Instruct | 02_模型训练与部署/ |
| 海外服务器pip源 | 不用清华源, 直连PyPI | 通用规则 |
