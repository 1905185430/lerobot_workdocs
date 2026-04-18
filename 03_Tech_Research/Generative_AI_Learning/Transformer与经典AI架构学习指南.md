# Transformer 与经典 AI 架构学习指南

> 更新时间：2026-04-16

---

## 一、学习路线图

```
AI 基础知识
│
├─ 第一阶段：神经网络基础
│   ├─ 感知机 → MLP (多层感知机)
│   ├─ 反向传播算法
│   └─ 激活函数、损失函数
│
├─ 第二阶段：经典架构
│   ├─ CNN (卷积神经网络)
│   ├─ RNN / LSTM / GRU
│   └─ Word2Vec / Embedding
│
└─ 第三阶段：Transformer 时代
    ├─ Attention 机制
    ├─ Transformer 架构
    ├─ BERT (双向编码)
    ├─ GPT 系列 (自回归解码)
    └─ 大语言模型 (LLM) 基础
```

---

## 二、神经网络基础

### 2.1 入门必读

| 资源 | 链接 | 说明 |
|------|------|------|
| **3Blue1Brown 神经网络** | https://www.youtube.com/@3blue1brown | 视频入门，直观理解 |
| **Neural Networks from Scratch** | https://youtube.com/@Sentdex | Python 从零实现 |
| **CS231n 斯坦福课程** | http://cs231n.stanford.edu/ | 计算机视觉入门 |

### 2.2 数学基础

| 主题 | 推荐内容 |
|------|----------|
| 线性代数 | Gilbert Strang MIT 公开课 / 3Blue1Brown |
| 概率论 | 《概率论与数理统计》/ Khan Academy |
| 优化基础 | Adam 优化器原论文 / SGD 入门 |

---

## 三、经典网络架构

### 3.1 CNN (卷积神经网络)

#### 发展脉络
```
LeNet (1998) → AlexNet (2012) → VGG (2014) → GoogLeNet (2015) → ResNet (2016) →
EfficientNet (2019) → ConvNeXt (2022)
```

#### 经典论文

| 论文 | 年份 | 链接 | 说明 |
|------|------|------|------|
| **LeNet** | 1998 | http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf | CNN 开山之作 |
| **AlexNet** | 2012 | https://papers.nips.cc/paper/4824-imagenet-classification.pdf | 深度学习复兴 |
| **VGGNet** | 2014 | https://arxiv.org/abs/1409.1556 | 简洁深邃 |
| **GoogLeNet/Inception** | 2014 | https://arxiv.org/abs/1409.4842 | Inception 模块 |
| **ResNet** | 2016 | https://arxiv.org/abs/1512.03385 | 残差连接，里程碑 |
| **Batch Normalization** | 2015 | https://arxiv.org/abs/1502.03167 | 训练稳定性 |
| **Dropout** | 2014 | https://arxiv.org/abs/1312.6197 | 正则化 |
| **EfficientNet** | 2019 | https://arxiv.org/abs/1905.11946 | 效率与精度平衡 |

#### 学习资源
| 资源 | 链接 |
|------|------|
| **CS231n 课程笔记** | https://cs231n.github.io/convolutional-networks/ |
| **CNN 入门博客** | https://towardsdatascience.com/cnn-from-scratch-71e3de864941 |

---

### 3.2 RNN / LSTM / GRU

#### 网络对比
```
RNN → LSTM → GRU → Transformer (取代 RNN)
```

#### 核心问题
- **长期依赖问题** (Long-term Dependencies)
- **梯度消失/爆炸** (Vanishing/Exploding Gradients)

#### 经典论文

| 论文 | 年份 | 链接 | 说明 |
|------|------|------|------|
| **RNN 原始论文** | 1990 | - | 循环网络基础 |
| **LSTM** | 1997 | https://www.bioinf.jku.at/publications/older/2604.pdf | 长短期记忆 |
| **GRU** | 2014 | https://arxiv.org/abs/1409.1259 | LSTM 简化版 |
| **Sequence to Sequence** | 2014 | https://arxiv.org/abs/1409.3215 | 编码器-解码器 |

#### 学习资源
| 资源 | 链接 |
|------|------|
| **Colah's Blog: LSTM** | https://colah.github.io/posts/2015-08-Understanding-LSTMs/ |
| **Colah's Blog: RNN** | https://colah.github.io/posts/2015-08-RNN--summary/ |

---

### 3.3 Embedding 与 Word2Vec

| 论文 | 年份 | 链接 | 说明 |
|------|------|------|------|
| **Word2Vec** | 2013 | https://arxiv.org/abs/1310.4546 | 词向量里程碑 |
| **GloVe** | 2014 | https://aclanthology.org/D14-1162.pdf | 全局词向量 |

#### 学习资源
| 资源 | 链接 |
|------|------|
| **The Illustrated Word2Vec** | Jay Alammar 博客 |
| **Sebastian Ruder 博客** | https://ruder.io/ |

---

## 四、Transformer 架构（重点）

