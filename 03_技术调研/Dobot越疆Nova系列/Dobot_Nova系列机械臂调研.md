# Dobot 越疆 Nova 系列机械臂调研

> 日期：2026-04-16
> 分类：技术调研
> 状态：初稿

---

## 一、核心结论

Dobot Nova系列是越疆机器人面向商业场景的六轴协作机械臂，包含Nova2（2kg负载）和Nova5（5kg负载）两个型号。与CR系列相比，Nova系列更轻更小，支持TCP/IP和ROS2控制，官方在GitHub的Dobot-Arm组织下提供完整的Python SDK和ROS2驱动。**Nova系列使用V3版本的TCP/IP协议和ROS2包，而非最新的V4版本（V4仅支持CRA/E6）。**

---

## 二、产品线概览

Nova系列是Dobot（越疆机器人）面向商业轻量场景的协作机械臂产品线，定位比CR系列更轻便、更紧凑，适合餐饮、零售、理疗等场景。

### 2.1 型号对比

| 参数 | Nova2 | Nova5 |
|------|-------|-------|
| 负载 | 2 kg | 5 kg |
| 臂展（最大可达半径） | 625 mm | 850 mm |
| 重复定位精度 | ±0.02 mm | ±0.02 mm |
| 自重 | ~4.5 kg | ~7 kg |
| 自由度 | 6 | 6 |
| 控制箱 | 掌上型（Palm-sized） | 掌上型（Palm-sized） |
| 供电 | 24V DC | 24V DC |
| 通信接口 | TCP/IP（以太网）| TCP/IP（以太网）|
| 安全特性 | 5级可调碰撞保护、人体感应、断电姿态保持 | 同左 |
| 外壳定制 | 支持颜色定制 | 支持颜色定制 |

> 注：Nova2自重比CR3轻33%-44%，体积小20%；Nova5比CR5轻33%-44%。精确参数以官方Specs页为准，官网规格数据为动态加载，建议下载产品手册确认。

### 2.2 核心特性

- **超轻便携**：占用仅1m²空间，控制箱掌上大小，无需改造场地
- **零门槛编程**：支持轨迹回放和图形化编程，无需编码经验
- **安全协作**：5级可调碰撞检测，0.01秒内停止；人体运动感应；断电姿态保持
- **外观定制**：外壳颜色可定制，适配品牌风格

### 2.3 官方链接

- 官网产品页：https://www.dobot-robots.com/products/nova-series/dobot-nova-series.html
- 官网下载中心：https://www.dobot-robots.com/service （Download Center）
- 官网Academy：https://www.dobot-robots.com/service/academy
- 邮箱：sales@dobot-robots.com

---

## 三、通信协议与SDK

### 3.1 TCP/IP协议（核心控制方式）

Nova系列通过以太网TCP/IP协议进行控制，连接方式：

- **有线连接LAN1**：控制器IP为 192.168.5.1
- **有线连接LAN2**：控制器IP为 192.168.100.1
- **无线连接**：控制器IP为 192.168.1.6

连接前需确保电脑与控制器在同一网段，先用ping测试连通性。

### 3.2 协议版本说明（重要）

Dobot六轴机械臂有两代TCP/IP协议：

| 版本 | 适用产品 | Nova支持 |
|------|---------|---------|
| V3 | CR系列、Nova系列 | **是** |
| V4 | CRA系列、E6系列 | **否** |

**Nova系列必须使用V3版本**的协议和SDK。V4版本的仓库（TCP-IP-Python-V4、DOBOT_6Axis_ROS2_V4）仅支持CRA/E6，不适用Nova。

### 3.3 Python SDK使用

