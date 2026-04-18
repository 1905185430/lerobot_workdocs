---
title: SO-101 波特率兼容性问题
created: 2026-04-18
updated: 2026-04-18
type: entity
tags: [pitfall, robot-arm, calibration]
sources: [raw/articles/so101-baudrate-fix-2026.md]
---

# SO-101 波特率兼容性问题

## 问题现象

使用 `lerobot-teleoperate` 遥操作时，从臂报错：
```
ConnectionError: Failed to sync read 'Present_Position' on ids=[1,2,3,4,5,6] after 1 tries.
[TxRxResult] There is no status packet!
```

校准可通过，但遥操作时无法读取舵机位置。

## 根因分析

1. LeRobot 在 `feetech.py` 中硬编码默认波特率为 1,000,000 bps
2. SO-101 的 USB 转串口芯片 CH9101F（1a86:55d3）在 ACM 模式下对 1Mbps 支持不稳定
3. 所有舵机在 1Mbps 下返回 "no status packet"
4. 逐波特率测试：9600-500000 全部 OK，唯独 1000000 FAILED

## 解决方案

修改 `~/lerobot/src/lerobot/motors/feetech/feetech.py`：
```python
# 原：DEFAULT_BAUDRATE = 1_000_000
DEFAULT_BAUDRATE = 500_000
```

修改后需重新校准（旧校准文件不再适用）。

## 注意事项

- **ttyACM 编号可能变化**：每次插拔或重启后端口可能互换
- **LeRobot 更新覆盖**：git pull 可能还原修改，建议 git stash 或记录
- **权限永久方案**：`sudo usermod -aG dialout $USER`，重启后不再需要 chmod
- **其他芯片**：FTDI/CP2102 可能支持 1Mbps，此问题仅在使用 CH9101F 时出现

## 修复日期

2026-04-14

## 相关概念

- [[so101|SO-101]] — 出问题的机械臂
- [[lerobot|LeRobot]] — 需要修改默认波特率的框架
