# 流匹配（Flow Matching）与扩散模型（Diffusion Models）学习指南

> 更新时间：2026-04-16

---

## 一、核心概念速览

### 扩散模型（Diffusion Models）

扩散模型是一类生成模型，通过**逐步加噪（Forward Process）**和**逐步去噪（Reverse Process）**来生成数据。

- **Forward Process（加噪）**：将真实数据 $x_0$ 逐步加入高斯噪声，最终变成纯噪声 $x_T \sim \mathcal{N}(0, I)$
- **Reverse Process（去噪）**：学习一个神经网络 $p_\theta(x_{t-1}|x_t)$，从噪声逐步恢复数据

**代表工作**：DDPM (Ho et al. 2020)

### 流匹配（Flow Matching）

流匹配是一种**不需要 SDE/ODE 形式**的连续生成模型训练框架，本质上是将数据从噪声映射到真实样本的过程建模为一个常微分方程（ODE）的轨迹。

核心思想：**直接回归从噪声到数据的向量场**

- 不需要预定义的噪声调度
- 训练目标更简洁，理论分析更优雅
- 可以看作是扩散模型的"精益版"

**代表工作**：Flow Matching (Chen & Lipman, 2023)

---

## 二、学习路径（推荐顺序）

```
入门阶段
│
├─ 1. 建立直观理解
│   ├─ Lil'Log 博客（必读）
│   └─ Hugging Face Annotated Diffusion
│
├─ 2. 跑通第一个代码
│   ├─ 官方 DDPM 实现（PyTorch）
│   └─ Hugging Face Diffusers 库
│
└─ 3. 理解核心数学
    ├─ 条件概率、贝叶斯公式
    ├─ KL 散度
    └─ 变分推断基础

进阶阶段
│
├─ 4. 经典论文精读
│
├─ 5. Score-Based Models 理论
│   └─ Song Yang 的 SDE 框架
│
└─ 6. Flow Matching 理论
    └─ 连续归一化流视角

实战阶段
│
├─ 7. Stable Diffusion / SDXL / SD3
├─ 8. 条件控制（Classifier-Free Guidance）
└─ 9. 加速采样（DDIM、Consistency Models）
```

---

## 三、入门资源

### 3.1 博客教程（必读）

| 资源 | 链接 | 说明 |
|------|------|------|
| **Lil'Log: Diffusion Models** | https://lilianweng.github.io/posts/2021-07-11-diffusion-models/ | 全面系统的推导，入门必读 |
| **Hugging Face: The Annotated Diffusion** | https://huggingface.co/blog/annotated-diffusion | 代码即注释，边跑边学 |
| **Hugging Face: An Introduction to Diffusion Models** | https://huggingface.co/blog/gentle-introduction-diffusion | 相对入门友好 |
| **Lil'Log: Flow Matching** | https://lilianweng.github.io/posts/2024-02-05-flow-matching/ | 同一作者，流匹配入门 |
| **What is Flow Matching?** | https://colinп不多的博客中有解释 | 简洁直观 |

### 3.2 视频课程

| 资源 | 链接 |
|------|------|
| **Hugging Face Diffusion Course** | https://www.youtube.com/@huggingface |
| **Yannic Kilcher - Diffusion Models** | YouTube 搜索 "Yannic Kilcher diffusion models" |
| **AI Coffee Break - Flow Matching** | YouTube 搜索相关 |

### 3.3 快速上手代码

```python
# 最简 DDPM 实现（PyTorch）
# 参考：https://github.com/lucidrains/denoising-diffusion-pytorch

# Diffusers 库快速使用
from diffusers import DDPMPipeline

pipeline = DDPMPipeline.from_pretrained("google/ddpm-ema-celebahq")
image = pipeline().images[0]
```

---

## 四、经典论文列表

### 4.1 扩散模型基础

| 论文 | 年份 | 链接 | 重点 |
|------|------|------|------|
| **DDPM** (Denoising Diffusion Probabilistic Models) | 2020 | https://arxiv.org/abs/2006.11239 | 奠基之作，必读 |
| **DDIM** (Denoising Diffusion Implicit Models) | 2020 | https://arxiv.org/abs/2010.02502 | 加速采样 |
| **Improved DDPM** | 2021 | https://arxiv.org/abs/2102.09672 | 改进训练稳定性 |
| **Diffusion Beats GANs** (ADM) | 2021 | https://arxiv.org/abs/2105.05233 | 超越 GAN 的质量 |

### 4.2 Score-Based Models

| 论文 | 年份 | 链接 | 重点 |
|------|------|------|------|
| **Score-Based SDE** (Song Yang) | 2020 | https://arxiv.org/abs/2011.13456 | 理论框架，SDE 统一视角 |
| **Score-Based ODE** | 2021 | https://arxiv.org/abs/2106.01354 | 连续化版本 |

### 4.3 潜空间扩散（Latent Diffusion）

| 论文 | 年份 | 链接 | 重点 |
|------|------|------|------|
| **Latent Diffusion** (LDM/SD) | 2021 | https://arxiv.org/abs/2112.10752 | 高效图像生成 |
| **Stable Diffusion 2** | 2022 | 官方 Blog | SD 续作 |
| **SDXL** | 2023 | 官方 Blog | 更大模型 |
| **Stable Diffusion 3 (SD3)** | 2024 | https://arxiv.org/abs/2403.03206 | MM-DiT 架构 |

### 4.4 条件引导技术

| 论文 | 年份 | 链接 | 重点 |
|------|------|------|------|
| **Classifier-Free Guidance** | 2021 | https://arxiv.org/abs/2207.12598 | 无分类器引导 |
| **CLIP Guidance** | 2021 | 结合 OpenAI CLIP | 文生图条件控制 |
| **Classifier Guidance** | 2021 | cascaded diffusion | 条件扩散 |

