# Wiki Schema

## Domain

Robot Wiki — 机器人学习与视觉-语言-动作模型

覆盖范围：
- 机器人策略学习（imitation learning, RL, VLA）
- 视觉语言动作模型（SmolVLA, GR00T, OpenVLA, RT-2 等）
- 机器人硬件与调试（SO-101, Dobot Nova, Orbbec 相机）
- 数据采集与处理（LeRobot, 遥操作, 数据集管理）
- 模型训练与部署（微调, 推理优化, 边缘部署）
- AI 基础理论（Transformer, 扩散模型, 流匹配）

## Conventions

- 文件名：小写，连字符分隔，无空格（例：`transformer-architecture.md`）
- 每个知识页以 YAML frontmatter 开头（见下方模板）
- 使用 `[[wikilinks]]` 链接其他页面（每页至少 2 个出链）
- 更新页面时务必更新 `updated` 日期
- 新页面必须添加到 `index.md` 对应分类下
- 每次操作必须追加到 `log.md`
- 语言：中文为主，专有名词保留英文

## Frontmatter

```yaml
---
title: 页面标题
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query
tags: [来自下方标签分类]
sources: [raw/articles/source-name.md]
---
```

## Tag Taxonomy

### 模型与架构
- `model` — 具体模型（SmolVLA, GR00T, OpenVLA 等）
- `architecture` — 架构设计（Transformer, VLA, Diffusion Policy）
- `benchmark` — 基准测试与评估

### 训练与微调
- `training` — 训练方法与流程
- `fine-tuning` — 微调技术（LoRA, PEFT, 全参）
- `dataset` — 数据集与数据管理
- `optimization` — 优化器与训练技巧

### 部署与推理
- `deployment` — 模型部署（边缘设备, Jetson）
- `inference` — 推理优化与加速
- `quantization` — 量化技术

### 机器人硬件
- `robot-arm` — 机械臂（SO-101, Dobot Nova）
- `camera` — 相机与视觉（Orbbec, RGB-D）
- `sensor` — 传感器
- `calibration` — 校准与标定

### 数据采集
- `teleoperation` — 遥操作
- `data-collection` — 数据采集流程
- `simulation` — 仿真环境（MuJoCo, Isaac Sim）

### 基础理论
- `deep-learning` — 深度学习基础
- `diffusion` — 扩散模型与流匹配
- `rl` — 强化学习
- `nlp` — 自然语言处理

### 工具与框架
- `framework` — 框架与工具（LeRobot, HuggingFace）
- `open-source` — 开源项目与社区

### 元信息
- `comparison` — 对比分析
- `pitfall` — 踩坑与故障修复
- `tutorial` — 教程与指南

规则：每个页面的 tag 必须来自此分类。需要新 tag 时先在此添加再使用。

## Page Thresholds

- **创建页面**：实体/概念在 2+ 个来源中出现，或在单个来源中为核心主题
- **追加到已有页面**：新来源提到了已覆盖的内容
- **不创建页面**：仅一笔带过的提及、超出领域范围的细节
- **拆分页面**：超过 200 行时，拆分为子主题并交叉链接
- **归档页面**：内容完全过时时，移至 `_archive/`，从 index 移除

## Entity Pages

每个值得记录的实体一个页面。包含：
- 概述 / 是什么
- 关键事实与日期
- 与其他实体的关系（`[[wikilinks]]`）
- 来源引用

## Concept Pages

每个概念/主题一个页面。包含：
- 定义 / 解释
- 当前认知状态
- 待解决问题或争议
- 相关概念（`[[wikilinks]]`）

## Comparison Pages

并排分析。包含：
- 比较对象与原因
- 对比维度（优先用表格）
- 结论或综合
- 来源

## Pitfall Pages

踩坑记录。包含：
- 问题现象
- 根因分析
- 解决方案
- 预防措施
- 相关实体/概念链接

## Update Policy

当新信息与已有内容冲突时：
1. 检查日期 — 较新的来源通常优先
2. 如果确实矛盾，同时保留两种观点并标注日期和来源
3. 在 frontmatter 中标记：`contradictions: [page-name]`
4. 在 lint 报告中标记供用户审核
