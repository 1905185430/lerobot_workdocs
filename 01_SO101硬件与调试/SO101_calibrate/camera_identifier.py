#!/usr/bin/env python3
"""
SO-101 相机识别工具 - Modern UI
依赖：PySimpleGUI, opencv-python
安装：pip install PySimpleGUI opencv-python
"""

import cv2
import json
import time
import threading
from pathlib import Path
import PySimpleGUI as sg

# ========== 配置 ==========
CAMERA_NAMES_FILE  = Path(__file__).parent / "camera_names.txt"
MAPPING_JSON_FILE = Path(__file__).parent / "camera_mapping.json"
MAPPING_MD_FILE   = Path(__file__).parent / "camera_mapping.md"
UDEV_RULES_FILE    = Path(__file__).parent / "99-so101-cameras.rules"
PHOTO_DIR         = Path(__file__).parent / "camera_photos"
PHOTO_DIR.mkdir(exist_ok=True)

sg.theme('DarkPurple7')
sg.set_options(
    font=('Cascadia Code', 10),
    border_width=0,
    element_padding=(6, 4),
    button_color=('#1E1E2E', '#7C3AED'),
)


def load_camera_names():
    defaults = ['laptop_webcam', 'so101_left_top', 'so101_right_top',
                'so101_left_wrist', 'so101_right_wrist']
    if not CAMERA_NAMES_FILE.exists():
        return defaults
    names = []
    with open(CAMERA_NAMES_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                names.append(line)
    return names if names else defaults


def get_camera_info(index):
    import subprocess
    try:
        result = subprocess.run(
            ['udevadm', 'info', '-q', 'property',
             '-p', f'/sys/class/video4linux/video{index}'],
            capture_output=True, text=True, timeout=5
        )
        props = {}
        for line in result.stdout.strip().split('\n'):
            if '=' in line:
                k, v = line.split('=', 1)
                props[k] = v
        return {
            'id_path':     props.get('ID_PATH', 'unknown'),
            'id_serial':   props.get('ID_SERIAL_SHORT',
                                     props.get('ID_SERIAL', 'unknown')),
            'id_path_tag': props.get('ID_PATH_TAG', 'unknown'),
        }
    except:
        return {'id_path': 'unknown',
                'id_serial': 'unknown', 'id_path_tag': 'unknown'}


def detect_cameras(max_check=10):
    cameras = []
    for i in range(max_check):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                info = get_camera_info(i)
                cameras.append({
                    'index': i,
                    'info':  info,
                    'width':  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                })
            cap.release()
    return cameras


class PreviewThread(threading.Thread):
    def __init__(self, index, frame_holder):
        super().__init__(daemon=True)
        self.index = index
        self.frame_holder = frame_holder
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(self.index)
        while self.running:
            ret, frame = cap.read()
            if ret:
                self.frame_holder[0] = frame
        cap.release()


def main():
    camera_names = load_camera_names()
    cameras = detect_cameras()

    if not cameras:
        sg.popup_error(
            '未检测到任何相机！\n\n请检查相机连接后重试。',
            title='错误', modal=True
        )
        return

    # ---- 顶部标题栏 ----
    header = [
        [sg.Text('SO-101 相机识别工具',
                 font=('Cascadia Code', 18, 'bold'), text_color='#A78BFA'),
         sg.Push(),
         sg.Text(f'检测到 {len(cameras)} 个设备',
                 font=('Cascadia Code', 10), text_color='#94A3B8'),
        ],
        [sg.Text('点击设备开始预览，再分配名称，最后保存配置',
                 font=('Cascadia Code', 9), text_color='#64748B')],
        [sg.HorizontalSeparator(color='#7C3AED')],
    ]

    # ---- 左侧：设备列表 ----
    device_section = [
        [sg.Text('设备列表',
                 font=('Cascadia Code', 11, 'bold'), text_color='#E2E8F0')],
    ]
    for cam in cameras:
        port = cam['info']['id_path'].split('-')[-1] if cam['info']['id_path'] != 'unknown' else '?'
        device_section.append([
            sg.Radio(
                f'  video{cam["index"]}   ->   usb-{port}',
                group_id='camera_sel',
                key=f'cam_{cam["index"]}',
                enable_events=True,
                default=(cam['index'] == cameras[0]['index']),
                size=(32, 1),
                background_color='#1E1E2E',
                text_color='#CBD5E1',
            )
        ])

    # ---- 已分配映射 ----
    assign_section = [
        [sg.Text('名称分配',
                 font=('Cascadia Code', 11, 'bold'), text_color='#E2E8F0',
                 pad=(0, (16, 4)))],
    ]
    for cam in cameras:
        assign_section.append([
            sg.Text(f'video{cam["index"]}',
                   size=(10, 1), text_color='#94A3B8'),
            sg.Input(key=f'name_{cam["index"]}', size=(22, 1),
                    background_color='#0F0F1A',
                    text_color='#E2E8F0',
                    border_width=1)
        ])

    # ---- 预设快捷按钮 ----
    preset_section = [
        [sg.Text('预设名称',
                 font=('Cascadia Code', 11, 'bold'), text_color='#E2E8F0',
                 pad=(0, (16, 4)))],
    ]
    for i, name in enumerate(camera_names):
        preset_section.append([
            sg.Button(f'{name}', key=f'preset_{i}',
                     size=(20, 1.6),
                     button_color=('#7C3AED', '#2D1B69'),
                     font=('Cascadia Code', 9))
        ])

    # ---- 操作按钮 ----
    action_section = [
        [sg.HorizontalSeparator(color='#7C3AED', pad=(0, (16, 8)))],
        [
            sg.Button('保存配置', key='save',
                     size=(18, 1.8),
                     button_color=('#10B981', '#064E3B'),
                     font=('Cascadia Code', 10, 'bold')),
            sg.Button('退出', key='exit',
                     size=(12, 1.8),
                     button_color=('#6B7280', '#1F2937'),
                     font=('Cascadia Code', 10)),
        ],
    ]

    left_panel = header + device_section + assign_section + preset_section + action_section

    # ---- 右侧预览区 ----
    right_panel = [
        [sg.Text('实时预览',
                 font=('Cascadia Code', 13, 'bold'), text_color='#A78BFA',
                 justification='center', size=(30, 1), pad=(0, (0, 8)))],

        [sg.Frame('', [
            [sg.Image(key='preview', filename='', size=(640, 480),
                      background_color='#0A0A0F')]
        ], background_color='#0A0A0F', border_width=0)],

        [sg.Frame('', [
            [sg.Text(key='cam_info',
                     text_color='#94A3B8',
                     font=('Cascadia Code', 9),
                     size=(70, 4))]
        ], background_color='#1A1A2E', border_width=0, pad=(0, (8, 0)))],
    ]

    # ---- 主布局 ----
    layout = [
        [
            sg.Column(left_panel, size=(340, 750),
                     background_color='#1E1E2E',
                     scrollable=True,
                     vertical_scroll_only=True,
                     pad=(0, 0)),
            sg.VSep(color='#7C3AED'),
            sg.Column(right_panel, size=(720, 750),
                     background_color='#11111B',
                     element_justification='center'),
        ]
    ]

    window = sg.Window(
        'SO-101 相机识别工具',
        layout,
        finalize=True,
        resizable=True,
        size=(1120, 780),
        background_color='#1E1E2E',
    )

    # ---- 状态 ----
    current_idx = cameras[0]['index']
    frame_holder = [None]
    preview_thread = None

    def start_preview(idx):
        nonlocal preview_thread
        if preview_thread:
            preview_thread.running = False
            preview_thread.join(timeout=1)
        frame_holder[0] = None
        preview_thread = PreviewThread(idx, frame_holder)
        preview_thread.start()
        for cam in cameras:
            if cam['index'] == idx:
                info = cam['info']
                port = info['id_path'].split('-')[-1] if info['id_path'] != 'unknown' else '?'
                window['cam_info'].update(
                    f'video{idx}  |  {cam["width"]}x{cam["height"]}  |  '
                    f'usb-{port}\nID_PATH:  {info["id_path"]}\n'
                    f'SERIAL:   {info["id_serial"]}'
                )
                break

    start_preview(current_idx)

    # ---- 事件循环 ----
    while True:
        event, values = window.read(timeout=80)

        if event in (sg.WIN_CLOSED, 'exit'):
            break

        if event.startswith('cam_'):
            new_idx = int(event.split('_')[1])
            if new_idx != current_idx:
                current_idx = new_idx
                start_preview(new_idx)

        if event.startswith('preset_'):
            i = int(event.split('_')[1])
            chosen = camera_names[i]
            window[f'name_{current_idx}'].update(chosen)

        if event == 'save':
            assignments = {}
            for cam in cameras:
                idx = cam['index']
                name = values.get(f'name_{idx}', '').strip()
                if not name:
                    name = f'camera_{idx}'
                info = cam['info']
                assignments[name] = {
                    'video_index': idx,
                    'id_path':     info['id_path'],
                    'id_serial':   info['id_serial'],
                    'id_path_tag': info['id_path_tag'],
                }

            with open(MAPPING_JSON_FILE, 'w') as f:
                json.dump(assignments, f, indent=2)

            md_lines = [
                "# SO-101 相机映射表", "",
                f"> 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}", "",
                "| 名称 | video 设备 | 分辨率 | ID_PATH |",
                "|---|---|---|---|",
            ]
            for name, info in assignments.items():
                for cam in cameras:
                    if cam['index'] == info['video_index']:
                        md_lines.append(
                            f"| {name} | /dev/video{info['video_index']} "
                            f"| {cam['width']}x{cam['height']} | "
                            f"{info['id_path']} |"
                        )
                        break
            md_lines.extend([
                "", "## udev 规则安装", "",
                "```bash",
                f"sudo cp {UDEV_RULES_FILE} /etc/udev/rules.d/",
                "sudo udevadm control --reload-rules && sudo udevadm trigger",
                "```",
            ])
            with open(MAPPING_MD_FILE, 'w') as f:
                f.write('\n'.join(md_lines))

            udev_rules = [
                "# SO-101 相机 udev 固定设备名规则",
                f"# 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}", ""
            ]
            for name, info in assignments.items():
                tag = info.get('id_path_tag', '')
                if tag and tag != 'unknown':
                    udev_rules.append(
                        f'SUBSYSTEM=="video4linux", '
                        f'ENV{{ID_PATH_TAG}}=="{tag}", SYMLINK+="{name}"'
                    )
            with open(UDEV_RULES_FILE, 'w') as f:
                f.write('\n'.join(udev_rules))

            sg.popup_ok(
                f'保存成功！\n\n'
                f'camera_mapping.json\n'
                f'camera_mapping.md\n'
                f'99-so101-cameras.rules\n\n'
                f'安装 udev 规则：\n'
                f'sudo cp {UDEV_RULES_FILE} /etc/udev/rules.d/\n'
                'sudo udevadm control --reload-rules && sudo udevadm trigger',
                title='保存成功', modal=True, keep_on_top=True,
            )

        frame = frame_holder[0]
        if frame is not None:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imgbytes = cv2.imencode('.png', frame_rgb)[1].tobytes()
            window['preview'].update(data=imgbytes)

    if preview_thread:
        preview_thread.running = False
        preview_thread.join(timeout=1)
    window.close()


if __name__ == '__main__':
    main()
