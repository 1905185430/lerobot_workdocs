#!/usr/bin/env python3
"""
SO-101 摄像头画面采集工具
=========================

功能：采集所有可用彩色摄像头的画面，保存为图片文件，按设备名命名。

使用方法：
    # 激活环境后运行
    conda activate lerobot
    python 摄像头画面采集.py

    # 只采集指定摄像头
    python 摄像头画面采集.py --devices /dev/video10 /dev/video18

    # 指定输出目录
    python 摄像头画面采集.py --output ~/我的输出目录

    # 指定分辨率
    python 摄像头画面采集.py --width 1920 --height 1080

    # 不指定 fourcc 时自动选择，如需强制指定：
    python 摄像头画面采集.py --fourcc MJPG

输出：每个摄像头一张 .jpg 文件，命名为 video0.jpg, video10.jpg 等。

---

【摄像头踩坑指南】

1. Orbbec Gemini 335 必须用 V4L2 后端（cv2.CAP_V4L2=200），FFMPEG 后端读不了帧。
   本脚本已默认使用 V4L2，无需额外配置。

2. Orbbec 每个相机会产生多个 /dev/video* 节点：
   - video4/5/6/7/8/9 → Orbbec #1（彩色/深度/IR/metadata）
   - video12-19       → Orbbec #2（彩色/深度/IR/metadata）
   只有部分是彩色流，其余是深度(Z16)、红外、metadata，LeRobot 用不了。
   彩色流对应节点：
     - Orbbec #1 彩色 → /dev/video10
     - Orbbec #2 彩色 → /dev/video18

3. lerobot-find-cameras 命令会无差别扫描所有 video 节点，遇到深度/IR 节点
   就会报错甚至段错误，这是正常现象，不代表摄像头坏了。
   用本脚本可以正确测试彩色摄像头是否工作。

4. 用户需要加入 video 组才能访问所有摄像头：
     sudo usermod -aG video $USER
   添加后需重新登录才生效。

5. 640x480@30fps + MJPG 是 Orbbec 彩色流稳定可用的配置。
   更高分辨率（如 1920x1080）帧率会大幅下降，不建议采集时使用。

6. LeRobot 采集数据的帧格式是 RGB，OpenCV imwrite 需要 BGR，脚本中已做转换。

---

【系统摄像头映射参考（嘉璇的机器）】

    设备节点     | 硬件                      | 流类型   | 分辨率
    ----------- | ------------------------- | -------- | --------
    /dev/video0 | 笔记本内置摄像头           | 彩色     | 640x480
    /dev/video2 | icSpring USB 摄像头        | 彩色     | 640x480
    /dev/video6 | Orbbec #1 (CP15641000AW)  | 深度 Z16 | 640x400
    /dev/video8 | Orbbec #1                 | 红外 IR  | 640x400
    /dev/video10| Orbbec #1                 | 彩色     | 640x480
    /dev/video12| Orbbec #2 (CP1L44P0007K)  | 深度 Z16 | 640x480
    /dev/video14| Orbbec #2                 | 彩色(副) | 640x480
    /dev/video16| Orbbec #2                 | 深度(副) | 640x480
    /dev/video18| Orbbec #2                 | 彩色     | 640x480

    采集时用 video10 + video18 作为 top/wrist 双目。
"""

import cv2
import argparse
import sys
from pathlib import Path

# ============================================================================
# 默认配置
# ============================================================================

# 所有可用彩色摄像头（按实际硬件映射，可按需增删）
DEFAULT_DEVICES = [
    "/dev/video0",   # 笔记本内置摄像头
    "/dev/video2",   # icSpring USB 摄像头
    "/dev/video10",  # Orbbec Gemini 335 #1 彩色流
    "/dev/video18",  # Orbbec Gemini 335 #2 彩色流
]

# V4L2 后端（Orbbec 必须用这个，FFMPEG 会读帧失败）
BACKEND = cv2.CAP_V4L2  # 值为 200

# 预热帧数：丢弃前几帧，等摄像头曝光稳定
WARMUP_FRAMES = 5


def capture_camera(dev_path: str, width: int, height: int, fourcc: str | None) -> tuple[bool, any]:
    """
    打开摄像头，预热后采集一帧。

    Args:
        dev_path:  设备路径，如 /dev/video10
        width:     请求宽度
        height:    请求高度
        fourcc:    四字符编码，如 "MJPG"；None 则自动选择

    Returns:
        (success, frame_bgr)  frame_bgr 为 BGR 格式的 numpy 数组
    """
    cap = cv2.VideoCapture(dev_path, BACKEND)
    if not cap.isOpened():
        return False, None

    try:
        # 设置分辨率
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, float(width))
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, float(height))

        # 设置 fourcc（如指定）
        if fourcc is not None:
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*fourcc))

        # 预热：丢弃前几帧，等曝光稳定
        for _ in range(WARMUP_FRAMES):
            cap.read()

        ret, frame = cap.read()
        if not ret or frame is None:
            return False, None

        # V4L2 后端读出来的帧默认是 BGR 格式，直接保存即可
        # 注意：LeRobot 内部会转成 RGB 用于模型推理，但 cv2.imwrite 需要 BGR
        frame_bgr = frame

        # 获取实际分辨率
        actual_h, actual_w = frame.shape[:2]
        return True, frame_bgr

    except Exception as e:
        print(f"    异常: {e}")
        return False, None
    finally:
        cap.release()


def main():
    parser = argparse.ArgumentParser(
        description="采集摄像头画面并保存为图片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--devices", nargs="+", default=DEFAULT_DEVICES,
        help=f"要采集的设备路径列表（默认: {' '.join(DEFAULT_DEVICES)}）",
    )
    parser.add_argument(
        "--output", type=str, default="outputs",
        help="输出目录（默认: outputs/）",
    )
    parser.add_argument(
        "--width", type=int, default=640,
        help="请求宽度（默认: 640）",
    )
    parser.add_argument(
        "--height", type=int, default=480,
        help="请求高度（默认: 480）",
    )
    parser.add_argument(
        "--fourcc", type=str, default=None,
        help="四字符编码，如 MJPG / YUYV（默认: 自动选择）",
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"输出目录: {output_dir.resolve()}")
    print(f"分辨率: {args.width}x{args.height}")
    print(f"Fourcc: {args.fourcc or '自动'}")
    print("-" * 50)

    ok_count = 0
    fail_count = 0

    for dev in args.devices:
        index = dev.split("/")[-1]  # e.g. "video10"
        print(f"采集 {dev} ...", end=" ", flush=True)

        success, frame_bgr = capture_camera(dev, args.width, args.height, args.fourcc)

        if success and frame_bgr is not None:
            h, w = frame_bgr.shape[:2]
            out_path = output_dir / f"{index}.jpg"
            cv2.imwrite(str(out_path), frame_bgr)
            print(f"OK  {w}x{h}  -> {out_path}")
            ok_count += 1
        else:
            print("失败")
            fail_count += 1

    print("-" * 50)
    print(f"完成！成功 {ok_count} 个，失败 {fail_count} 个")

    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
