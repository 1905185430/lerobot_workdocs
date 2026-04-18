---
title: RNN / LSTM / GRU
created: 2026-04-18
updated: 2026-04-18
type: concept
tags: [architecture, deep-learning]
sources: [raw/articles/transformer-classic-ai-guide-2026.md]
---

# RNN / LSTM / GRU

## 定义

循环神经网络（RNN）及其变体 LSTM、GRU 是处理序列数据的经典架构，通过隐藏状态在时间步间传递信息。

## 发展脉络

```
RNN (1990) → LSTM (1997) → GRU (2014) → Seq2Seq (2014) → Transformer (2017, 取代 RNN)
```

## 核心问题

- **长期依赖问题**：标准 RNN 难以捕获远距离依赖
- **梯度消失/爆炸**：反向传播通过时间步时梯度指数级衰减或增长

## LSTM

长短期记忆网络，通过门控机制解决长期依赖：
- **遗忘门**：决定丢弃哪些旧信息
- **输入门**：决定存储哪些新信息
- **输出门**：决定输出哪些信息

## GRU

LSTM 的简化版，合并遗忘门和输入门为更新门，参数更少，训练更快。

## 与 [[transformer-architecture|Transformer]] 的对比

| 特性 | RNN/LSTM | Transformer |
|------|----------|-------------|
| 并行化 | 否（逐步处理） | 是（全序列并行） |
| 长距离依赖 | 弱（即使 LSTM 也有限） | 强（[[self-attention|自注意力]] O(1) 路径） |
| 计算效率 | 序列长度线性 | 序列长度二次 |
| 适用场景 | 短序列、实时流式 | 大规模序列、批量处理 |

## 经典论文

- **LSTM** (1997) — https://www.bioinf.jku.at/publications/older/2604.pdf
- **GRU** (2014) — https://arxiv.org/abs/1409.1259
- **Sequence to Sequence** (2014) — https://arxiv.org/abs/1409.3215

## 相关概念

- [[transformer-architecture|Transformer]] — 取代 RNN 成为序列建模主流
- [[self-attention|自注意力机制]] — Transformer 解决 RNN 长距离依赖问题的核心
