---
title: Stable Diffusion
created: 2026-04-18
updated: 2026-04-18
type: entity
tags: [model, diffusion, open-source]
sources: [raw/articles/flow-matching-diffusion-guide-2026.md]
---

# Stable Diffusion

## 概述

Stable Diffusion (SD) 是基于 [[diffusion-models|扩散模型]] 的开源图像生成模型，使用潜空间扩散（Latent Diffusion）大幅降低计算成本。是生成式 AI 领域最具影响力的开源项目之一。

## 版本演进

| 版本 | 年份 | 架构改进 |
|------|------|---------|
| SD 1.x | 2022 | 原始潜空间扩散 |
| SD 2.x | 2022 | 更强文本编码器 |
| SDXL | 2023 | 更大模型，双文本编码器 |
| SD3 | 2024 | MM-DiT 架构，使用 [[flow-matching|流匹配]] (Rectified Flow) |

## SD3 的突破

SD3 从 [[diffusion-models|扩散模型]] 切换到 [[flow-matching|流匹配]]（Rectified Flow），是流匹配在工业级产品中的首次大规模应用。

## 关键论文

- **High-Resolution Image Synthesis with Latent Diffusion Models** (2022) — https://arxiv.org/abs/2112.10752
- **SD3** (2024) — https://arxiv.org/abs/2403.03206

## 代码仓库

- CompVis/stable-diffusion — 原始实现
- StabilityAI/stable-diffusion — Stability 维护版
- huggingface/diffusers — 主流推理库

## 相关概念

- [[diffusion-models|扩散模型]] — SD 的理论基础
- [[flow-matching|流匹配]] — SD3 使用的新训练框架
- [[transformer-architecture|Transformer]] — DiT/MM-DiT 使用 Transformer 做去噪网络
