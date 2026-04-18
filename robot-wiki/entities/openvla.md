---
title: OpenVLA
created: 2026-04-18
updated: 2026-04-18
type: entity
tags: [model, open-source, fine-tuning]
sources: [raw/articles/vla-guide-2026.md]
---

# OpenVLA

## 概述

OpenVLA 是一个开源 [[vla|VLA]] 模型，7B 参数，使用 97k 机器人演示数据训练。是 VLA 领域的重要开源基准。

## 架构

- 基于大型视觉-语言模型
- Action Head 输出机器人动作
- 支持多种机器人平台

## 关键论文

- **OpenVLA: Open Vision-Language-Action Model** (2024) — https://arxiv.org/abs/2401.12254

## 与 [[smolvla|SmolVLA]] 的对比

| 特性 | OpenVLA | SmolVLA |
|------|---------|---------|
| 参数量 | 7B | ~500M |
| 数据需求 | 97k+ 演示 | 50-100 演示可微调 |
| 边缘部署 | 困难（需量化） | 友好 |
| 泛化能力 | 强 | 单任务为主 |

## 代码仓库

- https://github.com/openvla/openvla (2.4k stars)

## 相关概念

- [[vla|VLA]] — OpenVLA 所属的模型类别
- [[smolvla|SmolVLA]] — OpenVLA 的轻量替代
- [[rt-2|RT-2]] — OpenVLA 的商业对标
