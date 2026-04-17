#!/usr/bin/env python3
"""
SO-101 三相机遥操作程序
=======================

功能：SO-101 单臂遥操作 + 三相机画面实时显示（wrist/front/top）

使用方法：
    conda activate lerobot
    python teleoperate_3cam.py

    # 自定义相机 index
    python teleoperate_3cam.py --wrist 2 --front 10 --top 18

    # 自定义串口
    python teleoperate_3cam.py --follower-port /dev/ttyACM1 --leader-port /dev/ttyACM0

按键：
    q - 退出
    s - 截图保存到 shots/ 目录

---

【踩坑记录】

1. Orbbec 摄像头必须指定 backend=cv2.CAP_V4L2 (200)，
   否则 FFMPEG 后端读帧失败。已在 OpenCVCameraConfig 中设置。

2. 相机 name（"wrist"/"front"/"top"）决定了 LeRobot 数据集中
   observation.images 的子目录名，改了需重新采集。

3. 640x480@30fps 是 Orbbec 彩色流稳定配置，不建议采集时用更高分辨率。

4. LeRobot get_observation() 返回的帧是 RGB 格式，cv2.imshow 需要 BGR，
   需手动 cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)。

5. cameras 必须放在 FollowerConfig 里，不能放 LeaderConfig。

6. 串口权限：脚本开头自动 chmod 666，若失败需手动 sudo。

7. lerobot v0.5.1 import 路径：so_follower / so_leader（非 so101_*）。

8. 串口通信偶尔丢包（"There is no status packet!"）是正常现象，
   脚本已加重试逻辑，单次失败不会崩溃。

9. QFont 警告 "Cannot find font directory" 是 OpenCV 的 Qt 字体问题，
   不影响功能，脚本已自动抑制。
"""

import os
import sys
import argparse
import time
import logging
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np

from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig
from lerobot.teleoperators.so_leader import SO101LeaderConfig, SO101Leader
from lerobot.robots.so_follower import SO101FollowerConfig, SO101Follower

# 抑制 OpenCV Qt 字体警告
os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.qpa.fonts=false"

# ============================================================================
# 默认配置
# ============================================================================

# 串口 by-id（比 /dev/ttyACM* 更稳定，不随插拔顺序变化）
DEFAULT_FOLLOWER_PORT = "/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B42073876-if00"
DEFAULT_LEADER_PORT = "/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B41533034-if00"

# 相机默认 index —— 用整数（与录制脚本一致，字符串路径可能导致后端选择差异）
DEFAULT_WRIST_CAM = 2    # icSpring USB 或 Orbbec 彩色
DEFAULT_FRONT_CAM = 18   # Orbbec #1 彩色
DEFAULT_TOP_CAM = 10     # Orbbec #2 彩色

# 分辨率与帧率
CAM_WIDTH = 640
CAM_HEIGHT = 480
CAM_FPS = 30

# 串口通信重试
MAX_RETRY = 3
RETRY_DELAY = 0.1  # 秒

# 截图保存目录
SHOTS_DIR = Path("shots")


def parse_args():
    parser = argparse.ArgumentParser(
        description="SO-101 三相机遥操作程序",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--wrist", type=int, default=DEFAULT_WRIST_CAM,
                        help=f"腕部相机 index（默认: {DEFAULT_WRIST_CAM}）")
    parser.add_argument("--front", type=int, default=DEFAULT_FRONT_CAM,
                        help=f"正面相机 index（默认: {DEFAULT_FRONT_CAM}）")
    parser.add_argument("--top", type=int, default=DEFAULT_TOP_CAM,
                        help=f"顶部相机 index（默认: {DEFAULT_TOP_CAM}）")
    parser.add_argument("--follower-port", type=str, default=DEFAULT_FOLLOWER_PORT,
                        help="从臂串口路径")
    parser.add_argument("--leader-port", type=str, default=DEFAULT_LEADER_PORT,
                        help="主臂串口路径")
    parser.add_argument("--no-cam", action="store_true",
                        help="不使用相机，仅遥操作")
    return parser.parse_args()


def safe_disconnect(device, name="device"):
    """安全断开设备，忽略断开时的通信错误"""
    try:
        device.disconnect()
    except Exception as e:
        print(f"  {name} 断开时出错（可忽略）: {e}")


def retry_call(fn, description, max_retry=MAX_RETRY, delay=RETRY_DELAY):
    """
    带重试的函数调用，用于串口通信可能丢包的场景。
    返回 (success, result_or_None)
    """
    for attempt in range(1, max_retry + 1):
        try:
            result = fn()
            return True, result
        except ConnectionError as e:
            if attempt < max_retry:
                print(f"  [{description}] 第{attempt}次失败，重试... ({e})")
                time.sleep(delay)
            else:
                print(f"  [{description}] {max_retry}次重试均失败: {e}")
                return False, None
        except Exception as e:
            print(f"  [{description}] 异常: {e}")
            return False, None


