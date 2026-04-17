"""
SO101 单臂数据采集脚本（带双摄像头）
基于 lerobot v0.5.1 API

使用方法：
  1. 确保机械臂已通电、USB已连接
  2. conda activate lerobot
  3. python record_so101_2cam.py                    # 默认：冲突时自动加时间戳
     python record_so101_2cam.py --name my_dataset  # 自定义数据集名
     python record_so101_2cam.py --overwrite         # 覆盖已有数据集

注意：
  - 数据集目录冲突时会自动追加时间戳，或用 --overwrite 覆盖

键盘控制：
  右箭头  → 提前结束当前 episode
  左箭头  → 重录当前 episode
  ESC     → 停止所有录制
"""

import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# ==================== 版本要求 ====================
# LeRobot 版本要求：lerobot (官方 v0.5.1, Python 3.12)
#   import 路径 so_follower / so_leader 仅在 v0.5.1 中存在
#   lerobot-seeed (v0.4.4) 使用旧路径 so101_follower / so101_leader，不兼容本脚本
# 运行环境：conda activate lerobot
# =====================================================================
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig
from lerobot.datasets.lerobot_dataset import LeRobotDataset
from lerobot.datasets.feature_utils import hw_to_dataset_features
from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
from lerobot.teleoperators.so_leader import SO101Leader, SO101LeaderConfig
from lerobot.utils.control_utils import init_keyboard_listener
from lerobot.utils.visualization_utils import init_rerun
from lerobot.scripts.lerobot_record import record_loop
from lerobot.processor import make_default_processors

# ==================== 配置区 ====================
NUM_EPISODES = 50              # 采集 episode 数量
FPS = 30                       # 帧率
EPISODE_TIME_SEC = 60          # 每个 episode 最长录制时间（秒）
RESET_TIME_SEC = 10            # 重置环境时间（秒）
TASK_DESCRIPTION = "grab_red_cube"  # 任务描述
DATASET_REPO_ID = "Ready321/so101_grab_redcube"  # HF 数据集名称

# 摄像头索引
TOP_CAM = 10      # 俯视摄像头 (video10)
WRIST_CAM = 2     # 腕部摄像头 (video2)

# 从臂（follower）— 串口 by-id
FOLLOWER_PORT = "/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B42073876-if00"
FOLLOWER_ID = "so101_cong_left"

# 主臂（leader）— 串口 by-id
LEADER_PORT = "/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B41533034-if00"
LEADER_ID = "so101_zhu_left"
# ================================================

# 赋予串口权限
os.system("sudo chmod 666 /dev/ttyACM* /dev/ttyUSB* 2>/dev/null")

# 从臂配置（含双摄像头）
robot_config = SO101FollowerConfig(
    id=FOLLOWER_ID,
    port=FOLLOWER_PORT,
    cameras={
        "top": OpenCVCameraConfig(index_or_path=TOP_CAM, width=640, height=480, fps=FPS),
        "wrist": OpenCVCameraConfig(index_or_path=WRIST_CAM, width=640, height=480, fps=FPS),
    },
)

# 主臂配置
teleop_config = SO101LeaderConfig(
    id=LEADER_ID,
    port=LEADER_PORT,
)

# 初始化机器人
robot = SO101Follower(robot_config)
teleop = SO101Leader(teleop_config)

# 生成 dataset features
action_features = hw_to_dataset_features(robot.action_features, "action")
obs_features = hw_to_dataset_features(robot.observation_features, "observation")
dataset_features = {**action_features, **obs_features}

print(f"action_features:   {action_features}")
print(f"obs_features:      {obs_features}")

# 创建数据集（含重复检测）
LEROBOT_CACHE_ROOT = Path.home() / ".cache" / "huggingface" / "lerobot"

