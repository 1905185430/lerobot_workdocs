# VLA (视觉-语言-动作模型) 学习指南

> 更新时间：2026-04-16

---

## 一、什么是 VLA？

**VLA = Vision-Language-Action Model**

核心理念：用预训练的视觉-语言模型理解世界，然后直接输出机器人控制动作。

```
输入
├── 视觉 (摄像头图像)
├── 语言 (任务指令，如"把红色方块放到绿色方块旁边")
└── 状态 (机器人当前关节角度)

输出
└── 动作 (末端执行器位姿 / 关节角度 / 夹爪开合)
```

---

## 二、VLA 发展脉络

```
2021-2022: 萌芽期
├── CLIP as Roboteer (CLIPort) - 视觉-语言到机器人控制
├── RT-1 (Google) - 首批大规模机器人演示数据训练
└── Flamingo (DeepMind) - 多模态大模型启发

2023: 爆发期
├── RT-2 (Google DeepMind) - VLA 里程碑
├── PaLM-E (Google) - LLM 驱动的具身智能
├── LLaVA - 开源视觉-语言模型
├── InstructBLIP - 指令微调 VLM
└── π0 雏形 (Physical Intelligence)

2024: 成熟期
├── OpenVLA - 开源 VLA (7B 参数)
├── π0 (Physical Intelligence) - 通用机器人控制
├── GR00T (NVIDIA) - 人形机器人基础模型
├── RDT-1B (阿里巴巴) - 模仿学习
├── LLAMA-VID / LongVA - 长上下文 VLM
└── 各大厂商 VLA 竞品

2025: 落地期
├── 各大机器人公司发布商业 VLA
├── 家庭服务机器人应用
└── 工业场景规模化部署探索
```

---

## 三、经典论文

### 3.1 必读论文

| 论文 | 年份 | 链接 | 说明 |
|------|------|------|------|
| **RT-2** | 2023 | https://arxiv.org/abs/2307.15818 | VLA 里程碑，视觉-语言-动作端到端 |
| **PaLM-E** | 2023 | https://arxiv.org/abs/2301.02285 | LLM 驱动的具身智能 |
| **RT-1** | 2023 | https://arxiv.org/abs/2212.09816 | RT-2 前身，大规模演示数据 |
| **CLIPort** | 2022 | https://arxiv.org/abs/2109.12098 | CLIP 迁移到机器人控制 |
| **Flamingo** | 2022 | https://arxiv.org/abs/2204.14198 | DeepMind 多模态模型 |

### 3.2 开源 VLA 模型

| 论文 | 年份 | 链接 | 说明 |
|------|------|------|------|
| **OpenVLA** | 2024 | https://arxiv.org/abs/2401.12254 | 开源 VLA，7B 参数，97k 机器人演示 |
| **LLaVA** | 2023 | https://arxiv.org/abs/2304.08485 | 开源 LMM，VLA 视觉基座 |
| **LLaVA-1.5** | 2023 | 改进版 | 更强的视觉理解 |
| **π0** | 2024 | https://physicalintelligence.github.io/blog/ | Physical Intelligence 通用控制 |
| **GR00T** | 2024 | NVIDIA 官方 | 人形机器人基础模型 |

### 3.3 具身智能相关

| 论文 | 年份 | 链接 | 说明 |
|------|------|------|------|
| **VoxPoser** | 2023 | https://arxiv.org/abs/2307.05952 | LLM 合成机器人轨迹 |
| **Inner Monologue** | 2023 | https://arxiv.org/abs/2307.07646 | 视觉-语言规划 |
| **RT-X** | 2023 | Google | 跨实体机器人控制 |
| **ACT** | 2023 | https://github.com/tonyzhaozh/act | 动作分块 transformer |

---

## 四、GitHub 代码仓库

### 4.1 主流 VLA 仓库

| 仓库 | Stars | 链接 | 说明 |
|------|-------|------|------|
| **openvla/openvla** | ⭐2.4k | https://github.com/openvla/openvla | 必学！开源 VLA 实现 |
| **haotian-liu/LLaVA** | ⭐32k | https://github.com/haotian-liu/LLaVA | 开源 LMM 基座 |
| **google-research/robotics_transformers** | - | Google 官方 | RT 系列实现 |
| **tonyzhaozh/act** | ⭐5k | https://github.com/tonyzhaozh/act | ACT 算法，模仿学习 |
| **Physical-Intelligence/pi0** | - | https://github.com/Physical-Intelligence/pi0 | π0 模型 |

### 4.2 LeRobot 中的 VLA

| 仓库 | 说明 |
|------|------|
| **lerobot** | HuggingFace LeRobot 框架，支持 VLA 策略 |
| **SmolVLA** | 轻量级 VLA，用于 SO-101 机械臂 |

### 4.3 其他相关

| 仓库 | 说明 |
|------|------|
| **step1x-ai/Step1X-VLA** | 3B 参数 VLA 模型 |
| **Project-Seeed/SmolVLA** | Seeed 优化的 SmolVLA |

---

## 五、学习路线图

