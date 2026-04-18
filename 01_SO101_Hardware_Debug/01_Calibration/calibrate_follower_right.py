import os
from lerobot.robots.so_follower import SO101FollowerConfig, SO101Follower

# 在连接前自动赋予所有常见串口权限（运行脚本时可能需要输入密码）
os.system("sudo chmod 666 /dev/ttyACM* /dev/ttyUSB* 2>/dev/null")

config = SO101FollowerConfig(
    port="/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B41532613-if00",
    id="so101_cong_right",
)

follower = SO101Follower(config)
follower.connect(calibrate=False)
follower.calibrate()
follower.disconnect()