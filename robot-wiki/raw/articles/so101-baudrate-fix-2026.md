# SO-101 机械臂通信失败修复记录

## 问题描述

使用 `lerobot-teleoperate` 进行主从遥操作时，从臂（follower）报错：

```
ConnectionError: Failed to sync read 'Present_Position' on ids=[1, 2, 3, 4, 5, 6] after 1 tries.
[TxRxResult] There is no status packet!
```

校准（lerobot-calibrate）可通过，但遥操作时无法读取舵机位置。

## 环境信息

- 机械臂：SO-101（Feetech STS 系列舵机）
- USB转串口芯片：沁恒 CH9101F（1a86:55d3，cdc_acm 驱动）
- 系统识别为 /dev/ttyACM0、/dev/ttyACM1
- LeRobot 版本：0.4.4
- 安装方式：pip install -e（editable 模式）

## 排查过程

### 1. 权限排查

首次运行时出现 Permission denied，通过 `sudo chmod 666 /dev/ttyACM*` 临时解决。
长期方案：将用户加入 dialout 组，重启后永久生效。

```bash
sudo usermod -aG dialout $USER
```

### 2. 通信排查

使用 scservo_sdk 逐波特率 ping 电机：

```python
from scservo_sdk import PortHandler, PacketHandler

for baud in [9600, 19200, 38400, 57600, 115200, 128000, 250000, 500000, 1000000]:
    port = PortHandler('/dev/ttyACM0')
    port.openPort()
    port.setBaudRate(baud)
    ph = PacketHandler(0)
    stat, err, _ = ph.ping(port, 1)
    print(f'baud={baud}: {"OK" if stat == 0 else "FAILED"}')
    port.closePort()
```

结果：

| 波特率  | 结果   |
|---------|--------|
| 9600    | OK     |
| 19200   | OK     |
| 38400   | OK     |
| 57600   | OK     |
| 115200  | OK     |
| 128000  | OK     |
| 250000  | OK     |
| 500000  | OK     |
| 1000000 | FAILED |

唯独 1000000 bps 无法通信，而 LeRobot 的默认波特率恰好是 1000000。

### 3. 读取电机实际波特率

在 115200 下读取波特率寄存器（地址 3），返回值为 0。按 Feetech STS 协议，寄存器值 0 对应 1000000 bps，但实测 1000000 无法通信。原因是 CH9101F 芯片在 ACM 模式下对 1Mbps 支持不稳定。

## 根因

LeRobot 在 `feetech.py` 中硬编码默认波特率为 1000000：

```python
# 文件：src/lerobot/motors/feetech/feetech.py
DEFAULT_BAUDRATE = 1_000_000
```

而 CH9101F USB转串口芯片在 1Mbps 下通信不可靠，导致所有舵机返回 "no status packet"。

## 修复方法

### 修改默认波特率

将 `~/lerobot/src/lerobot/motors/feetech/feetech.py` 中的：

```python
DEFAULT_BAUDRATE = 1_000_000
```

改为：

```python
DEFAULT_BAUDRATE = 500_000
```

由于是 editable 安装，修改后立即生效，无需重新安装。

### 重新校准

修改波特率后，旧的校准文件不再适用，需要重新校准：

```bash
# 校准从臂
lerobot-calibrate \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM0 \
    --robot.id=so101_cong_left
# 输入 c 重新校准

# 校准主臂
lerobot-calibrate \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM1 \
    --teleop.id=so101_zhu_left
# 输入 c 重新校准
```

### 启动遥操作

```bash
lerobot-teleoperate \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM0 \
    --robot.id=so101_cong_left \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM1 \
    --teleop.id=so101_zhu_left
```

## 注意事项

1. **ttyACM 编号可能变化**：每次插拔 USB 或重启后，ttyACM0/1 的分配可能互换。建议使用前用 `ls /dev/ttyACM*` 确认，或使用 `lerobot-find-port` 识别。

2. **LeRobot 更新覆盖**：如果后续 git pull 更新 LeRobot，feetech.py 可能被还原，需要重新修改默认波特率。建议用 `git stash` 或记录此修改。

3. **权限永久解决**：加入 dialout 组后重启即可，不再需要每次 sudo chmod：
   ```bash
   sudo usermod -aG dialout $USER
   ```

4. **其他 USB 转串口芯片**：如果使用 FTDI 或 CP2102 等芯片，可能支持 1Mbps，无需此修改。此问题仅在使用 CH9101F（1a86:55d3）时出现。

## 修复日期

2026-04-14
