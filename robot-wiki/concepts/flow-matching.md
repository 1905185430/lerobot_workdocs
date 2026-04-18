---
title: 流匹配
created: 2026-04-18
updated: 2026-04-18
type: concept
tags: [diffusion, deep-learning]
sources: [raw/articles/flow-matching-diffusion-guide-2026.md]
---

# 流匹配 (Flow Matching)

## 定义

流匹配是一种不需要 SDE/ODE 形式的连续生成模型训练框架，本质上是将数据从噪声映射到真实样本的过程建模为一个常微分方程（ODE）的轨迹。

核心思想：**直接回归从噪声到数据的向量场**

## 核心优势

- 不需要预定义的噪声调度
- 训练目标更简洁，理论分析更优雅
- 可以看作是 [[diffusion-models|扩散模型]] 的"精益版"

## 关键论文

| 论文 | 年份 | 重点 |
|------|------|------|
| Flow Matching (Chen & Lipman) | 2023 | 奠基论文 |
| Conditional Flow Matching | 2023 | 条件流匹配 |
| Rectified Flow | 2024 | 更好的流匹配，SD3 使用 |

## 代码资源

- Apple: MLFlowMatching — Apple 官方实现
- StableTransfer/Flow-Matching — 图像生成专用
- idiap/flow-matching — 研究向

## 与 [[diffusion-models|扩散模型]] 的区别

| 特性 | 扩散模型 | 流匹配 |
|------|---------|--------|
| 噪声调度 | 需要预定义 | 不需要 |
| 训练目标 | 预测噪声/分数 | 回归向量场 |
| 推理方式 | 迭代去噪 | ODE 积分 |
| 理论优雅度 | 较复杂 | 更简洁 |

## 机器人应用

流匹配在机器人领域有潜在应用，特别是动作生成。VLA 模型（如 [[vla|VLA]]）的未来版本可能采用流匹配替代扩散策略。

## 相关概念

- [[diffusion-models|扩散模型]] — 流匹配的理论前身
- [[vla|VLA]] — 机器人控制中的视觉-语言-动作模型
