# SO-101 机械臂 USB 端口映射表

> 目的：记录每台机械臂的固定 USB 端口（by-id），避免插拔后端口名（ttyACM0/1/2/3）变化导致命令失效

## 机械臂（串口）

| 臂名称 | 角色 (follower/leader) | by-id 路径 | 当前对应 |
|---|---|---|---|
| so101_cong_left | follower | /dev/serial/by-id/usb-1a86_USB_Single_Serial_5B42073876-if00 | ttyACM3 |
| so101_cong_right | follower | /dev/serial/by-id/usb-1a86_USB_Single_Serial_5B41532613-if00 | ttyACM1 |
| so101_zhu_left | leader | /dev/serial/by-id/usb-1a86_USB_Single_Serial_5B41533034-if00 | ttyACM2 |
| so101_zhu_right | leader | /dev/serial/by-id/usb-1a86_USB_Single_Serial_5B42137834-if00 | ttyACM0 |

## 相机

| 设备 | 固定路径 | 说明 |
|---|---|---|
| 相机0（主摄） | /dev/v4l/by-id/usb-Sonix_Technology_Co.__Ltd._USB2.0_HD_UVC_WebCam-video-index0 | → video0 |
| 相机1（副摄） | /dev/v4l/by-id/usb-Sonix_Technology_Co.__Ltd._USB2.0_HD_UVC_WebCam-video-index1 | → video1 |

> 注意：两个相机共用同一个 USB 物理端口（Bus 003 Device 005），是同一摄像头设备的不同端点，video-index0/1 基本固定

---

## 校准命令参考

```bash
# 从臂（follower）校准
python ~/le_xuan/SO101_calibrate/so101_cong_left.py
python ~/le_xuan/SO101_calibrate/so101_cong_right.py

# 主臂（leader）校准
python ~/le_xuan/SO101_calibrate/so101_zhu_left.py
python ~/le_xuan/SO101_calibrate/so101_zhu_right.py
```

> 注意：使用 by-id 路径，插拔顺序不影响端口识别