def main():
    args = parse_args()

    # 赋予串口权限
    os.system("sudo chmod 666 /dev/ttyACM* /dev/ttyUSB* 2>/dev/null")

    # ------------------------------------------------------------------
    # 构建相机配置
    # ------------------------------------------------------------------
    if args.no_cam:
        cameras = {}
    else:
        cameras = {
            "top": OpenCVCameraConfig(
                index_or_path=args.top,
                width=CAM_WIDTH, height=CAM_HEIGHT, fps=CAM_FPS,
            ),
            "wrist": OpenCVCameraConfig(
                index_or_path=args.wrist,
                width=CAM_WIDTH, height=CAM_HEIGHT, fps=CAM_FPS,
            ),
            "front": OpenCVCameraConfig(
                index_or_path=args.front,
                width=CAM_WIDTH, height=CAM_HEIGHT, fps=CAM_FPS,
            ),
        }

    # ------------------------------------------------------------------
    # 构建机械臂配置
    # ------------------------------------------------------------------
    follower_cfg = SO101FollowerConfig(
        port=args.follower_port,
        id="so101_cong_left",
        cameras=cameras,
    )
    leader_cfg = SO101LeaderConfig(
        port=args.leader_port,
        id="so101_zhu_left",
    )

    # ------------------------------------------------------------------
    # 连接设备
    # ------------------------------------------------------------------
    print("=" * 55)
    print("       SO-101 三相机遥操作")
    print("=" * 55)
    print(f"  从臂: {args.follower_port}")
    print(f"  主臂: {args.leader_port}")
    if cameras:
        print(f"  腕部相机: video{args.wrist}")
        print(f"  正面相机: video{args.front}")
        print(f"  顶部相机: video{args.top}")
    else:
        print("  相机: 未启用")
    print("-" * 55)
    print("正在连接设备...")

    leader = SO101Leader(leader_cfg)
    follower = SO101Follower(follower_cfg)

    try:
        leader.connect()
        follower.connect()
    except Exception as e:
        print(f"连接失败: {e}")
        safe_disconnect(leader, "主臂")
        safe_disconnect(follower, "从臂")
        sys.exit(1)

    print("连接成功！")
    print("  按 Ctrl+C 或 q 退出")
    print("  按 s 截图保存")
    print("=" * 55)

    # 打印 observation 结构
    ok, obs = retry_call(follower.get_observation, "首次读取observation")
    if ok and obs:
        print(f"\nobservation keys: {list(obs.keys())}")
        for k, v in obs.items():
            if isinstance(v, np.ndarray):
                print(f"  {k}: shape={v.shape}, dtype={v.dtype}")
            else:
                print(f"  {k}: {type(v).__name__} = {v}")
        print()
    else:
        print("\n首次读取 observation 失败，但仍继续运行...\n")

    # ------------------------------------------------------------------
    # 遥操作主循环
    # ------------------------------------------------------------------
    SHOTS_DIR.mkdir(exist_ok=True)
    cam_names = ["wrist", "front", "top"]
    consecutive_failures = 0
    MAX_CONSECUTIVE_FAILURES = 10  # 连续失败超过此数则退出

    try:
        while True:
            # 遥操作：主臂 -> 从臂（核心操作，必须成功）
            ok, action = retry_call(leader.get_action, "主臂读取")
            if ok and action is not None:
                ok2, _ = retry_call(
                    lambda: follower.send_action(action), "从臂执行"
                )
                if ok2:
                    consecutive_failures = 0
                else:
                    consecutive_failures += 1
            else:
                consecutive_failures += 1

            # 连续失败过多，可能断线
            if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                print(f"\n连续 {MAX_CONSECUTIVE_FAILURES} 次通信失败，可能断线，退出。")
                break

            # 获取观察（含相机画面）—— 允许失败，不影响遥操作
            observation = None
            if cameras:
                ok, observation = retry_call(
                    follower.get_observation, "相机读取", max_retry=1
                )

            if observation:
                for cam_name in cam_names:
                    if cam_name not in observation:
                        continue
                    frame = observation[cam_name]
                    if not isinstance(frame, np.ndarray) or frame.ndim != 3:
                        continue

                    # LeRobot 返回 RGB，imshow 需要 BGR
                    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                    # 画面缩放（3个窗口并排不要太挤）
                    h, w = frame_bgr.shape[:2]
                    scale = min(400 / w, 300 / h)
                    if scale < 1.0:
                        frame_bgr = cv2.resize(
                            frame_bgr,
                            (int(w * scale), int(h * scale)),
                            interpolation=cv2.INTER_AREA,
                        )

                    # 在画面上标注相机名称
                    cv2.putText(
                        frame_bgr, cam_name, (8, 24),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2,
                    )
                    cv2.imshow(cam_name, frame_bgr)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord("s"):
                # 截图
                if observation:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    for cam_name in cam_names:
                        if cam_name not in observation:
                            continue
                        frame = observation[cam_name]
                        if isinstance(frame, np.ndarray) and frame.ndim == 3:
                            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                            path = SHOTS_DIR / f"{timestamp}_{cam_name}.jpg"
                            cv2.imwrite(str(path), frame_bgr)
                    print(f"截图已保存到 {SHOTS_DIR}/")
                else:
                    print("当前无画面，无法截图")

    except KeyboardInterrupt:
        print("\n正在停止...")
    finally:
        safe_disconnect(leader, "主臂")
        safe_disconnect(follower, "从臂")
        cv2.destroyAllWindows()
        print("已安全断开连接。")


if __name__ == "__main__":
    main()
