# WSL 에서 Build한 PX4-Autopilot의 컴파일 명령어를 분석하여
# 경로를 Windows에서 사용 가능한 경로로 변환.
# PX4-Autopilot/build/px4_fmu-v6x_default/compile_commands.json 파일

import json
import tkinter as tk
from tkinter import filedialog

def convert_wsl_to_windows(path):
    # WSL 경로를 Windows 경로로 변환
    if path.startswith('/home/'):
        windows_path = '\\\\wsl.localhost\\Ubuntu' + path.replace('/', '\\')
        return windows_path
    return path

def convert_compile_commands():

    root = tk.Tk()
    root.withdraw()  # Hide the root window
    compile_commands_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])

    if not compile_commands_path:
        print("파일 선택이 취소되었습니다.")
        return

    with open(compile_commands_path, 'r') as f:
        data = json.load(f)

    # compile_commands의 각 항목을 변환
    for item in data:
        # `-I` 옵션 경로 변환
        if '-I' in item['command']:
            item['command'] = item['command'].replace('/home/', '\\\\wsl.localhost\\Ubuntu\\home\\')
            item['command'] = item['command'].replace('/', '\\')
        
        item['directory'] = convert_wsl_to_windows(item['directory'])
        item['file'] = convert_wsl_to_windows(item['file'])

    # 변환된 결과를 새로운 파일에 저장
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    save_path = filedialog.asksaveasfilename(defaultextension=".json", initialfile="converted_compile_commands.json", filetypes=[("JSON files", "*.json")])
    
    if save_path:
        with open(save_path, 'w') as f:
            json.dump(data, f, indent=4)
    else:
        print("파일 저장이 취소되었습니다.")

    return save_path

# 파일 경로 예시
# compile_commands_path = r"\\wsl.localhost\Ubuntu\home\jh\PX4-Autopilot/build/px4_fmu-v6x_default/compile_commands.json"
# convert_compile_commands(compile_commands_path)
