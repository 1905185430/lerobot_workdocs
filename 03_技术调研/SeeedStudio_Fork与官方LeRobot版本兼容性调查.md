# SeeedStudio Fork 与官方 LeRobot 版本兼容性调查

> 2026-04-15

## 背景

本地使用 SeeedStudio 支持的 LeRobot fork 采集数据集，服务器使用官方 LeRobot 训练，需确认两端版本是否需要对应。

## 版本对比

| | SeeedStudio Fork | 官方最新 |
|---|---|---|
| 仓库 | github.com/Seeed-Projects/lerobot | github.com/huggingface/lerobot |
| 版本号 | 0.4.4 | 0.5.1 |
| 基于官方 | 2026-02-04 快照 (commit 0f39248) | 最新 |
| 落后官方 | 143 commits, 507 文件差异 | — |
| Python 要求 | 3.10 | 3.12 |
| CODEBASE_VERSION | v3.0 | v3.0 |
| 额外分支 | DepthCameraSupport (RealSense/Orbbec 深度相机) | — |
| CI 状态 | failure | — |

## 核心结论：数据集格式兼容，不需要版本严格对应

数据集格式由 `CODEBASE_VERSION` 决定，两端都是 **v3.0**，格式完全一致：
- Parquet 数据文件结构一致
- 元数据格式一致
- 视频路径结构一致
- `info.json` 字段一致

## 数据集格式版本历史

| 官方版本 | CODEBASE_VERSION | 变化 |
|----------|-----------------|------|
| v0.3.x | v2.1 | 旧格式 |
| v0.4.0 | v3.0 | **Breaking change** |
| v0.4.4 | v3.0 | 无变化 |
| v0.5.1 | v3.0 | 无变化 |
| SeeedStudio fork | v3.0 | 无变化 |

## v2.1 → v3.0 Breaking Change 详情

发生在官方 v0.3.x → v0.4.0 之间：

| 项目 | v2.1 | v3.0 |
|------|------|------|
| 数据文件 | `data/chunk-000/episode_000000.parquet` | `data/chunk-000/file_000.parquet` |
| 视频文件 | `videos/chunk-000/CAMERA/episode_000000.mp4` | `videos/CAMERA/chunk-000/file_000.mp4` |
| Episode 元数据 | `episodes.jsonl` | `meta/episodes/chunk-000/episodes_000.parquet` |
| 任务格式 | `tasks.jsonl` | `meta/tasks/chunk-000/file_000.parquet` |
| 统计信息 | `episodes_stats.jsonl` | `meta/episodes_stats/chunk-000/file_000.parquet` |

官方提供转换脚本：`src/lerobot/datasets/v30/convert_dataset_v21_to_v30.py`

## 潜在风险（非格式层面）

1. **SeeedStudio fork 落后 143 commit** — 官方 0.5.1 包含 metadata indexing、frame_index、Parquet 写入等 bug 修复，fork 可能有已知 bug 影响采集质量
2. **Python 版本差异** — fork 要求 3.10，官方 0.5.1 要求 3.12，两端环境不互通
3. **依赖差异** — v0.5.1 使用 transformers v5、draccus==0.10.0 等，训练端安装 0.5.1 即可
4. **CI 状态** — SeeedStudio fork CI 为 failure，可能存在未修问题

## 实际建议

```
本地采集（SeeedStudio fork 0.4.4） → 上传 HF → 服务器训练（官方 0.5.1）
                              ✅ 数据集格式完全兼容
```

- 服务器端放心用 `pip install lerobot==0.5.1` 训练
- 采集时注意数据完整性（fork 可能有未修 bug）
- 如有旧版 v2.x 数据集，先用官方转换脚本升级到 v3.0
- 本地已升级到官方 0.5.1，可直接用官方版采集，SeeedStudio fork 非必须
- SeeedStudio fork 的 DepthCameraSupport 分支如需深度相机（Orbbec/RealSense），可单独考虑