### 4.1 核心论文

| 论文 | 年份 | 链接 | 必读程度 |
|------|------|------|----------|
| **Attention is All You Need** | 2017 | https://arxiv.org/abs/1706.03762 | ⭐⭐⭐ 必读！ |
| **Layer Normalization** | 2017 | https://arxiv.org/abs/1607.06450 | 辅助理解 |
| **Post-LN vs Pre-LN Transformer** | 2019-2021 | 多种论文 | 进阶理解 |

### 4.2 必读博客（强烈推荐）

| 博客 | 链接 | 说明 |
|------|------|------|
| **The Illustrated Transformer** | Jay Alammar 博客 | 入门必读！图解最清晰 |
| **The Annotated Transformer** | Harvard NLP 组 | 代码即注释，PyTorch实现 |
| **Lil'Log: The Transformer** | lilianweng.github.io | 公式推导清晰 |
| **Attention is All You Need 图解** | 多位博主的图解版本 | 直观理解 |

### 4.3 Transformer 核心组件

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

### 4.4 Self-Attention 详解

#### 数学表达式

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

#### 核心概念
- **Query (Q)**: 我在找什么
- **Key (K)**: 我有什么特征
- **Value (V)**: 实际内容

#### Multi-Head Attention

$$
\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h)W^O
$$

其中 $\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$

---

## 五、BERT 与 GPT 系列

### 5.1 BERT (双向编码器)

| 论文 | 年份 | 链接 | 说明 |
|------|------|------|------|
| **BERT** | 2018 | https://arxiv.org/abs/1810.04805 | 里程碑 |
| **RoBERTa** | 2019 | https://arxiv.org/abs/1907.11692 | 改进版 |
| **ALBERT** | 2019 | https://arxiv.org/abs/1909.11942 | 轻量版 |
| **ELECTRA** | 2020 | https://arxiv.org/abs/2003.10555 | 替换 Token 检测 |

### 5.2 GPT 系列 (自回归解码器)

| 模型 | 年份 | 链接 | 说明 |
|------|------|------|------|
| **GPT** | 2018 | https://www.science.org/doi/10.1126/science.aax2342 | 初代 |
| **GPT-2** | 2019 | https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf | 15亿参数 |
| **GPT-3** | 2020 | https://arxiv.org/abs/2005.14165 | 1750亿参数 |
| **GPT-4** | 2023 | OpenAI 官方博客 | 多模态 |
| **ChatGPT** | 2022 | OpenAI 官方博客 | 对话优化 |

### 5.3 LLM 关键技术

| 技术 | 论文 | 说明 |
|------|------|------|
| **RLHF** | https://arxiv.org/abs/2009.01325 | 人类反馈强化学习 |
| **LoRA** | https://arxiv.org/abs/2106.09685 | 低秩适配 |
| **Scaling Laws** | https://arxiv.org/abs/2001.08361 | 规模化规律 |

---

## 六、Hugging Face 学习资源

### 6.1 官方教程

| 资源 | 链接 |
|------|------|
| **Hugging Face Course** | https://huggingface.co/learn/nlp-course |
| **Transformers 文档** | https://huggingface.co/docs/transformers/ |
| **PEFT 文档** | https://huggingface.co/docs/peft/ |

### 6.2 必学代码

```python
# 最简 Transformer 实现
from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

inputs = tokenizer("Hello, world!", return_tensors="pt")
outputs = model(**inputs)
```

---

## 七、GitHub 代码仓库

### 7.1 Transformer 实现

| 仓库 | Stars | 链接 | 说明 |
|------|-------|------|------|
| **Harvard-nlp/Annotated-Transformer** | ⭐12k | https://github.com/harvardnlp/annotated-transformer | 必学！代码即注释 |
| **lucidrains/x-transformers** | ⭐3k | https://github.com/lucidrains/x-transformers | 简洁实现 |
| **huggingface/transformers** | ⭐120k+ | https://github.com/huggingface/transformers | 主流库 |

### 7.2 经典网络实现

| 仓库 | 链接 | 说明 |
|------|------|------|
| **yoyojlf/ClassicNet** | CNN 经典网络实现 |
| **Jay在心木/经典神经网络pytorch** | 中文版 |

---

## 八、学习路径建议

### 入门路线（2-4 周）

```
Week 1: 神经网络基础
├─ 3Blue1Brown 神经网络视频 (3小时)
├─ CS231n 第1-3讲
└─ 实现一个 MLP

Week 2: CNN + RNN 基础
├─ CS231n CNN 部分
├─ Colah's LSTM Blog
└─ 实现 LeNet / LSTM

Week 3: Transformer 入门
├─ The Illustrated Transformer
├─ Attention is All You Need 论文
└─ Annotated Transformer 代码

Week 4: 实践
├─ Hugging Face Quick Tour
├─ 运行 BERT / GPT-2
└─ 微调一个小模型
```

### 进阶路线

