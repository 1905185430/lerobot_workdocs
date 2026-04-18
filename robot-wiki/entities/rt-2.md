---
title: RT-2
created: 2026-04-18
updated: 2026-04-18
type: entity
tags: [model, architecture]
sources: [raw/articles/vla-guide-2026.md]
---

# RT-2

## 概述

RT-2 (Robotic Transformer 2) 是 Google DeepMind 于 2023 年发布的 [[vla|VLA]] 里程碑模型，首次证明了视觉-语言-动作端到端的可行性。

## 核心贡献

- 将大规模视觉-语言预训练与机器人控制统一
- 证明 Web 知识可以迁移到机器人操控任务
- 为后续 [[openvla|OpenVLA]]、[[smolvla|SmolVLA]] 等开源 VLA 奠定基础

## 发展脉络

```
RT-1 (2022/2023) → RT-2 (2023) → RT-X (2023, 跨实体)
```

- **RT-1**：纯视觉输入的机器人 Transformer
- **RT-2**：加入视觉-语言理解，本质上是 VLA
- **RT-X**：跨实体机器人控制

## 关键论文

- **RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control** (2023) — https://arxiv.org/abs/2307.15818

## 相关概念

- [[vla|VLA]] — RT-2 首次定义的模型范式
- [[openvla|OpenVLA]] — RT-2 的开源复现
- [[transformer-architecture|Transformer]] — RT-2 的基础架构
