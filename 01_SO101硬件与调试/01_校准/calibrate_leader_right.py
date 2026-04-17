import os
from lerobot.teleoperators.so_leader import SO101LeaderConfig, SO101Leader

def grant_port_permissions():
    """自动赋予所有常见串口权限"""
    print("正在申请串口权限...")
    os.system("sudo chmod 666 /dev/ttyACM* /dev/ttyUSB* 2>/dev/null")
    print("权限赋予完成")

grant_port_permissions()

config = SO101LeaderConfig(
    port="/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B42137834-if00",
    id="so101_zhu_right",
)

leader = SO101Leader(config)
leader.connect(calibrate=False)
leader.calibrate()
leader.disconnect()