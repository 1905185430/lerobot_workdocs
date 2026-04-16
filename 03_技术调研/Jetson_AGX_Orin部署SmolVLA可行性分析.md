# Jetson AGX Orin 部署 SmolVLA 可行性分析

## 1. 硬件与软件环境

### Jetson AGX Orin 规格
| 项目 | 规格 |
|------|------|
| SoC | NVIDIA Orin (aarch64) |
| GPU | Orin (Ampere, CUDA arch 8.7) |
| 统一内存 | 61.4 GB（CPU/GPU共享） |
| 存储 | 54GB eMMC（已用24GB，剩余28GB）+ 外接NVMe |
| JetPack | R36.4.7 (L4T 36.4.7) |
| CUDA | 12.6 |
| cuDNN | 9.3.0 |

### 软件环境
| 包 | 版本 |
|----|------|
| Python | 3.10 |
| PyTorch | 2.5.0a0+872d972e41.nv24.08 (NVIDIA Jetson定制版) |
| torchvision | 0.21.0 |
| transformers | 4.53.3 |
| accelerate | 1.13.0 |
| lerobot | 0.4.4 (editable, Seeed fork) |
| huggingface-hub | 0.35.3 |
| safetensors | 0.7.0 |
| Pillow | 12.1.1 |

### SmolVLA 默认配置（关键参数）
- VLM骨干：`HuggingFaceTB/SmolVLM2-500M-Video-Instruct`
- 图像分辨率：512×512
- chunk_size：50（一次预测50步动作）
- n_obs_steps：1
- VLM层数：16
- expert_width_multiplier：0.75
- attention_mode：cross_attn
- 解码步数（flow matching）：10步

---

## 2. 部署方案对比

### 方案A：直接使用 lerobot 0.4.4 推理（推荐）

**思路**：不升级 lerobot，在 0.4.4 环境下加载 SmolVLA 模型直接推理。

**可行性验证结果**：

1. **API 可用性** — ✅ 已确认
   - `SmolVLAPolicy.from_pretrained("lerobot/smolvla_base")` 可正常加载
   - `SmolVLAPolicy.select_action(batch, noise=None)` 可正常调用
   - `SmolVLAPolicy.predict_action_chunk` 可用
   - 工厂函数 `make_smolvla_pre_post_processors` 可正常构建前/后处理器
   - `lerobot-eval` CLI 已支持 `--policy.type=smolvla`

2. **模型加载** — ✅
   - `from_pretrained` 支持 Hub 模型名和本地路径
   - 支持 `local_files_only=True` 离线加载
   - SmolVLM2-500M 为小型VLM，模型权重约 1-2GB

3. **推理依赖** — ✅
   - PyTorch 2.5.0 支持 `torch.amp.autocast`（FP16推理）
   - 支持 `torch.compile`（可选加速）
   - 支持 `scaled_dot_product_attention`（SDPA，Flash Attention 替代）
   - transformers 4.53.3 足够新

4. **内存估算** — ✅
   - SmolVLM2-500M 参数量约 500M，FP16 约 1GB 显存
   - Action Expert 参数量约 375M（0.75×500M），FP16 约 0.75GB
   - 总模型权重约 1.5-2GB（FP16），Orin 61GB 统一内存绰绰有余
   - 推理时 KV cache + 中间激活额外约 1-2GB
   - 整体推理内存占用预计 < 5GB

5. **推理延迟估算** — ⚠️ 需实测
   - Orin GPU 算力约 275 TOPS (INT8) / 34 TOPS (FP16)
   - SmolVLM2-500M 是轻量VLM，单次推理预计 50-200ms
   - flow matching 10步解码是主要延迟来源，可考虑减少步数（如5步）
   - chunk_size=50 意味着一次推理输出50步动作，可分步执行

**方案A实施步骤**：

```bash
# 1. 在Jetson上下载模型（或从本地拷贝）
python -c "
from lerobot.policies.smolvla.modeling_smolvla import SmolVLAPolicy
policy = SmolVLAPolicy.from_pretrained('lerobot/smolvla_base')
print('模型加载成功')
"

# 2. 使用lerobot-eval测试
lerobot-eval \
    --policy.path=lerobot/smolvla_base \
    --policy.type=smolvla \
    --policy.device=cuda \
    --policy.use_amp=true

# 3. 自定义推理脚本（对接SO-101）
# 需要编写：摄像头采集 -> 图像预处理 -> select_action -> 动作下发
```

