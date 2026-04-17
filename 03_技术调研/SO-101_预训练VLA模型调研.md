# SO-101 预训练 VLA 模型调研文档

> 更新日期：2026-04-16

---

## 一、基础预训练模型（可微调）

以下为通用 VLA 基座模型，需自行在 SO-101 上微调后使用。

| 模型 | HuggingFace 链接 | 下载量 | 备注 |
|------|-----------------|--------|------|
| SmolVLA Base | https://huggingface.co/lerobot/smolvla_base | ~28K | 轻量级 VLA，适合微调 |
| OpenVLA 7B | https://huggingface.co/openvla/openvla-7b | ~1.7M | 通用 VLA，体积更大 |

---

## 二、基于 SmolVLA 微调的 SO-101 专用模型

以下模型已使用 SO-101 机械臂数据微调，可直接尝试评估或部署：

| 模型 | HuggingFace 链接 | 基础模型 | 任务 | 摄像头 |
|------|-----------------|---------|------|--------|
| wuc1/bi_so101_flatten-and-fold-the-rag-0413 | https://huggingface.co/wuc1/bi_so101_flatten-and-fold-the-rag-0413-model | lerobot/smolvla_base | 叠衣服 | — |
| whosricky/svla-so101-pick-red-cube-2cam | https://huggingface.co/whosricky/svla-so101-pick-red-cube-2cam | lerobot/smolvla_base | 抓取红方块 | 2cam |
| whosricky/svla-so101-pick-red-cube-3cam | https://huggingface.co/whosricky/svla-so101-pick-red-cube-3cam | lerobot/smolvla_base | 抓取红方块 | 3cam |
| lerobot-edinburgh-white-team/smolvla_svla_so101_pickplace | https://huggingface.co/lerobot-edinburgh-white-team/smolvla_svla_so101_pickplace | lerobot/smolvla_base | Pick & Place | — |
| yathAg/pi05_so101_pick_place_fp16 | https://huggingface.co/yathAg/pi05_so101_pick_place_fp16 | — | Pick & Place | — |

---

## 三、SO-100 相关模型（参考）

SO-100 与 SO-101 结构相似，以下模型可作为参考：

| 模型 | HuggingFace 链接 | 基础模型 | 说明 |
|------|-----------------|---------|------|
| PLB/GR00T-N1-so100-wc | https://huggingface.co/PLB/GR00T-N1-so100-wc | NVIDIA GR00T-N1 | SO-100 叠衣服任务 |
| Rupesh386/so100-jepa-robotics-model | https://huggingface.co/Rupesh386/so100-jepa-robotics-model | JEPA | SO-100 通用 |

---

## 四、相关数据集

| 数据集 | HuggingFace 链接 | 说明 |
|--------|-----------------|------|
| lerobot/svla_so101_pickplace | https://huggingface.co/datasets/lerobot/svla_so101_pickplace | SO-101 Pick & Place 标准数据集 |
| whosricky/pick-red-cube-v3 | https://huggingface.co/datasets/whosricky/pick-red-cube-v3 | 抓取红方块数据集 |
| wuc1/bi_so101_flatten-and-fold-the-rag-0331 | https://huggingface.co/datasets/wuc1/bi_so101_flatten-and-fold-the-rag-0331 | 叠衣服数据集 |
| youliangtan/so101-table-cleanup | https://huggingface.co/datasets/youliangtan/so101-table-cleanup | 整理桌面 |
| orsoromeo/so101_pick_and_place | https://huggingface.co/datasets/orsoromeo/so101_pick_and_place | 抓取放置 |

其他 SO-101 数据集（个人实验/测试用）：
- https://huggingface.co/datasets/aaronsu11/so101_fruit
- https://huggingface.co/datasets/Grigorij/so-101-duck
- https://huggingface.co/datasets/aaawangge/so101_total
- https://huggingface.co/datasets/ehalicki/so101_multitask
- https://huggingface.co/datasets/Sengankou/so101_fold_towel_100ep
- https://huggingface.co/datasets/khb2439/piper-so101-demo

---

## 五、推荐工作流

1. **快速验证**：直接尝试上面的微调模型（如 whosricky/svla-so101-pick-red-cube-2cam），看任务是否匹配
2. **自定义微调**：使用 `lerobot/smolvla_base` + 自己的 SO-101 数据集微调
3. **参考 LeRobot 示例**：
   - `examples/tutorial/act/act_using_example.py`（ACT 算法示例）
   - `examples/tutorial/diffusion/diffusion_using_example.py`（扩散策略示例）
   - `examples/so100_to_so100_EE/`（SO-101 遥操作/评估示例）

---

## 六、补充说明

- **目前没有通用、开箱即用的 SO-101 VLA 模型**，都需要微调或选择已有的任务匹配模型
- SmolVLA（https://arxiv.org/abs/2506.01844）是目前 SO-101 上最常用的 VLA 架构
- 如果任务简单（Pick & Place），可以直接使用 `lerobot/svla_so101_pickplace` 数据集对应的微调模型
- LeRobot 官方提供了完整的 SO-101 遥操作、数据采集、微调、评估流程：https://github.com/huggingface/lerobot
