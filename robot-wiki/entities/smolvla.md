---
title: SmolVLA
created: 2026-04-18
updated: 2026-04-18
type: entity
tags: [model, fine-tuning, deployment, open-source]
sources: [raw/articles/vla-guide-2026.md]
---

# SmolVLA

## 概述

SmolVLA 是一个轻量级 [[vla|VLA]] 模型，专为资源受限的边缘设备设计。适合在 [[so101|SO-101]] 等小型机械臂上部署。

## 架构特点

- 基于预训练视觉-语言模型（SmolVLM2-500M-Video-Instruct）
- Action Expert 头用于动作预测
- 支持多相机输入（camera1/camera2）
- 参数量小，可在 Jetson 等边缘设备上推理

## 训练配置要点

- 需显式 import SmolVLAConfig（lerobot-seeed）
- config.json 需删除 use_peft 字段
- policy.path 必须使用绝对路径
- 须 `--policy.empty_cameras=1 --dataset.push_to_hub=false`
- 不要指定 fourcc 参数

## 微调效果

小数据集（50-100 条演示）即可微调，适合单任务场景（如抓取红色方块）。

## 已知问题

- lerobot-seeed 版本与官方 LeRobot 版本有 API 差异
- 摄像头名必须用 camera1/camera2（非 top/wrist）
- 须配置 `--policy.empty_cameras=1` 处理缺失相机

## 相关概念

- [[vla|VLA]] — SmolVLA 所属的模型类别
- [[lerobot|LeRobot]] — SmolVLA 的训练框架
- [[so101|SO-101]] — SmolVLA 常用的部署平台
- [[openvla|OpenVLA]] — SmolVLA 的大型对标模型
