"""
SO101 单臂数据采集脚本（带三摄像头）
基于 lerobot v0.5.1 API（conda 环境：lerobot，Python 3.12）

三机位说明：
  - top：   俯视摄像头，全局视角，观察桌面和物体位置
  - wrist： 腕部摄像头，跟随机械臂运动，近距离观察抓取细节
  - side：  侧面摄像头，提供深度信息，辅助判断物体与夹爪的相对距离

使用方法：
  1. 确保机械臂已通电、USB 已连接
  2. 确保三个摄像头已连接，可用 v4l2-ctl --list-devices 确认索引
  3. conda activate lerobot
  4. python record_so101_3cam.py                      # 默认：冲突时自动加时间戳
     python record_so101_3cam.py --name my_dataset    # 自定义数据集名
     python record_so101_3cam.py --overwrite           # 覆盖已有数据集

注意：
  - 三摄像头同时采集会加重 USB 带宽负担，如遇丢帧可降低分辨率或帧率
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
# --- 采集参数 ---
NUM_EPISODES = 50                  # 采集 episode 总数
FPS = 30                           # 采集帧率（三摄像头共用）
EPISODE_TIME_SEC = 60              # 每个 episode 最长录制时间（秒）
RESET_TIME_SEC = 10                # 每两个 episode 间重置环境的时间（秒）
TASK_DESCRIPTION = "grab_red_cube" # 任务描述标签，会写入数据集 metadata
DATASET_REPO_ID = "Ready321/so101_grab_redcube_3cam"  # HuggingFace 数据集仓库 ID

# --- 摄像头索引 ---
# 用 v4l2-ctl --list-devices 查看设备名和索引号的对应关系
# 注意：video N+1（如 video3）通常是 video N 的 metadata 设备，不可读帧
TOP_CAM = 10       # 俯视摄像头（video10）
WRIST_CAM = 2      # 腕部摄像头（video2）
SIDE_CAM = 18       # 侧面摄像头（video8）—— 请根据实际连接情况修改

# --- 摄像头分辨率 ---
# 三摄像头同时工作，USB 带宽有限，建议分辨率统一 640x480
# 若带宽不足导致丢帧，可降到 320x240 或降低 FPS
CAM_WIDTH = 640
CAM_HEIGHT = 480

# --- 从臂（follower）串口配置 ---
# 通过 by-id 路径指定，比 /dev/ttyACM0 更稳定（不随插拔顺序变化）
# 可用 ls /dev/serial/by-id/ 查看实际路径
FOLLOWER_PORT = "/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B42073876-if00"
FOLLOWER_ID = "so101_cong_left"

# --- 主臂（leader）串口配置 ---
LEADER_PORT = "/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B41533034-if00"
LEADER_ID = "so101_zhu_left"
# ================================================

# 在连接串口前自动赋予读写权限（可能需要输入 sudo 密码）
os.system("sudo chmod 666 /dev/ttyACM* /dev/ttyUSB* 2>/dev/null")

# ==================== 从臂配置（含三摄像头） ====================
#
# cameras 字典的 key（如 "top"、"wrist"、"side"）会作为数据集中
# observation.images.<key> 的字段名，后续训练和推理时需保持一致。
#
# OpenCVCameraConfig 参数说明：
#   index_or_path: 摄像头索引号或设备路径（如 /dev/video2）
#   width/height:  采集分辨率
#   fps:           目标帧率
#   fourcc:        编码格式，None 表示使用摄像头默认格式
#                  （本机摄像头不要指定 fourcc，否则报 buf.empty 错误）
#
robot_config = SO101FollowerConfig(
    id=FOLLOWER_ID,
    port=FOLLOWER_PORT,
    cameras={
        "top": OpenCVCameraConfig(
            index_or_path=TOP_CAM,
            width=CAM_WIDTH,
            height=CAM_HEIGHT,
            fps=FPS,
        ),
        "wrist": OpenCVCameraConfig(
            index_or_path=WRIST_CAM,
            width=CAM_WIDTH,
            height=CAM_HEIGHT,
            fps=FPS,
        ),
        "side": OpenCVCameraConfig(
            index_or_path=SIDE_CAM,
            width=CAM_WIDTH,
            height=CAM_HEIGHT,
            fps=FPS,
        ),
    },
)

# ==================== 主臂配置 ====================
teleop_config = SO101LeaderConfig(
    id=LEADER_ID,
    port=LEADER_PORT,
)

# ==================== 初始化设备 ====================
# 创建从臂和主臂实例（此时还未连接硬件）
robot = SO101Follower(robot_config)
teleop = SO101Leader(teleop_config)

# ==================== 数据集特征定义 ====================
# hw_to_dataset_features 将硬件特征转为数据集可存储的格式
# action_features：记录主臂发出的动作指令（关节角度）
# obs_features：记录从臂的观测数据（关节角度 + 三个摄像头的图像）
action_features = hw_to_dataset_features(robot.action_features, "action")
obs_features = hw_to_dataset_features(robot.observation_features, "observation")
dataset_features = {**action_features, **obs_features}

print(f"action_features:   {action_features}")
print(f"obs_features:      {obs_features}")
# obs_features 中应包含 observation.images.top / wrist / side 三个图像字段

# ==================== 重复数据集检测与处理 ====================
#
# LeRobotDataset.create 要求目标目录不存在，否则报 FileExistsError。
# 此处检测三种处理方式（按优先级）：
#   1. 命令行传入 --name <自定义名>：使用自定义数据集名
#   2. 命令行传入 --overwrite：删除旧数据集目录后重新创建
#   3. 默认行为：自动追加时间戳后缀，避免冲突
#
# LeRobot 本地缓存根目录
LEROBOT_CACHE_ROOT = Path.home() / ".cache" / "huggingface" / "lerobot"

# 解析命令行参数
# 用法示例：
#   python record_so101_3cam.py                    # 默认：冲突时自动加时间戳
#   python record_so101_3cam.py --name my_dataset  # 自定义数据集名（仅名称部分，不含用户名）
#   python record_so101_3cam.py --overwrite        # 删除旧数据集，重新开始
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
        print("用法: python record_so101_3cam.py [--name <数据集名>] [--overwrite]")
        sys.exit(1)

# 确定最终的 DATASET_REPO_ID
if custom_name:
    # --name 只替换 repo_id 的名称部分，用户名保持不变
    username = DATASET_REPO_ID.split("/")[0]
    DATASET_REPO_ID = f"{username}/{custom_name}"

dataset_local_path = LEROBOT_CACHE_ROOT / DATASET_REPO_ID

if dataset_local_path.exists():
    if overwrite:
        # --overwrite：删除旧目录后重建
        print(f"[覆盖模式] 删除已有数据集：{dataset_local_path}")
        shutil.rmtree(dataset_local_path)
    else:
        # 默认：自动追加时间戳后缀（格式：_YYYYMMDD_HHMMSS）
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

# 创建数据集（此时目录已确认不存在，不会报 FileExistsError）
dataset = LeRobotDataset.create(
    repo_id=DATASET_REPO_ID,
    fps=FPS,
    features=dataset_features,
    robot_type=robot.name,
    use_videos=True,
    image_writer_threads=4,
)
# ============================================================

# ==================== 键盘监听 & 可视化 ====================
# init_keyboard_listener: 注册键盘事件（左右箭头、ESC）
# init_rerun: 初始化 Rerun 可视化工具（实时查看采集画面）
_, events = init_keyboard_listener()
init_rerun(session_name="recording_3cam")

# ==================== 连接硬件 ====================
print("正在连接设备...")
robot.connect()   # 连接从臂 + 初始化三个摄像头
teleop.connect()  # 连接主臂
print("连接成功！三个摄像头：top(俯视), wrist(腕部), side(侧面)")

# ==================== 创建数据处理器 ====================
# 处理器负责在采集循环中对动作/观测数据进行预处理
# 默认处理器通常做归一化、格式转换等操作
teleop_action_processor, robot_action_processor, robot_observation_processor = make_default_processors()

# ==================== 录制主循环 ====================
#
# 流程：每个 episode 包含两个阶段
#   1. 录制阶段（EPISODE_TIME_SEC）：用户遥控操作，数据自动采集
#   2. 重置阶段（RESET_TIME_SEC）：用户将物体/环境恢复初始状态，
#      此阶段也采集数据但不保存为正式 episode
#
# 键盘事件处理：
#   - exit_early：按右箭头，提前结束当前 episode（已采集数据保留）
#   - rerecord_episode：按左箭头，丢弃当前 episode 并重新录制
#   - stop_recording：按 ESC，停止所有录制并退出
#
episode_idx = 0
while episode_idx < NUM_EPISODES and not events["stop_recording"]:
    print(f"\n{'='*50}")
    print(f"  录制 Episode {episode_idx + 1} / {NUM_EPISODES}")
    print(f"{'='*50}")

    # ---- 阶段1：正式录制 ----
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
        display_data=True,  # True 表示在 Rerun 中实时显示画面
    )

    # ---- 阶段2：重置环境 ----
    # 如果未按 ESC 停止，且不是最后一个 episode（或需要重录），则进入重置阶段
    if not events["stop_recording"] and (episode_idx < NUM_EPISODES - 1 or events["rerecord_episode"]):
        print("重置环境中...（请将物体放回初始位置）")
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

    # ---- 重录处理 ----
    # 如果按了左箭头，清除当前 episode 的缓冲数据，不递增计数，重新录制
    if events["rerecord_episode"]:
        print("重录当前 episode")
        events["rerecord_episode"] = False
        events["exit_early"] = False
        dataset.clear_episode_buffer()
        continue

    # ---- 保存当前 episode ----
    # 将缓冲区数据写入磁盘（视频文件 + parquet 元数据）
    dataset.save_episode()
    episode_idx += 1

# ==================== 录制结束，清理资源 ====================
print("\n录制结束，正在保存...")
robot.disconnect()   # 断开从臂 + 释放摄像头
teleop.disconnect()  # 断开主臂
print(f"共录制 {episode_idx} 个 episode")
print(f"数据集本地路径：~/.cache/huggingface/lerobot/{DATASET_REPO_ID}")
print("如需上传到 HuggingFace Hub，在 Python 中运行：")
print(f"  from lerobot.datasets.lerobot_dataset import LeRobotDataset")
print(f"  ds = LeRobotDataset('{DATASET_REPO_ID}')")
print(f"  ds.push_to_hub()")