**方案A风险**：
- 0.4.4 的 SmolVLA 可能与 0.5.x 训练出的模型权重不兼容（config.json 格式可能不同）
- 需确认训练时使用的 lerobot 版本，如果用 0.5.x 训练，权重格式可能需要转换
- 缓解方法：**训练也用 0.4.4**，或**用 0.4.4 的 SmolVLA config 重新导出模型**

---

### 方案B：升级 lerobot 到 0.5.x（当前不可行）

**思路**：在 Jetson 上安装 lerobot 0.5.x，直接使用最新推理流水线。

**阻塞原因**：

| 依赖 | 要求 | Jetson现状 | 状态 |
|------|------|-----------|------|
| Python | >= 3.12 | 3.10 | ❌ 不满足 |
| PyTorch | >= 2.7 | 2.5.0 | ❌ 不满足 |
| pip | --no-deps可绕过依赖 | Requires-Python约束无法绕过 | ❌ 硬约束 |

**为什么无法升级 PyTorch**：
- Jetson 的 PyTorch 是 NVIDIA 定制版（`nv24.08`后缀），绑定 JetPack 版本
- JetPack R36.4.7 对应的最高 PyTorch 版本为 2.5.0
- `pip install torch==2.7.0` 的 dry-run 虽然显示"Would install"，但安装的是 x86 通用版，aarch64 上会运行失败
- NVIDIA 未为 Jetson 发布 PyTorch 2.7.0（截至2026年4月）

**为什么无法升级 Python**：
- Jetson 系统库依赖 Python 3.10
- conda 创建 Python 3.12 环境后，NVIDIA 定制版 PyTorch 无法安装（只有 3.10 wheel）
- 从源码编译 PyTorch 2.7+ 在 aarch64 上耗时长且兼容性无保障

**方案B结论**：**当前不可行**，需等待 NVIDIA 发布适配新 JetPack 的 PyTorch 2.7+。

---

### 方案C：混合方案（备选）

**思路**：在 Jetson 上用 Python 3.10 + PyTorch 2.5.0 运行推理，但手动移植 0.5.x 的推理代码。

**操作**：
1. 保留 0.4.4 lerobot 安装
2. 从 0.5.x 源码中仅复制 SmolVLA 推理相关模块
3. 修改 import 路径和兼容性问题

**适用场景**：当训练用 0.5.x 完成，0.4.4 无法加载 0.5.x 格式的模型权重时。

**风险**：手动移植工作量大，容易引入 bug。

---

## 3. 推荐部署路线

```
训练环境（PPIO 4090 / 本地 RTX 4060）
    │
    │  lerobot 0.5.x 训练 SmolVLA
    │  或 lerobot 0.4.4 训练 SmolVLA
    ▼
导出模型权重（确保 config.json 兼容）
    │
    ▼
Jetson AGX Orin（方案A：0.4.4 推理）
    │
    │  FP16 + AMP 推理
    │  select_action() -> 动作序列
    ▼
SO-101 执行动作
```

**核心建议**：
1. **优先用方案A**，0.4.4 已内置 SmolVLA 完整推理支持
2. **训练端统一版本**：如果 Jetson 推理用 0.4.4，训练也尽量用 0.4.4，避免权重格式不兼容
3. **如果必须用 0.5.x 训练**：训练完成后，在本地用 0.5.x 导出，再用 0.4.4 格式重新保存权重
4. **推理优化**：开启 AMP（FP16）、考虑减少 flow matching 步数（10→5）、使用 `torch.compile` 加速

---

## 4. 性能优化建议

| 优化项 | 方法 | 预期收益 |
|--------|------|---------|
| FP16推理 | `policy.use_amp=true` 或 `torch.amp.autocast('cuda')` | 显存减半，速度提升2x |
| 减少解码步数 | config中 `num_steps: 10` → `5` | 推理速度提升约2x，精度略降 |
| 减小chunk_size | `chunk_size: 50` → `25` | 单次推理更快，但需更频繁推理 |
| torch.compile | `policy = torch.compile(policy)` | 首次编译慢，后续推理加速10-30% |
| TensorRT导出 | 将模型转为TensorRT引擎 | Jetson上最优推理性能，但需额外导出工作 |
| 降低图像分辨率 | `resize_imgs_with_padding: (512,512)` → `(256,256)` | VLM推理大幅加速，精度下降 |

---

## 5. 待办事项

- [ ] 在 Jetson 上实际加载 SmolVLA 模型并测量推理延迟
- [ ] 确认训练端 lerobot 版本（0.4.4 vs 0.5.x）以决定权重兼容策略
- [ ] 编写 Jetson 上的完整推理脚本（摄像头→预处理→推理→动作执行）
- [ ] 测试 FP16 AMP 推理的数值稳定性
- [ ] 评估 TensorRT 导出的可行性和工作量