# 解析命令行参数
custom_name = None
overwrite = False
args = sys.argv[1:]
i = 0
while i < len(args):
    if args[i] == "--name" and i + 1 < len(args):
        custom_name = args[i + 1]
        i += 2
    elif args[i] == "--overwrite":
        overwrite = True
        i += 1
    else:
        print(f"未知参数: {args[i]}")
        print("用法: python record_so101_2cam.py [--name <数据集名>] [--overwrite]")
        sys.exit(1)

# 确定最终的 DATASET_REPO_ID
if custom_name:
    username = DATASET_REPO_ID.split("/")[0]
    DATASET_REPO_ID = f"{username}/{custom_name}"

dataset_local_path = LEROBOT_CACHE_ROOT / DATASET_REPO_ID

if dataset_local_path.exists():
    if overwrite:
        print(f"[覆盖模式] 删除已有数据集：{dataset_local_path}")
        shutil.rmtree(dataset_local_path)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        username = DATASET_REPO_ID.split("/")[0]
        base_name = DATASET_REPO_ID.split("/")[1]
        new_name = f"{base_name}_{timestamp}"
        DATASET_REPO_ID = f"{username}/{new_name}"
        dataset_local_path = LEROBOT_CACHE_ROOT / DATASET_REPO_ID
        print(f"[自动重命名] 数据集目录已存在，新数据集：{DATASET_REPO_ID}")
        print(f"  旧目录保留在：{LEROBOT_CACHE_ROOT / (username + '/' + base_name)}")
        print(f"  如需覆盖旧数据，请使用 --overwrite 参数重新运行")
else:
    print(f"[新建] 数据集将创建在：{dataset_local_path}")

print(f"最终 DATASET_REPO_ID = {DATASET_REPO_ID}")

dataset = LeRobotDataset.create(
    repo_id=DATASET_REPO_ID,
    fps=FPS,
    features=dataset_features,
    robot_type=robot.name,
    use_videos=True,
    image_writer_threads=4,
)

# 键盘监听 & rerun 可视化
_, events = init_keyboard_listener()
init_rerun(session_name="recording")

# 连接设备
print("正在连接设备...")
robot.connect()
teleop.connect()
print("连接成功！")

# 创建处理器
teleop_action_processor, robot_action_processor, robot_observation_processor = make_default_processors()

# 录制循环
episode_idx = 0
while episode_idx < NUM_EPISODES and not events["stop_recording"]:
    print(f"\n{'='*50}")
    print(f"  录制 Episode {episode_idx + 1} / {NUM_EPISODES}")
    print(f"{'='*50}")

    record_loop(
        robot=robot,
        events=events,
        fps=FPS,
        teleop_action_processor=teleop_action_processor,
        robot_action_processor=robot_action_processor,
        robot_observation_processor=robot_observation_processor,
        teleop=teleop,
        dataset=dataset,
        control_time_s=EPISODE_TIME_SEC,
        single_task=TASK_DESCRIPTION,
        display_data=True,
    )

    # 如果没有停止，重置环境
    if not events["stop_recording"] and (episode_idx < NUM_EPISODES - 1 or events["rerecord_episode"]):
        print("重置环境中...")
        record_loop(
            robot=robot,
            events=events,
            fps=FPS,
            teleop_action_processor=teleop_action_processor,
            robot_action_processor=robot_action_processor,
            robot_observation_processor=robot_observation_processor,
            teleop=teleop,
            control_time_s=RESET_TIME_SEC,
            single_task=TASK_DESCRIPTION,
            display_data=True,
        )

    # 重录处理
    if events["rerecord_episode"]:
        print("重录当前 episode")
        events["rerecord_episode"] = False
        events["exit_early"] = False
        dataset.clear_episode_buffer()
        continue

    dataset.save_episode()
    episode_idx += 1

# 清理
print("\n录制结束，正在保存...")
robot.disconnect()
teleop.disconnect()
print(f"共录制 {episode_idx} 个 episode")
print("如需上传到 HuggingFace Hub，运行：")
print(f"  dataset.push_to_hub()")