```
第一阶段：基础概念
│
├─ 1. 理解 VLM (视觉-语言模型)
│   ├─ CLIP 原理
│   ├─ LLaVA 架构
│   └─ 指令微调 (Instruction Tuning)
│
├─ 2. 机器人控制基础
│   ├─ 逆运动学 (IK)
│   ├─ 末端执行器控制
│   └─ 关节空间控制
│
└─ 3. 模仿学习 (Imitation Learning)
    ├─ 行为克隆 (BC)
    ├─ DAgger
    └─ 动作分块 (Action Chunking)

第二阶段：VLA 核心
│
├─ 4. RT-2 论文精读
├─ 5. OpenVLA 架构解析
└─ 6. 动作空间设计 (Action Head)

第三阶段：实战
│
├─ 7. LeRobot 框架使用
├─ 8. VLA 微调 (SmolVLA / OpenVLA)
└─ 9. 机器人遥操作数据采集
```

---

## 六、学习资源

### 6.1 官方文档

| 资源 | 链接 |
|------|------|
| **HuggingFace VLA 文档** | https://huggingface.co/docs/transformers/en/model_doc/vla |
| **OpenVLA 文档** | https://openvla.readthedocs.io/ |
| **LeRobot 文档** | https://lerobot.github.io/ |

### 6.2 博客教程

| 博客 | 链接 |
|------|------|
| **Google DeepMind RT-2 Blog** | https://deepmind.google/discover/blog/rt-2/ |
| **Physical Intelligence Blog** | https://physicalintelligence.github.io/blog/ |
| **Lil'Log VLA 相关** | https://lilianweng.github.io/ |
| **Jay Alammar LLaVA 图解** | http://jalammar.github.io/ |

### 6.3 视频课程

| 资源 | 链接 |
|------|------|
| **Stanford CS231N** | http://cs231n.stanford.edu/ |
| **CS 330 (Meta Learning)** | 含 VLA 内容 |
| **Yannic Kilcher YouTube** | 搜索 VLA 论文解读 |

### 6.4 数据集

| 数据集 | 说明 |
|--------|------|
| **Open X-Embodiment** | 100+ 机器人数据集，RT-X 发布 |
| **BridgeData V2** | 机器人家务数据 |
| **SO-101 数据** | LeRobot 采集的演示数据 |

---

## 七、核心概念解释

### 7.1 VLA vs VLM

| 特性 | VLM | VLA |
|------|-----|-----|
| 输入 | 图像 + 文本 | 图像 + 文本 + 机器人状态 |
| 输出 | 文本描述 | 机器人动作 (关节角度/末端位姿) |
| 训练数据 | 图文对 | 机器人演示轨迹 |
| 应用 | 视觉问答、图像描述 | 机器人操控 |

### 7.2 动作空间设计

```
动作空间类型：
├── 末端执行器位姿 (6D: position + rotation)
├── 关节角度 (DOF 数量)
├── 增量动作 (delta position/velocity)
└── 混合动作 (语言 + 视觉 + 动作)
```

### 7.3 动作分块 (Action Chunking)

- VLA 输出的是一系列未来动作 (chunk)
- 例如：预测未来 16 步动作
- 提高动作平滑性，减少时延

---

## 八、FAQ

**Q: VLA 和 RT-1/RT-2 是什么关系？**
> RT-1 是 Google 的早期机器人 Transformer (纯视觉输入)，RT-2 是升级版，加入了视觉-语言理解，本质上就是 VLA。

**Q: VLA 需要多少机器人数据？**
> OpenVLA 使用了 97k 条演示数据，π0 使用了数百万条。数据量越大泛化能力越强。

**Q: VLA 在机器人领域的前景？**
> VLA 是具身智能的核心方向之一。2024-2025 年各大公司都在投入，商业化前景明确。

**Q: 如何在自己的机器人上部署 VLA？**
> 1. 用 LeRobot 框架
> 2. 基于 OpenVLA 或 SmolVLA 微调
> 3. 采集少量演示数据
> 4. 在边缘设备 (Jetson) 推理

---

## 九、与本项目的关联

```
VLA 学习
├── LeRobot 框架 (你的机器人实验环境)
│   ├── 支持 VLA 策略 (SmolVLA, ACT, etc.)
│   └── 遥操作数据采集
├── SO-101 机械臂
│   ├── 可用 VLA 控制
│   └── 需要视觉传感器 (Orbbec 深度相机)
├── SmolVLA 微调 (你已有经验)
│   └── 轻量级 VLA，适合边缘部署
└── NVIDIA GR00T
    └── 人形机器人基础模型 (前沿方向)
```

---

## 十、参考资料

1. Brohan et al. "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control" (2023)
2. Driess et al. "PaLM-E: An Embodied Multimodal Language Model" (2023)
3. Team et al. "OpenVLA: Open Vision-Language-Action Model" (2024)
4. Zhaozh et al. "ACT: Action Chunks with Transformers"
5. Ouyang et al. "LLaVA: Large Language and Vision Assistant" (2023)
