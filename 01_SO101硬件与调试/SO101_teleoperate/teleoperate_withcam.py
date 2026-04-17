# LeRobot 版本要求：lerobot (官方 v0.5.1, Python 3.12)
#   import 路径 so_follower / so_leader 仅在 v0.5.1 中存在
#   lerobot-seeed (v0.4.4) 使用旧路径 so101_follower / so101_leader，不兼容本脚本
# 运行环境：conda activate lerobot
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig
from lerobot.teleoperators.so_leader import SO101LeaderConfig, SO101Leader
from lerobot.robots.so_follower import SO101FollowerConfig, SO101Follower
import os
import cv2
import numpy as np

# 在连接前自动赋予所有常见串口权限（运行脚本时可能需要输入密码）
os.system("sudo chmod 666 /dev/ttyACM* /dev/ttyUSB* 2>/dev/null")

# 摄像头索引：video2=俯视(1920x1080), video8=腕部(640x400)
# 注意：video10是video8的metadata设备，不能读帧
top_cam = 10
wrist_cam = 2

so101_cong_left = SO101FollowerConfig(
    port="/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B42073876-if00",
    id="so101_cong_left",
    cameras={
        "top": OpenCVCameraConfig(index_or_path=top_cam, width=1920, height=1080, fps=30),
        "wrist": OpenCVCameraConfig(index_or_path=wrist_cam, width=640, height=480, fps=30),
    },
)

so101_zhu_left = SO101LeaderConfig(
    port="/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B41533034-if00",
    id="so101_zhu_left",
)

teleop_device = SO101Leader(so101_zhu_left)
robot = SO101Follower(so101_cong_left)

print("正在连接设备...")
teleop_device.connect()
robot.connect()
print("连接成功！按 Ctrl+C 退出。")

# 先读一次observation看看内容
obs = robot.get_observation()
print(f"observation keys: {list(obs.keys())}")
for k, v in obs.items():
    if isinstance(v, np.ndarray):
        print(f"  {k}: ndarray shape={v.shape}, dtype={v.dtype}")
    else:
        print(f"  {k}: {type(v).__name__} = {v}")

try:
    while True:
        observation = robot.get_observation()
        action = teleop_device.get_action()
        robot.send_action(action)

        # 显示摄像头画面
        for cam_name in ["top", "wrist"]:
            if cam_name in observation:
                frame = observation[cam_name]
                if isinstance(frame, np.ndarray) and frame.ndim == 3:
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    # 缩小画面以便显示
                    h, w = frame.shape[:2]
                    scale = min(800 / w, 600 / h)
                    if scale < 1.0:
                        frame = cv2.resize(frame, (int(w * scale), int(h * scale)))
                    cv2.imshow(cam_name, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
except KeyboardInterrupt:
    print("\n正在停止...")
finally:
    teleop_device.disconnect()
    robot.disconnect()
    cv2.destroyAllWindows()
    print("已安全断开连接。")