仓库：[Dobot-Arm/TCP-IP-Python-V3](https://github.com/Dobot-Arm/TCP-IP-Python-V3)（34 stars, MIT协议）

**依赖**：Python 3.x，无需额外pip包（纯socket通信）

**基本用法**：
```python
from dobot_api import DobotApi

# 连接机械臂
ip = "192.168.5.1"  # LAN1口
port = 29999        # 命令端口
api = DobotApi(ip, port)

# 使能机器人
api.SendCmd("EnableRobot()")

# 关节运动
api.SendCmd("MovJ(0,0,0,0,0,0)")

# 直线运动
api.SendCmd("MovL(100,200,300,180,0,0)")

# 获取当前位姿
result = api.SendCmd("GetPose()")
```

**注意**：固件版本需V3.5.5.0以上。

---

## 四、ROS2支持

### 4.1 官方ROS2包（V3版）

仓库：[Dobot-Arm/DOBOT_6Axis_ROS2_V3](https://github.com/Dobot-Arm/DOBOT_6Axis_ROS2_V3)（35 stars）

支持型号：CR3/CR5/CR7/CR10/CR12/CR16/Nova2/Nova5

包含的MoveIt配置：
- `nova2_moveit/` — Nova2的MoveIt2配置
- `nova5_moveit/` — Nova5的MoveIt2配置
- `dobot_bringup_v3/` — 启动文件
- `dobot_gazebo/` — Gazebo仿真
- `dobot_demo/` — 示例程序
- `dobot_msgs_v3/` — 自定义消息
- `servo_action/` — Servo模式

### 4.2 ROS1支持

仓库：[Dobot-Arm/TCP-IP-ROS-6AXis](https://github.com/Dobot-Arm/TCP-IP-ROS-6AXis)（41 stars, MIT协议）

支持CRA/CR/E6/Nova全系列ROS1驱动，C++实现。

---

## 五、GitHub开源项目汇总

### 5.1 官方仓库（Dobot-Arm组织，466 followers，39个仓库）

与Nova系列直接相关的官方仓库：

| 仓库 | 描述 | 语言 | Stars | 适用版本 |
|------|------|------|-------|---------|
| [TCP-IP-ROS-6AXis](https://github.com/Dobot-Arm/TCP-IP-ROS-6AXis) | CRA/CR/E6/Nova ROS1驱动 | C++ | 41 | V3 |
| [DOBOT_6Axis_ROS2_V3](https://github.com/Dobot-Arm/DOBOT_6Axis_ROS2_V3) | CR/Nova ROS2驱动+MoveIt | Python | 35 | V3 |
| [TCP-IP-Python-V3](https://github.com/Dobot-Arm/TCP-IP-Python-V3) | CR/Nova Python TCP/IP SDK | Python | 34 | V3 |
| [TCP-IP-Protocol-6AXis-V3](https://github.com/Dobot-Arm/TCP-IP-Protocol-6AXis-V3) | CR/Nova TCP/IP协议文档 | - | 14 | V3 |

**注意**：以下V4版本仓库**不适用**Nova系列：
- DOBOT_6Axis_ROS2_V4（76 stars）— 仅CRA/E6
- TCP-IP-Python-V4（61 stars）— 仅CRA/E6

### 5.2 社区开源项目

| 仓库 | 描述 | 语言 | Stars |
|------|------|------|-------|
| [emusman-lab/dual_robot_arm](https://github.com/emusman-lab/dual_robot_arm) | 双Nova5臂Isaac Sim 4.2.0仿真+MoveIt2 | Python | 5 |
| [Kwon-Hyun/Nova5](https://github.com/Kwon-Hyun/Nova5) | Nova5+Realsense深度相机QR码检测解码 | Jupyter | 5 |
| [huahaizo/Dobot-ROS2-Dobot-Nova5](https://github.com/huahaizo/Dobot-ROS2-Dobot-Nova5) | Nova5手势跟随+Qt GUI+Python API | C | 2 |
| [adeel1608/dobot-nova5-barns](https://github.com/adeel1608/dobot-nova5-barns) | Nova5咖啡自动化系统 | C++ | 1 |
| [zylovexyddcoco/Dobot-Nova5-Controll-and-Calibration](https://github.com/zylovexyddcoco/Dobot-Nova5-Controll-and-Calibration) | Nova5控制与标定 | - | - |

### 5.3 官方其他相关仓库

| 仓库 | 描述 | Stars |
|------|------|-------|
| [DOBOT_6Axis_ROS2_V4](https://github.com/Dobot-Arm/DOBOT_6Axis_ROS2_V4) | CRA/E6 ROS2 V4版（参考架构） | 76 |
| [TCP-IP-Python-V4](https://github.com/Dobot-Arm/TCP-IP-Python-V4) | CRA/E6 Python V4版（参考API设计） | 61 |
| [TCP-IP-Protocol-4AXis](https://github.com/Dobot-Arm/TCP-IP-Protocol-4AXis) | MG400/M1Pro四轴协议 | 64 |
| [TCP-IP-4Axis-Python](https://github.com/Dobot-Arm/TCP-IP-4Axis-Python) | MG400/M1Pro Python SDK | 26 |

---

## 六、快速上手指南

### 6.1 硬件连接

1. 将网线连接电脑和Nova控制器LAN1口
2. 设置电脑有线网络IP为 192.168.5.x（x≠1），子网掩码 255.255.255.0
3. ping 192.168.5.1 确认连通

### 6.2 Python控制

```bash
# 克隆SDK
git clone https://github.com/Dobot-Arm/TCP-IP-Python-V3.git
cd TCP-IP-Python-V3

# 运行示例
python main.py
# 或运行带GUI的版本
python main_UI.py
```

### 6.3 ROS2控制

```bash
# 克隆ROS2包
git clone https://github.com/Dobot-Arm/DOBOT_6Axis_ROS2_V3.git

# 编译（以Nova5为例）
cd DOBOT_6Axis_ROS2_V3
colcon build --packages-select nova5_moveit dobot_bringup_v3 dobot_msgs_v3

# 启动
source install/setup.bash
ros2 launch dobot_bringup_v3 dobot_bringup.launch.py robot_type:=nova5
```

---

## 七、与SO-101的对比

| 维度 | Dobot Nova5 | SO-101 |
|------|------------|--------|
| 类型 | 工业协作臂 | 开源学习臂 |
| 负载 | 5 kg | ~0.5 kg |
| 精度 | ±0.02 mm | 较低 |
| 驱动 | 关节电机+减速器 | 舵机 |
| 通信 | TCP/IP以太网 | 串口UART |
| 控制方式 | 逆运动学/关节空间 | 关节空间 |
| 价格 | ~3-5万人民币 | ~数千元 |
| 生态 | 商业闭源，SDK开源 | LeRobot开源生态 |
| 适合场景 | 工业/商业应用 | 学习/研究/VLA |

---

## 八、注意事项与踩坑

1. **协议版本**：Nova系列只能用V3版SDK和ROS2包，V4不支持Nova
2. **固件版本**：需V3.5.5.0以上才能使用Python SDK
3. **网络配置**：控制器默认IP因LAN口不同而不同，注意区分LAN1(192.168.5.1)和LAN2(192.168.100.1)
4. **ROS2版本**：官方V3包适配Humble，使用前确认ROS2版本兼容性
5. **MoveIt配置**：nova2_moveit和nova5_moveit配置已包含在官方仓库中，无需自己配置URDF
6. **与LeRobot集成**：Nova系列使用TCP/IP控制，与LeRobot的串口通信方式不同，若要接入LeRobot需自行开发通信适配层

---

## 九、参考资料

- Dobot官网：https://www.dobot-robots.com
- Dobot-Arm GitHub组织：https://github.com/Dobot-Arm
- TCP-IP-Python-V3 README：https://github.com/Dobot-Arm/TCP-IP-Python-V3/blob/main/README.md
- DOBOT_6Axis_ROS2_V3 README：https://github.com/Dobot-Arm/DOBOT_6Axis_ROS2_V3
