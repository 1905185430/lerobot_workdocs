---
title: VLA (视觉-语言-动作模型)
created: 2026-04-18
updated: 2026-04-18
type: concept
tags: [architecture, model, fine-tuning, deployment]
sources: [raw/articles/vla-guide-2026.md, raw/articles/flow-matching-diffusion-guide-2026.md]
---

# VLA (视觉-语言-动作模型)

## 定义

VLA = Vision-Language-Action Model，用预训练的视觉-语言模型理解世界，然后直接输出机器人控制动作。

```
输入：视觉 (摄像头图像) + 语言 (任务指令) + 状态 (机器人关节角度)
输出：动作 (末端执行器位姿 / 关节角度 / 夹爪开合)
```

## 发展脉络

```
2021-2022 萌芽期：CLIPort, RT-1, Flamingo
2023 爆发期：  RT-2, PaLM-E, LLaVA, π0 雏形
2024 成熟期：  OpenVLA, π0, GR00T, RDT-1B
2025 落地期：  商业 VLA, 家庭/工业场景部署
```

## VLA vs VLM

| 特性 | VLM | VLA |
|------|-----|-----|
| 输入 | 图像 + 文本 | 图像 + 文本 + 机器人状态 |
| 输出 | 文本描述 | 机器人动作 |
| 训练数据 | 图文对 | 机器人演示轨迹 |
| 应用 | 视觉问答 | 机器人操控 |

## 核心模型

- [[rt-2|RT-2]] — VLA 里程碑，Google DeepMind
- [[openvla|OpenVLA]] — 开源 VLA，7B 参数
- [[smolvla|SmolVLA]] — 轻量级 VLA，适合边缘部署

## 动作空间设计

- 末端执行器位姿 (6D: position + rotation)
- 关节角度 (DOF 数量)
- 增量动作 (delta position/velocity)
- 混合动作 (语言 + 视觉 + 动作)

## 动作分块 (Action Chunking)

VLA 输出一系列未来动作（chunk），而非单步动作。例如预测未来 16 步动作，提高动作平滑性，减少时延。详见 [[imitation-learning|模仿学习]]。

## 部署路径

1. 用 [[lerobot|LeRobot]] 框架采集演示数据
2. 基于 [[smolvla|SmolVLA]] 或 [[openvla|OpenVLA]] 微调
3. 在边缘设备（Jetson）上推理

## 相关概念

- [[transformer-architecture|Transformer]] — VLA 的基础架构
- [[imitation-learning|模仿学习]] — VLA 的训练范式
- [[diffusion-models|扩散模型]] — 可用于 VLA 的动作生成
- [[so101|SO-101]] — 常用的 VLA 部署硬件平台
