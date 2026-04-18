---
title: 自注意力机制
created: 2026-04-18
updated: 2026-04-18
type: concept
tags: [architecture, deep-learning]
sources: [raw/articles/transformer-classic-ai-guide-2026.md]
---

# 自注意力机制 (Self-Attention)

## 定义

自注意力机制允许序列中的每个元素关注所有其他元素，动态计算关联权重。是 [[transformer-architecture|Transformer]] 的核心运算。

## 数学表达

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

## 核心概念

- **Query (Q)**：我在找什么
- **Key (K)**：我有什么特征
- **Value (V)**：实际内容

## Multi-Head Attention

将 Q/K/V 投影到 h 个子空间，分别计算注意力后拼接：

$$
\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h)W^O
$$

其中 head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)

## 为什么比 [[rnn-lstm|RNN]] 更好

1. **并行计算**：所有位置同时计算，不受序列长度限制
2. **长距离依赖**：任意两个位置间的计算路径长度为 O(1)
3. **可扩展性**：易于扩展到大规模数据和模型

## 变体

- **Masked Self-Attention**：Decoder 中使用，防止看到未来信息
- **Cross-Attention**：Encoder-Decoder 间的注意力
- **Linear Attention**：降低 O(n^2) 复杂度的近似方法
- **Flash Attention**：GPU 友好的高效实现

## 相关概念

- [[transformer-architecture|Transformer]] — 基于自注意力的完整架构
- [[vla|VLA]] — 使用注意力机制处理视觉-语言-动作输入
