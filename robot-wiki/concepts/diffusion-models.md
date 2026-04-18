---
title: 扩散模型
created: 2026-04-18
updated: 2026-04-18
type: concept
tags: [diffusion, deep-learning, model]
sources: [raw/articles/flow-matching-diffusion-guide-2026.md]
---

# 扩散模型 (Diffusion Models)

## 定义

扩散模型是一类生成模型，通过**逐步加噪（Forward Process）**和**逐步去噪（Reverse Process）**来生成数据。

- **Forward Process**：将真实数据 x_0 逐步加入高斯噪声，最终变成纯噪声 x_T ~ N(0, I)
- **Reverse Process**：学习一个神经网络 p_θ(x_{t-1}|x_t)，从噪声逐步恢复数据

## 核心思想

本质上是定义了一个从数据分布到噪声分布的马尔可夫链，然后学习其逆过程来生成样本。

## 关键里程碑

| 模型 | 年份 | 意义 |
|------|------|------|
| DDPM | 2020 | 奠基之作，必读 |
| DDIM | 2020 | 加速采样，确定性推理 |
| Score-Based SDE | 2020 | Song Yang 的 SDE 统一理论框架 |
| LDM/[[stable-diffusion|Stable Diffusion]] | 2021 | 潜空间扩散，高效图像生成 |
| ADM | 2021 | 超越 GAN 的质量 |

## 条件引导技术

- **Classifier-Free Guidance** (2021)：无需额外分类器，通过条件/无条件预测的差异引导生成
- **CLIP Guidance**：结合 OpenAI CLIP 做文生图条件控制

## 加速采样

- **Consistency Models** (2023)：一步/少步生成
- **LCM** (2024)：SD 的 Latent Consistency Models
- **SDXL-Turbo** (2023)：实时生成

## 与 [[flow-matching|流匹配]] 的关系

扩散模型和流匹配都是生成模型，但流匹配不需要预定义的噪声调度，训练目标更简洁（直接回归向量场），理论上更容易分析。可看作扩散模型的"精益版"。

## 相关概念

- [[flow-matching|流匹配]] — 扩散模型的简化理论框架
- [[transformer-architecture|Transformer]] — DiT (Diffusion Transformer) 使用 Transformer 做去噪网络
- [[vla|VLA]] — 扩散模型可用于机器人的动作生成
