---
title: 模仿学习
created: 2026-04-18
updated: 2026-04-18
type: concept
tags: [training, rl]
sources: [raw/articles/vla-guide-2026.md]
---

# 模仿学习 (Imitation Learning)

## 定义

模仿学习是一种通过观察专家演示来学习策略的方法，无需手动设计奖励函数。是 [[vla|VLA]] 模型的主要训练范式。

## 核心方法

- **行为克隆 (Behavior Cloning, BC)**：最简单的方法，直接学习 state → action 映射
- **DAgger**：迭代式数据集聚合，解决分布偏移问题
- **动作分块 (Action Chunking)**：预测未来多步动作，提高平滑性

## 与 [[vla|VLA]] 的关系

VLA 本质上是模仿学习的一种实现：
1. 用遥操作采集专家演示数据
2. 训练模型从 (视觉, 语言, 状态) 预测动作
3. 部署时模型模仿专家行为

## 数据采集

使用 [[so101|SO-101]] 等机械臂通过 [[lerobot|LeRobot]] 框架进行遥操作采集。数据量需求：
- OpenVLA：97k 条演示
- π0：数百万条
- [[smolvla|SmolVLA]]：小数据集（50-100 条演示）即可微调

## 关键挑战

- **分布偏移**：训练时的状态分布与部署时不同
- **多模态动作**：同一状态可能有多种正确动作
- **长期推理**：BC 缺乏规划能力

## 相关概念

- [[vla|VLA]] — 模仿学习在机器人控制中的应用
- [[so101|SO-101]] — 常用的遥操作数据采集硬件
- [[lerobot|LeRobot]] — 支持模仿学习训练的框架
