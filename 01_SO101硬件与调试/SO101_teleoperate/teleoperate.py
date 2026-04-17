from lerobot.teleoperators.so_leader import SO101LeaderConfig, SO101Leader
from lerobot.robots.so_follower import SO101FollowerConfig, SO101Follower
import os

# 在连接前自动赋予所有常见串口权限（运行脚本时可能需要输入密码）
os.system("sudo chmod 666 /dev/ttyACM* /dev/ttyUSB* 2>/dev/null")

so101_cong_left = SO101FollowerConfig(
    port="/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B42073876-if00",
    id="so101_cong_left",
)

so101_cong_right = SO101FollowerConfig(
    port="/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B41532613-if00",
    id="so101_cong_right",
)

so101_zhu_left = SO101LeaderConfig(
    port="/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B41533034-if00",
    id="so101_zhu_left",
)

so101_zhu_right = SO101LeaderConfig(
    port="/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B42137834-if00",
    id="so101_zhu_right",
)



def main():
    print("=" * 50)
    print("      🌟 欢迎使用 SO101 遥操作控制系统 🌟")
    print("=" * 50)
    print("请选择你的遥操作模式：")
    print("  [1] 一对一遥操作 (单臂控制单主从臂)")
    print("  [2] 一对多遥操作 (单主臂同步控制双从臂)")
    print("  [3] 双臂遥操作   (双主臂独立控制双从臂)")
    print("=" * 50)
    
    mode = input("输入选项数字 (1/2/3) 并回车: ").strip()

    if mode == "1":
        print("\n您选择了【一对一遥操作】")
        print("  [1] 左主臂 🎮 -> 左从臂 🤖")
        print("  [2] 右主臂 🎮 -> 右从臂 🤖")
        sub_mode = input("选择要使用的手臂对 (1/2): ").strip()
        
        if sub_mode == "1":
            l_cfg, f_cfg = so101_zhu_left, so101_cong_left
        else:
            l_cfg, f_cfg = so101_zhu_right, so101_cong_right

        print("\n🔧 正在连接设备...")
        leader = SO101Leader(l_cfg)
        follower = SO101Follower(f_cfg)
        leader.connect()
        follower.connect()
        print("✅ 连接成功！按 Ctrl+C 退出遥操作。")

        try:
            while True:
                follower.send_action(leader.get_action())
        except KeyboardInterrupt:
            print("\n🛑 正在停止运行...")
        finally:
            leader.disconnect()
            follower.disconnect()
            print("已安全断开连接。")

    elif mode == "2":
        print("\n您选择了【一对多遥操作】(右主臂同步控制左、右从臂)")
        print("\n🔧 正在连接设备...")
        
        # 默认使用右主控控制两个从控（如果想改为主左臂可自行更换 so101_zhu_right 为 left）
        leader = SO101Leader(so101_zhu_right)
        f_left = SO101Follower(so101_cong_left)
        f_right = SO101Follower(so101_cong_right)
        
        leader.connect()
        f_left.connect()
        f_right.connect()
        print("✅ 连接成功！按 Ctrl+C 退出遥操作。")

        try:
            while True:
                action = leader.get_action()
                f_left.send_action(action)
                f_right.send_action(action)
        except KeyboardInterrupt:
            print("\n🛑 正在停止运行...")
        finally:
            leader.disconnect()
            f_left.disconnect()
            f_right.disconnect()
            print("已安全断开连接。")

    elif mode == "3":
        print("\n您选择了【双臂遥操作】(左控左，右控右)")
        print("\n🔧 正在连接设备...")
        
        leader_l = SO101Leader(so101_zhu_left)
        leader_r = SO101Leader(so101_zhu_right)
        follower_l = SO101Follower(so101_cong_left)
        follower_r = SO101Follower(so101_cong_right)
        
        leader_l.connect()
        leader_r.connect()
        follower_l.connect()
        follower_r.connect()
        print("✅ 连接成功！按 Ctrl+C 退出遥操作。")

        try:
            while True:
                follower_l.send_action(leader_l.get_action())
                follower_r.send_action(leader_r.get_action())
        except KeyboardInterrupt:
            print("\n🛑 正在停止运行...")
        finally:
            leader_l.disconnect()
            leader_r.disconnect()
            follower_l.disconnect()
            follower_r.disconnect()
            print("已安全断开连接。")
            
    else:
        print("❌ 无效的选择，请重新运行脚本。")

if __name__ == "__main__":
    main()