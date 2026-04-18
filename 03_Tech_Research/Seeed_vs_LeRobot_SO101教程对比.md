# Seeed Studio vs LeRobot 官方教程 — SO-101 机械臂差异对比

> 对比日期：2026-04-15
> Seeed 教程来源：https://wiki.seeedstudio.com/lerobot_so100m_new/
> LeRobot 官方教程：https://huggingface.co/docs/lerobot/so101 + il_robots + installation

---

## 一、核心差异总览

### 1. 源码仓库不同

| 项目 | LeRobot 官方 | Seeed Studio |
|------|-------------|--------------|
| 仓库地址 | `https://github.com/huggingface/lerobot.git` | `https://github.com/Seeed-Projects/lerobot.git` |
| 说明 | 主分支，可能有 breaking changes | Seeed 维护的 fork，声称是"验证稳定的版本" |

### 2. Python 版本

| 项目 | LeRobot 官方 | Seeed Studio |
|------|-------------|--------------|
| Python 版本 | >= 3.12 | 3.10 |

说明：Seeed 教程还在用 3.10，官方新版已要求 3.12+。

### 3. Seeed 独有的 Seeed_RoboController 工具

- 官方教程没有这个工具
- Seeed 额外提供 `Seeed_RoboController`
  - 仓库：https://github.com/Seeed-Projects/Seeed_RoboController
  - 用途：舵机"中位校准"，解决 `Magnitude exceeds 2047` 报错
- 如果在校准时遇到这个报错，Seeed 的工具可以救命

### 4. 电压警告（Seeed 独有）

- Arm Kit Standard = 仅 5V
- Arm Kit Pro = Leader 5V + Follower 12V
- **接错电压会烧电机！** 官方教程没有特别强调这个

### 5. SO-ARM101 硬件改进（Seeed 独有说明）

- 改进了接线（Joint 3 不再断连）
- 优化了 Leader 臂齿轮比：

| Leader 臂关节 | 电机 | 齿轮比 |
|--------------|------|--------|
| Base / Shoulder Pan | 1 | 1:191 |
| Shoulder Lift | 2 | 1:345 |
| Elbow Flex | 3 | 1:191 |
| Wrist Flex | 4 | 1:147 |
| Wrist Roll | 5 | 1:147 |
| Gripper | 6 | 1:147 |

- 支持实时 Leader-follows-Follower 功能

### 6. DepthCameraSupport 分支（Seeed 独有）

- Seeed 维护了一个带深度相机支持的分支
- 支持 RealSense D435i/D405 和 Orbbec Gemini2/336
- 官方主线目前没有深度相机集成

### 7. 依赖版本锁定（Seeed 独有）

Seeed 锁定了几个关键版本：
- `rerun-sdk==0.23`
- `pynput==1.6.8`
- `datasets==2.19`

官方教程没有特别指定这些版本。

### 8. Jetson 平台支持（Seeed 更详细）

- Seeed 提供了 Jetson JetPack 6.0/6.1 的 OpenCV/numpy workaround
- 额外有 GR00T N1.5 在 Jetson Thor 上的独立教程
- 官方教程主要面向 x86 + CUDA

---

## 二、训练模型范围差异

### LeRobot 官方教程

- 主要讲解 ACT (300k steps)
- 提到 SmolVLA
- Google Colab 训练选项

### Seeed 教程

- ACT (300k steps)
- SmolVLA (20k steps)
- Pi0 (20k steps)
- Pi0.5 (3k steps)
- GR00T N1.5 (需 flash-attn)
- PEFT/LoRA 支持
- 多 GPU (accelerate)
- 异步推理 (async inference server/client)

**说明**：Seeed 在训练模型种类和部署方式上覆盖更广。

---

## 三、基础流程一致性

以下步骤两边基本一致，SO-100/SO-101 代码完全兼容：

- `lerobot-setup-motors` — 电机ID/波特率配置
- `lerobot-calibrate` — 校准
- `lerobot-teleoperate` — 遥操作
- `lerobot-record` — 数据录制
- `lerobot-train` — 训练
- `lerobot-record --policy.path` — 部署/评估

---

## 四、Seeed 额外相关资源

- SO-ARM101 RynnBot Developer Kit：https://wiki.seeedstudio.com/lerobot_soarm101_Rynnbot_Developer_Kit/
- Fine-tune GR00T N1.5 for LeRobot SO-101 Arm on Jetson Thor：https://wiki.seeedstudio.com/fine_tune_gr00t_n1.5_for_lerobot_so_arm_and_deploy_on_jetson_thor/
- Lerobot Dataset Tool：https://wiki.seeedstudio.com/lerobot_dataset_tool/

---

## 五、对当前环境的建议

基于我们的实际使用情况（官方 huggingface/lerobot 仓库、波特率已改 500000、有 Orbbec 深度相机）：

1. **Orbbec 深度相机集成**：关注 Seeed 的 DepthCameraSupport 分支，官方主线暂无深度相机支持
2. **校准报错**：如果遇到 `Magnitude exceeds 2047`，用 Seeed_RoboController 工具
3. **git pull 冲突**：Seeed 的 fork 可能和我们的波特率修改冲突，pull 时注意 `feetech.py` 的 `DEFAULT_BAUDRATE`
4. **训练选择**：Seeed 教程提供了更多模型（Pi0, GR00T N1.5），值得参考
5. **Python 版本**：建议跟官方走 3.12+，Seeed 的 3.10 已过时
