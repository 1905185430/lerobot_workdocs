---
title: 卷积神经网络 (CNN)
created: 2026-04-18
updated: 2026-04-18
type: concept
tags: [architecture, deep-learning]
sources: [raw/articles/transformer-classic-ai-guide-2026.md]
---

# 卷积神经网络 (CNN)

## 定义

CNN 是一类使用卷积运算提取局部特征的深度神经网络，特别擅长处理网格结构数据（图像、视频）。

## 发展脉络

```
LeNet (1998) → AlexNet (2012) → VGG (2014) → GoogLeNet (2015) → ResNet (2016) →
EfficientNet (2019) → ConvNeXt (2022)
```

## 核心思想

- **局部感受野**：卷积核只关注局部区域，提取局部特征
- **权值共享**：同一卷积核在整个输入上滑动，大幅减少参数
- **层次化特征**：低层提取边缘/纹理，高层提取语义信息

## 关键里程碑论文

| 论文 | 年份 | 意义 |
|------|------|------|
| LeNet | 1998 | CNN 开山之作 |
| AlexNet | 2012 | 深度学习复兴，GPU 训练 |
| VGGNet | 2014 | 简洁深邃，3x3 卷积堆叠 |
| ResNet | 2016 | 残差连接，里程碑 |
| EfficientNet | 2019 | 效率与精度平衡 |

## 与 [[transformer-architecture|Transformer]] 的关系

- CNN 在图像处理中仍然高效，参数更少
- ViT (Vision Transformer) 在大规模数据上可超越 CNN
- ConvNeXt (2022) 证明纯 CNN 架构经现代化改造后仍可匹敌 ViT
- 两者各有优势，通常根据任务选择或结合使用

## 相关概念

- [[transformer-architecture|Transformer]] — 取代 CNN 成为许多任务的新标准
- [[rnn-lstm|RNN/LSTM]] — 处理序列数据的另一经典架构
