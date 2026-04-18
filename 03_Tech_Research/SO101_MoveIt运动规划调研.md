# SO-101 MoveIt2 运动规划调研报告

> 调研日期：2026-04-15
> 硬件环境：SO-101 主臂 + 从臂（Feetech STS3215，波特率 500000）
> 目标：评估 SO-101 结合 MoveIt2 进行运动规划的可行性与现有开源方案

---

## 0. 核心结论

HuggingFace 官方 lerobot 框架**不含任何 ROS2/MoveIt 代码**（纯 Python ML 框架），所有 ROS2/MoveIt 集成均来自社区项目。整体生态处于早期阶段，尚无成熟的一站式方案，但已有若干可用项目。

---

## 1. 项目总览

按成熟度分三档：

### 1.1 TIER 1 — 最成熟/最推荐

| 项目 | Stars | ROS2 | 功能概述 |
|------|-------|------|----------|
| ycheng517/lerobot-ros | 181 | Jazzy | 通用 LeRobot-ROS2 框架，支持 MoveIt Servo 末端速度控制、ros2_control 关节控制、手柄/键盘遥操作 |
| nimiCurtis/so101_ros2 | 46 | Humble | 最完整的 SO-101 专属 ROS2 工作空间，含 URDF/网格/硬件接口/LeRobot桥接/遥操作，MoveIt 标注 WIP |
| MuammerBay/SO-ARM101_MoveIt_IsaacSim | 30 | Humble | MoveIt + Isaac Sim 双臂仿真，有 YouTube 视频教程，仅仿真 |

### 1.2 TIER 2 — 功能可用但较新

| 项目 | Stars | ROS2 | 功能概述 |
|------|-------|------|----------|
| Neoxra/lerobot-ros-moveit | 6 | Jazzy | 基于 lerobot-ros 加 MoveIt，C++ 硬件接口直连 Feetech 舵机，最完整的 SO-101+MoveIt 真机实现 |
| Architect-Labo/lerobot_ws | 0 | Jazzy | Docker 化部署，MoveIt + Gazebo Harmonic + RViz，含 lerobot_controller + lerobot_moveit 包 |
| Architect-Labo/so101_moveit | 0 | Jazzy | 上者的 Docker 封装，一键启动 |

### 1.3 TIER 3 — 配置包/早期项目

| 项目 | 说明 |
|------|------|
| EveW503/SO101_Moveit2 | MoveIt Setup Assistant 生成的配置包 |
| sahillathwal/so101_moveit_config | 同上 |
| piyaskheyal/so101_moveit2_config + description | 拆分的配置+描述包 |
| sourenpash/SOARM101-ROS2-HUMBLE-MOVEIT-PACKAGE | Humble MoveIt 配置 |
| Lavs-Daniels-Skots/so101-native-ubuntu-ros2-moveit | Jazzy 原生部署指南（进行中） |

---

## 2. 重点项目详细分析

### 2.1 ycheng517/lerobot-ros

- GitHub: https://github.com/ycheng517/lerobot-ros
- **定位**：通用框架，非 SO-101 专属，但 SO-101 是主要目标
- **控制模式**：
  - 关节位置控制：ros2_control (joint_trajectory_controller)
  - 末端速度控制：MoveIt Servo（实时 servo 模式）
  - 夹爪控制：ros2_control (Gripper Action Controller)
- **遥操作**：6-DoF 手柄 + 键盘
- **优点**：社区最大、最活跃，架构设计良好
- **不足**：需要自行适配 SO-101 的硬件接口

### 2.2 nimiCurtis/so101_ros2

- GitHub: https://github.com/nimiCurtis/so101_ros2
- 文档: https://so101-ros2.readthedocs.io/
- **包结构**：
  - so101_description — URDF、STL 网格、RViz 配置、USD (Isaac Sim)
  - so101_bringup — 启动文件
  - so101_controller — ROS2 控制
  - so101_hardware_interface — Feetech 舵机硬件接口
  - so101_ros2_bridge — LeRobot ↔ ROS2 桥接
  - so101_teleop — 遥操作
- **URDF 文件清单**（so101_description/urdf/）：
  - so101_new_calib.urdf
  - so101_new_calib.urdf.xacro
  - so101_new_calib.ros2_control.xacro
  - so101_new_calib_with_transmission.xacro（MoveIt/Gazebo 用）
  - meshes/ 目录含 STL 文件