1. **细读论文**：每篇经典论文至少读两遍
2. **从零实现**：用 PyTorch 实现 Transformer
3. **深入源码**：阅读 Hugging Face transformers 源码
4. **跟进前沿**：关注 NeurIPS / ICML / ICLR 新论文

---

## 九、数学基础补充

### 线性代数（必须掌握）
- 矩阵运算、特征值分解
- 注意力机制的核心：$QK^T$ 矩阵乘法
- 奇异值分解 (SVD)

### 概率论（必须掌握）
- 条件概率、贝叶斯公式
- Softmax 函数
- 交叉熵损失

### 优化基础（了解）
- 梯度下降、Adam 优化器
- 学习率调度
- 正则化（L1/L2/Dropout）

---

## 十、参考链接汇总

### 必读博客
- Jay Alammar 的博客：http://jalammar.github.io/
- Lilian Weng：https://lilianweng.github.io/
- Colah's Blog：https://colah.github.io/
- Sebastian Ruder：https://ruder.io/

### 视频课程
- **Stanford CS224N** (NLP with Deep Learning): http://web.stanford.edu/class/cs224n/
- **Stanford CS231N** (CNN for Visual Recognition): http://cs231n.stanford.edu/
- **Deep Learning Specialization** (Coursera): Andrew Ng

### 书籍
| 书名 | 说明 |
|------|------|
| **《Deep Learning》** (Ian Goodfellow) | 深度学习圣经 |
| **《Hands-On Machine Learning》** (Aurélien Géron) | 实践导向 |
| **《Neural Networks and Deep Learning》** (Michael Nielsen) | 在线免费 |

---

## 十一、FAQ

**Q: Transformer 会取代 CNN 吗？**
> 目前看来，CNN 在图像处理中仍然高效，Transformer 在视觉领域也有进展（如 ViT），两者各有优势，通常会根据任务选择或结合使用。

**Q: 需要从零实现所有经典网络吗？**
> 建议至少实现 MLP、CNN 和一个简化版 Transformer，能加深理解。生产代码用 PyTorch 内置实现即可。

**Q: Transformer 的计算复杂度是多少？**
> Self-Attention 的复杂度是 $O(n^2 \cdot d)$，其中 $n$ 是序列长度，$d$ 是隐层维度。这也是 Long Context 研究的方向（如 Flash Attention）。

---

## 十二、知识树/学习路径指导网站

### 🌐 AI/ML 学习路径网站（类似技能树）

| 网站 | 链接 | 特点 |
|------|------|------|
| **roadmap.sh** | https://roadmap.sh/ | 🎮 游戏技能树风格，完全免费开源，从 Python 到 LLM 全覆盖 |
| **AI Developer Roadmap** | https://github.com/Asabeneh/AI-Developer-Roadmap | GitHub 热门的 AI 学习路径，含配套练习 |
| **Deep Learning Wizard** | https://www.deeplearningwizard.com/ | 数学基础 → 深度学习 → 进阶，偏理论 |
| **Made with ML** | https://madewithml.com/ | 从零到生产级 ML 系统，偏实战 |
| **ML Birth** | https://ml.berkeley.edu/blog/ | 伯克利 ML 课程博客 |

### 📚 知识图谱/可视化理解

| 网站 | 链接 | 特点 |
|------|------|------|
| **Papers with Code** | https://paperswithcode.com/ | 论文 + 代码对照，知识点串联 |
| **Distill.pub** | https://distill.pub/ | 可视化理解 ML 概念，交互式文章 |
| **3Blue1Brown** | https://www.3blue1brown.com/ | 数学可视化，神经网络入门必看 |
| **Jay Alammar Blog** | http://jalammar.github.io/ | Transformer/GPT 图解，入门神器 |
| **Lil'Log** | https://lilianweng.github.io/ | 深度技术博客，公式推导清晰 |

### 🎮 交互式学习平台

| 平台 | 链接 | 特点 |
|------|------|------|
| **Hugging Face Course** | https://huggingface.co/learn/nlp-course | 官方 NLP 课程，边学边练 |
| **Kaggle Learn** | https://www.kaggle.com/learn | 入门级 ML 实战，交互式 Notebook |
| **Fast.ai** | https://course.fast.ai/ | 实践优先的深度学习课程 |

---

## 十三、下一步学习方向

```
Transformer 基础
    │
    ├── 多模态模型
    │   ├── CLIP (图文对齐)
    │   ├── GPT-4V (视觉理解)
    │   └── Flamingo (多模态对话)
    │
    ├── 大语言模型 (LLM)
    │   ├── LLaMA / Mistral
    │   ├── MoE (Mixture of Experts)
    │   └── Long Context
    │
    ├── 视觉 Transformer
    │   ├── ViT (Vision Transformer)
    │   ├── DETR (目标检测)
    │   └── Stable Diffusion (DiT)
    │
    └── 扩散模型 / 生成模型
        ├── DDPM / Stable Diffusion
        ├── Flow Matching
        └── 视频生成 (Sora 类)
```