### 4.5 加速采样与蒸馏

| 论文 | 年份 | 链接 | 重点 |
|------|------|------|------|
| **Consistency Models** | 2023 | https://arxiv.org/abs/2303.01469 | 一步/少步生成 |
| **LCM** (Latent Consistency Models) | 2024 | https://arxiv.org/abs/2310.04378 | SD 的 LCM |
| **SDXL-Turbo** | 2023 | 官方 Blog | 实时生成 |

### 4.6 流匹配（Flow Matching）

| 论文 | 年份 | 链接 | 重点 |
|------|------|------|------|
| **Flow Matching** (Chen & Lipman) | 2023 | https://arxiv.org/abs/2309.01436 | 奠基论文 |
| **Conditional Flow Matching** | 2023 | https://arxiv.org/abs/2309.01436 | 条件流匹配 |
| **Flow Matching for IMG** (FMI) | 2023 | Apple 团队 | 图像生成应用 |
| **Rectified Flow** | 2024 | https://arxiv.org/abs/2403.04247 | 更好的流匹配 |
| **MMA-Diffusion** | 2024 | 工业界 | 多模态流匹配 |

---

## 五、GitHub 代码仓库

### 5.1 必学库

| 仓库 | Stars | 链接 | 说明 |
|------|-------|------|------|
| **huggingface/diffusers** | ⭐28k | https://github.com/huggingface/diffusers | 主流扩散模型库，必学 |
| **CompVis/stable-diffusion** | ⭐8k | https://github.com/CompVis/stable-diffusion | 原始 SD 实现 |
| **StabilityAI/stable-diffusion** | ⭐25k | https://github.com/stable-diffusion | Stability 维护版 |

### 5.2 代码教程

| 仓库 | Stars | 链接 | 说明 |
|------|-------|------|------|
| **lucidrains/denoising-diffusion-pytorch** | ⭐5k | https://github.com/lucidrains/denoising-diffusion-pytorch | 代码即教程 |
| **openai/guided-diffusion** | ⭐4k | https://github.com/openai/guided-diffusion | OpenAI 官方实现 |

### 5.3 流匹配实现

| 仓库 | Stars | 链接 | 说明 |
|------|-------|------|------|
| **Apple-ML-Research/MLFlowMatching** | - | https://github.com/Apple-ML-Research/MLFlowMatching | Apple 官方 |
| **StableTransfer/Flow-Matching** | ⭐500 | https://github.com/StableTransfer/Flow-Matching | 图像生成专用 |
| **idiap/flow-matching** | - | https://github.com/idiap/flow-matching | 研究向 |
| **minimax-team/minimax-diffusion** | - | https://github.com/minimax-team/minimax-diffusion | 包含流匹配 |

### 5.4 Awesome 系列

| 仓库 | 链接 |
|------|------|
| **awesome-diffusion-models** | https://github.com/cunaud/awesome-diffusion-models |
| **awesome-stable-diffusion** | 搜索可得 |
| **awesome-flow-matching** | 搜索可得 |

---

## 六、理论进阶书单

### 数学基础

1. **Probabilistic Machine Learning** (Kevin Murphy) - 概率机器学习基础
2. **Information Theory, Inference, and Learning Algorithms** (MacKay) - 信息论与推断
3. **Deep Learning** (Goodfellow) - 第18章变分推断

### 生成模型专题

1. **Generative Deep Learning** (David Foster) - 入门友好
2. **Flow-Based Deep Generative Models** (综述论文)

---

## 七、实践项目建议

### 入门项目
1. 从零实现 DDPM（PyTorch）
2. 用 Diffusers 库生成图像
3. 微调 SD 生成特定风格

### 进阶项目
1. 实现条件生成（CLIP 引导）
2. 用 Flow Matching 训练自己的生成模型
3. 部署 SD 到边缘设备（Jetson）

### 科研方向
1. 新采样器设计（少步生成）
2. 流匹配的理论分析
3. 多模态生成（图像/视频/3D）

---

## 八、常见问题 FAQ

**Q: Flow Matching 和 Diffusion 有什么区别？**
> 本质上都是生成模型，但 Flow Matching 不需要预定义的噪声调度，训练目标更简洁（直接回归向量场），理论上更容易分析。

**Q: 需要多少 GPU 来训练扩散模型？**
> 经典 DDPM 至少需要 16GB VRAM（batch=32, 64x64 图像）。SD 需要 24GB+。Flow Matching 类似。

**Q: 先学扩散还是先学流匹配？**
> 建议先学扩散模型建立直觉，再学流匹配理解简化理论。

---

## 九、相关技术关联

```
扩散模型/流匹配
    │
    ├── 生成模型家族
    │   ├── GAN (对抗生成)
    │   ├── VAE (变分自编码器)
    │   ├── Flow-Based Models (归一化流)
    │   └── Diffusion/Flow Matching (扩散/流匹配)
    │
    ├── 机器人应用
    │   ├── VLA 模型 (如 SmolVLA)
    │   ├── 机器人视觉表征
    │   └── 动作生成
    │
    └── 前沿方向
        ├── 视频生成 (Sora, Stable Video)
        ├── 3D 生成 (Point-E, DreamFusion)
        └── 具身智能
```

---

## 十、参考资料

1. Ho et al. "Denoising Diffusion Probabilistic Models" (2020)
2. Song Yang "Score-Based Generative Modeling through Stochastic Differential Equations" (2020)
3. Chen & Lipman "Flow Matching for Generative Modeling" (2023)
4. Rombach et al. "High-Resolution Image Synthesis with Latent Diffusion Models" (2022)
5. Ho et al. "Classifier-Free Diffusion Guidance" (2022)
6. Song et al. "Consistency Models" (2023)