- **MoveIt 状态**：README 标注 "work in progress"
- **优点**：SO-101 专属、URDF/网格最全、有硬件接口
- **不足**：MoveIt 部分未完成，需自行补全

### 2.3 MuammerBay/SO-ARM101_MoveIt_IsaacSim

- GitHub: https://github.com/MuammerBay/SO-ARM101_MoveIt_IsaacSim
- **特点**：MoveIt + Isaac Sim 双臂仿真，有完整的视频教程
- **局限**：目前仅仿真，Sim2Real 待实现
- **适合**：先在仿真中跑通 MoveIt 流程的学习路径

### 2.4 Neoxra/lerobot-ros-moveit

- GitHub: https://github.com/Neoxra/lerobot-ros-moveit
- **包结构**：
  - so101_hardware — C++ 硬件接口插件（Feetech STS3215）
  - so101_moveit — MoveIt2 配置 + 键盘遥操作
  - so101_description — URDF 机器人描述
  - lerobot_teleoperator_devices — 遥操作支持
- **亮点**：
  - C++ 硬件接口直连真机舵机
  - MoveIt 运动规划开箱可用
  - 含校准脚本 calibrate_and_install.sh
- **不足**：项目较新，文档少

### 2.5 Architect-Labo/lerobot_ws + so101_moveit

- GitHub: https://github.com/Architect-Labo/lerobot_ws (sts_servo 分支)
- GitHub: https://github.com/Architect-Labo/so101_moveit
- **特点**：Docker 化一键部署，MoveIt + Gazebo Harmonic + RViz
- **使用流程**：启动 lerobot_controller → 启动 lerobot_moveit → RViz 中用 OMPL 规划器规划+执行
- **依赖**：feetech_ros2_driver (Architect-Labo fork, auto_calib 分支)
- **不足**：真机控制仍为 TODO

---

## 3. URDF 资源汇总

最全的 URDF 资源在 nimiCurtis/so101_ros2：

```
so101_description/urdf/
├── so101_new_calib.urdf
├── so101_new_calib.urdf.xacro
├── so101_new_calib.ros2_control.xacro
├── so101_new_calib_with_transmission.xacro  ← MoveIt/Gazebo 需要这个
└── meshes/
    └── *.stl
```

其他项目的 URDF 多数基于此修改或用 MoveIt Setup Assistant 重新生成。

---

## 4. 其他相关工具

- **legalaspro/robokin** (10 stars)：URDF-based IK 辅助工具，支持 SO-101，可插拔 IK 后端
- **PathOn-AI/pathon_opensource** (100 stars)：硬件资源（6DoF 腕部升级 + 夹爪），非 ROS2

---

## 5. 选型建议

### 方案A：快速上手（推荐入门）
- 用 nimiCurtis/so101_ros2
- URDF/硬件接口/遥操作现成，MoveIt 部分自行补全
- 适合 ROS2 Humble 用户

### 方案B：直接要 MoveIt（推荐进阶）
- 用 Neoxra/lerobot-ros-moveit
- 开箱即用的 MoveIt + C++ 真机硬件接口
- 最省事，但项目较新可能需调试

### 方案C：仿真先行
- 用 MuammerBay/SO-ARM101_MoveIt_IsaacSim
- 先在 Isaac Sim 里跑通，再迁移真机
- 有视频教程，学习曲线平缓

### 方案D：Docker 一键部署
- 用 Architect-Labo/so101_moveit
- 环境隔离好，但真机控制未完成

---

## 6. 本地硬件注意事项

- 舵机型号：Feetech STS3215，波特率 **必须 500000**（CH9101F 芯片 1Mbps 不可靠）
- 串口：从臂 /dev/ttyACM0，主臂 /dev/ttyACM1
- 如果走 ROS2 硬件接口，需确认串口通信稳定性（参考 `01_SO101硬件与调试/SO101通信失败修复记录.md`）
- 串口权限：`sudo usermod -aG dialout $USER`（需重新登录）

---

## 7. 后续计划

- [ ] 选定方案，搭建 ROS2 + MoveIt 环境
- [ ] 验证 URDF 与真机关节映射是否正确
- [ ] 测试 MoveIt 运动规划在真机上的执行精度
- [ ] 记录踩坑过程，更新本文档
