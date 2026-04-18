---
title: Transformer 架构
created: 2026-04-18
updated: 2026-04-18
type: concept
tags: [architecture, deep-learning, model]
sources: [raw/articles/transformer-classic-ai-guide-2026.md, raw/articles/vla-guide-2026.md]
---

# Transformer 架构

## 定义

Transformer 是一种基于自注意力机制（Self-Attention）的深度学习架构，由 Vaswani 等人在 2017 年的论文 "Attention is All You Need" 中提出。它完全摒弃了 RNN 的循环结构，仅靠注意力机制处理序列数据，实现了高效的并行计算。

## 核心组件

```
输入嵌入 (Input Embedding)
    ↓
位置编码 (Positional Encoding)
    ↓
┌───────────────────────────┐
│      N × Encoder Layer    │
│  ├─ Multi-Head Self-Attention
│  ├─ Add & Norm
│  ├─ Feed Forward
│  └─ Add & Norm
└───────────────────────────┘
    ↓
┌───────────────────────────┐
│      N × Decoder Layer     │
│  ├─ Masked Self-Attention
│  ├─ Encoder-Decoder Attention
│  ├─ Add & Norm
│  ├─ Feed Forward
│  └─ Add & Norm
└───────────────────────────┘
    ↓
线性层 + Softmax → 输出
```

## 核心思想

- **[[self-attention|自注意力机制]]**：通过 Q/K/V 矩阵计算序列内元素间的关联权重
- **并行化**：不像 [[rnn-lstm|RNN]] 逐步处理，Transformer 可并行处理整个序列
- **位置编码**：通过正弦/余弦函数注入位置信息，弥补无循环结构的位置感知缺失

## 历史意义

Transformer 彻底改变了 NLP 领域，是 BERT、GPT 等大语言模型的基础架构。其影响力延伸到视觉（ViT）和机器人控制（[[vla|VLA]] 模型）。

## 计算复杂度

Self-Attention 的复杂度为 O(n^2 * d)，其中 n 是序列长度，d 是隐层维度。这也是 Long Context 研究的方向（如 Flash Attention）。

## 关键论文

- **Attention is All You Need** (2017) — https://arxiv.org/abs/1706.03762
- **Layer Normalization** (2017) — https://arxiv.org/abs/1607.06450

## 学习资源

- Jay Alammar: The Illustrated Transformer
- Harvard NLP: The Annotated Transformer
- Lilian Weng: The Transformer

## 相关概念

- [[self-attention|自注意力机制]] — Transformer 的核心运算
- [[rnn-lstm|RNN/LSTM]] — Transformer 取代的前一代序列模型
- [[cnn|CNN]] — 另一种经典架构，在视觉领域仍高效
- [[vla|VLA]] — Transformer 在机器人控制领域的应用
