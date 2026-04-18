---
title: LeRobot 框架
created: 2026-04-18
updated: 2026-04-18
type: entity
tags: [framework, open-source, training, dataset]
sources: [raw/articles/vla-guide-2026.md, raw/articles/so101-baudrate-fix-2026.md]
---

# LeRobot 框架

## 概述

LeRobot 是 HuggingFace 开源的机器人学习框架，提供从数据采集到模型训练、评估、部署的全流程工具链。是 [[vla|VLA]] 模型训练和部署的主要框架。

## 核心功能

- **遥操作数据采集**：通过 `lerobot-teleoperate` 进行主从遥操作
- **机器人校准**：通过 `lerobot-calibrate` 校准机械臂
- **策略训练**：支持 ACT、Diffusion Policy、[[smolvla|SmolVLA]] 等策略
- **数据集管理**：HuggingFace Hub 数据集上传/下载
- **推理部署**：本地和边缘设备推理

## 版本说明

- **官方 lerobot (v0.5.1)**：支持 bi_so_follower/bi_so_leader 双臂模块，Python 3.12
- **lerobot-seeed (v0.4.4)**：Seeed Studio fork，支持 SmolVLA，但不含双臂模块

## 关键命令

```bash
lerobot-calibrate    # 校准机械臂
lerobot-teleoperate  # 遥操作
lerobot-record       # 录制数据集
lerobot-train        # 训练策略
lerobot-eval         # 评估策略
```

## 相关概念

- [[so101|SO-101]] — LeRobot 官方支持的机械臂
- [[smolvla|SmolVLA]] — LeRobot 支持的 VLA 策略
- [[vla|VLA]] — LeRobot 训练的模型类型
- [[imitation-learning|模仿学习]] — LeRobot 的训练范式
