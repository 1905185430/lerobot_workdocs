# Wiki Log

> 所有 wiki 操作的按时间记录。追加式。
> 格式：`## [YYYY-MM-DD] action | subject`
> 操作类型：ingest, update, query, lint, create, archive, delete
> 当条目超过 500 条时，重命名为 log-YYYY.md 并重新开始。

## [2026-04-18] create | Wiki initialized
- Domain: Robot Wiki — 机器人学习与视觉-语言-动作模型
- Structure created with SCHEMA.md, index.md, log.md
- Path: ~/le_xuan/robot-wiki/

## [2026-04-18] ingest | 批量导入4份现有资料
- Sources:
  - raw/articles/transformer-classic-ai-guide-2026.md (Transformer与经典AI架构学习指南)
  - raw/articles/flow-matching-diffusion-guide-2026.md (流匹配与扩散模型学习指南)
  - raw/articles/vla-guide-2026.md (VLA视觉语言动作模型学习指南)
  - raw/articles/so101-baudrate-fix-2026.md (SO101通信失败修复记录)
- Created pages:
  - concepts/transformer-architecture.md
  - concepts/self-attention.md
  - concepts/cnn.md
  - concepts/rnn-lstm.md
  - concepts/diffusion-models.md
  - concepts/flow-matching.md
  - concepts/vla.md
  - concepts/imitation-learning.md
  - entities/so101.md
  - entities/lerobot.md
  - entities/smolvla.md
  - entities/openvla.md
  - entities/rt-2.md
  - entities/stable-diffusion.md
  - entities/so101-baudrate-issue.md
- Updated: index.md (15 pages), log.md
- Cross-references: 32 wikilinks across all pages
