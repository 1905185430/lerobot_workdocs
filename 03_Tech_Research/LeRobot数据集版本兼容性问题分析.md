# LeRobot 数据集版本兼容性问题分析

> 2026-04-15

## 背景

本地用 LeRobot 0.4.4 采集数据集（Ready321/vla_grab_redcube），上传到 HuggingFace 后，在 PPIO 服务器上用 LeRobot 0.5.2 训练时反复报错。数据集的 Parquet 文件格式（CODEBASE_VERSION v3.0）在 0.4.0~0.5.2 之间没有变化，但训练仍然失败。

## 问题根因

LeRobot 的版本检查不是看 Parquet 数据文件结构，而是看 `meta/info.json` 里的 `codebase_version` 字段。0.4.x 到 0.5.x 之间，**info.json 元数据格式发生了变化**，导致版本检查不通过。

```
0.4.4 采集出的 info.json          0.5.2 训练期望的 info.json
─────────────────────────         ─────────────────────────
codebase_version: "v3.0"    →     codebase_version: "v0.5.2"
视频字段: "info"              →     "video_info" + video.fps
state/action 无 fps          →     必须有 fps 字段
无 next.done                 →     必须有 next.done
有 data_files_size_in_mb     →     需删除
```

## 版本链路

```
采集 (0.4.4)           上传 HF              训练 (0.5.2)
codebase_version       info.json             check_version_compatibility()
    "v3.0"        ──────────────→       期望 "v0.5.x" → ❌ 报错
```

## 报错表现

- `BackwardCompatibilityError` — 主版本号不匹配
- `NotImplementedError: Contact the maintainer on Discord` — `get_safe_version()` 无法处理旧格式
- `RevisionNotFoundError` — 数据集缺少 version tag

## info.json 差异详情

| 字段 | 0.4.4 (v3.0) | 0.5.2 (v0.5.2) |
|------|-------------|----------------|
| codebase_version | "v3.0" | "v0.5.2" |
| 视频特征字段 | `info: {video.codec, video.pix_fmt, ...}` | `video_info: {video.fps, video.codec, video.pix_fmt, ...}` |
| observation.state fps | 无 | 需要 `"fps": 30.0` |
| action fps | 无 | 需要 `"fps": 30.0` |
| timestamp/frame_index/episode_index/index/task_index fps | 无 | 需要 `"fps": 30.0` |
| next.done | 不存在 | `{"dtype": "bool", "shape": [1], "names": null, "fps": 30.0}` |
| data_files_size_in_mb | 有 | 需删除 |
| video_files_size_in_mb | 有 | 需删除 |

## 旧数据集升级方案

对已有的 vla_grab_redcube 数据集，需手动升级 info.json：

```python
from huggingface_hub import hf_hub_download, upload_file
import json

# 1. 下载当前 info.json
f = hf_hub_download("Ready321/vla_grab_redcube", "meta/info.json", repo_type="dataset")
with open(f) as fp:
    info = json.load(fp)

# 2. 更新 codebase_version
info["codebase_version"] = "v0.5.2"

# 3. 重命名视频 info → video_info，补充 video.fps
for key in ["observation.images.top", "observation.images.wrist"]:
    if key in info["features"] and info["features"][key]["dtype"] == "video":
        old_info = info["features"][key].pop("info", {})
        info["features"][key]["video_info"] = {
            "video.fps": float(info["fps"]),
            "video.codec": old_info.get("video.codec", "av1"),
            "video.pix_fmt": old_info.get("video.pix_fmt", "yuv420p"),
            "video.is_depth_map": old_info.get("video.is_depth_map", False),
            "has_audio": old_info.get("has_audio", False),
        }

# 4. 为 state/action 添加 fps
for key in ["observation.state", "action"]:
    if key in info["features"]:
        info["features"][key]["fps"] = float(info["fps"])

# 5. 为索引字段添加 fps
for key in ["timestamp", "frame_index", "episode_index", "index", "task_index"]:
    if key in info["features"]:
        info["features"][key]["fps"] = float(info["fps"])

# 6. 添加 next.done (0.5.x 必需)
info["features"]["next.done"] = {
    "dtype": "bool", "shape": [1], "names": None, "fps": float(info["fps"])
}

# 7. 删除过时字段
info.pop("data_files_size_in_mb", None)
info.pop("video_files_size_in_mb", None)

# 8. 上传回 HF
with open("/tmp/info.json", "w") as fp:
    json.dump(info, fp, indent=2)
upload_file("/tmp/info.json", "meta/info.json",
            repo_id="Ready321/vla_grab_redcube",
            repo_type="dataset",
            commit_message="Update info.json to v0.5.2 format")
```

## 还需要打 version tag

升级 info.json 后，还需给数据集打 version tag：

```python
from huggingface_hub import HfApi
api = HfApi(token="<your_hf_token>")
api.create_tag("Ready321/vla_grab_redcube", tag="v0.5.2", repo_type="dataset")
```

## 后续方案：统一版本，避免再踩坑

```
方案：本地采集 + 服务器训练 统一使用 0.5.x

本地 (0.5.1) 采集 → info.json 为 v0.5.x 格式 → 上传 HF → 服务器 (0.5.2) 训练
                                                     ✅ 直接兼容
```

- 本地已升级到 0.5.1，以后采集出的数据集就是 v0.5.x 格式
- 服务器 0.5.2 直接能训练，无需手动转换
- 不需要改服务器版本，也不需要降级任何东西
- 已有旧数据集（0.4.4 采集）只需一次性升级 info.json 即可

## 其他训练踩坑汇总

| 报错 | 原因 | 修复 |
|------|------|------|
| RevisionNotFoundError | 数据集无 version tag | `HfApi().create_tag(repo_id, tag="v0.5.2")` |
| Feature mismatch (camera1/2/3 vs top/wrist) | SmolVLA 默认 input_features 与数据集摄像头名不匹配 | 用 Python 脚本覆写 policy_cfg.input_features |
| DecodingError: rename_map | draccus 无法从 CLI 解析 dict | 用 Python 训练脚本代替 CLI |
| OSError: libtorchcodec_core / libavutil.so.56 | 缺 ffmpeg 库 | `apt-get install -y ffmpeg libavutil-dev libavcodec-dev libavformat-dev libswscale-dev` |
| FileExistsError: Output directory | 旧输出目录存在且未启用 resume | 加 `--resume=true` 或换 `--output_dir` |
| 401 Unauthorized on HF | Token 过期 | 重新生成 token |
