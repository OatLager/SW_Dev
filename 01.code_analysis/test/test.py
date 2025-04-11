import os
import csv
import tkinter as tk
from tkinter import filedialog
from clang import cindex
from collections import defaultdict
import sys
import json

# Clang 라이브러리 설정
cindex.Config.set_library_file("C:/Program Files/LLVM/bin/libclang.dll")

# 경로 설정
DEFAULT_PROJECT_PATH = r'\\wsl.localhost\Ubuntu\home\jh\PX4-Autopilot\src\modules\commander'
DEFAULT_ANALYSIS_PATH = r'\\wsl.localhost\Ubuntu\home\jh\PX4-Autopilot\src\modules\commander\failsafe'
compile_commands_path = r"C:\Users\ypelec\Desktop\ing\방산100_FCS SW(박지훈)\작업 중\Code_v09\converted_compile_commands.json"
SAVE_DIR = r"C:\Users\ypelec\Desktop"

# 필터할 확장자
EXTENSIONS = ['.c', '.cpp', '.h', '.hpp']

FUNCTION_KINDS = {
    cindex.CursorKind.FUNCTION_DECL,
    cindex.CursorKind.CXX_METHOD,
    cindex.CursorKind.CONSTRUCTOR,
    cindex.CursorKind.DESTRUCTOR,
    cindex.CursorKind.FUNCTION_TEMPLATE
}


# UI로 폴더 선택
def select_folder(title, default_path):
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title=title, initialdir=default_path)
    return folder

def parse_project(path_source_file, path_compile_commands = None):
    path_source_file = os.path.normpath(path_source_file).replace('\\', '\\\\')

    include_flags = []
    print(f"\n Compile commands Parsing - {os.path.basename(path_source_file)}")
    print(f"🔹 Source file path : {path_source_file}")
    # (옵션) compile commands json 파일 확인---------------------------------------------
    if path_compile_commands:
        print(f"🔹 Found compile commands file - {os.path.basename(path_compile_commands)}")
        # 컴파일 명령어 파일 읽기
        with open(path_compile_commands, 'r') as f:
            
            compile_commands = json.load(f)
            for command in compile_commands:
                if command.get('file') == path_source_file:
                    include_flags = [arg for arg in command['command'].split() if arg.startswith('-I') or arg.startswith('-isystem ') ] # or arg.startswith('-D') or arg.startswith('-iquote')
                    print(f"🔹 Found compile commands - {os.path.basename(path_source_file)}")
                    break

        # include 경로 출력
        for flag in include_flags:
            print(f'        : {flag}')
            if not include_flags:
                print(f"🔹 No Compile commands found")
    else:
        print(f"🔹 No compile commands file found")
    # ----------------------------------------------------------------------------------
    try:
        print(f"🔹 compile commands - {os.path.basename(path_source_file)}")
        args = ["-x", "c++", "-std=c++11"] + include_flags
        # args = ["-x","c++","-nostdinc++", "-std=gnu++14"] + include_flags
                    
    except cindex.TranslationUnitLoadError as e:
        print(f"Error parsing file {os.path.basename(path_source_file)}: {e}")
        return None
    
    return args



# 파일 내 모든 함수 정의 수집
def collect_function_definitions(index, file_path, project_path):
    # args = parse_project(file_path, compile_commands_path)
    args = ["-x", "c++", "-std=c++11"]
    tu = index.parse(file_path, args=args)
    functions = []

    def visit(node, parent=None):
        if node.kind in FUNCTION_KINDS and node.is_definition():
            if node.location.file and node.location.file.name == file_path:
                func_name = node.spelling
                # print(f'spelling : {node.spelling}, display : {node.displayname}')
                func_parent = parent.spelling if parent and parent.kind == cindex.CursorKind.CLASS_DECL else ''
                line = node.location.line
                try:
                    rel_path = os.path.relpath(file_path, project_path)
                except ValueError:
                    rel_path = file_path
                functions.append({
                    'parent': func_parent,
                    'name': func_name,
                    'line': line,
                    'file': rel_path
                })
        for child in node.get_children():
            visit(child, node)

    visit(tu.cursor)
    return functions

def is_valid_parent_kind(kind):
    return kind in {
        cindex.CursorKind.CLASS_DECL,
        cindex.CursorKind.STRUCT_DECL,
        cindex.CursorKind.CLASS_TEMPLATE,
        cindex.CursorKind.NAMESPACE
    }

# 파일 내 모든 함수 호출 수집
def collect_function_calls(index, file_path, project_path):
    # args = parse_project(file_path, compile_commands_path)
    args = ["-x", "c++", "-std=c++11"]
    tu = index.parse(file_path, args=args)
    results = []

    def visit(node, current_function=None, current_function_parent=None):
        if node.kind in (cindex.CursorKind.FUNCTION_DECL, cindex.CursorKind.CXX_METHOD):
            current_function = node.spelling
            current_function_parent = node.semantic_parent.spelling if node.semantic_parent and is_valid_parent_kind(node.semantic_parent.kind) else None
        if node.kind == cindex.CursorKind.CALL_EXPR:
            if node.location and node.location.file and not node.location.is_in_system_header:
                referenced = node.referenced
                if referenced:
                    ref_name = referenced.spelling
                    ref_parent_cursor = referenced.semantic_parent
                    ref_parent = ref_parent_cursor.spelling if ref_parent_cursor and is_valid_parent_kind(ref_parent_cursor.kind) else ''
                else:
                    # fallback 처리: referenced 정보가 없을 때
                    ref_name = node.spelling
                    ref_parent = ''
                
                try:
                    rel_path = os.path.relpath(node.location.file.name, project_path)
                except ValueError:
                    rel_path = node.location.file.name    
                
                results.append({
                    'current_file' : os.path.basename(file_path),
                    'caller_parent' : current_function_parent,
                    'caller': current_function,
                    'called_parent' : ref_parent,
                    'called': ref_name,
                    'file': rel_path,
                    'line': node.location.line,
                    'caller_line': node.semantic_parent.location.line if node.semantic_parent and node.semantic_parent.location else None,
                })
        for child in node.get_children():
            visit(child, current_function, current_function_parent)

    visit(tu.cursor)
    return results


# 경로 표시 변환
def normalize_path(path):
    return os.path.normpath(path).replace('\\', '/')

# 메인 분석 로직
def analyze_functions(project_path, target_path):
    index = cindex.Index.create()
    defined_funcs = []
    calls = []

    # 대상 파일 수집
    target_files = []
    for root, _, files in os.walk(target_path):
        for file in files:
            if os.path.splitext(file)[1] in EXTENSIONS:
                target_files.append(os.path.join(root, file))

    target_files = [normalize_path(f) for f in target_files]

    # 함수 정의 수집
    for file in target_files:
        defined_funcs.extend(collect_function_definitions(index, file, project_path))
    # 분석폴더 내 함수정의 부분
    for defined_func_idx, defined_func in enumerate(defined_funcs, 1):
        print(f'{defined_func_idx:3d}. 함수정의 : {defined_func}')

    print('='*50)
    # 호출 정보 수집 (전체 프로젝트 범위)
    project_files = []
    for root, _, files in os.walk(project_path):
        for file in files:
            if os.path.splitext(file)[1] in EXTENSIONS:
                project_files.append(os.path.join(root, file))

    for file in project_files:
        calls.extend(collect_function_calls(index, file, project_path))

    # 프로젝트 내 함수호출 부분
    for call_idx, call in enumerate(calls, 1):
        print(f'{call_idx:3d}. 함수호출 : {call}')

    print('정의함수 호출자'+'='*50)

    # 호출자 매핑 (함수명 + 파일 경로 기준)
    results = []
    fun_idx = 0
    for func in defined_funcs:
        matched = False  # 해당 함수에 대해 호출 매칭 여부
        called_idx = 0
        fun_idx = fun_idx+1
        function = f"{func['parent']}::{func['name']}" if func['parent'] else func['name']
        print(f"{fun_idx}. {os.path.basename(func['file'])}:{func['line']} - {function}")
        for call in calls:
            if call['called'] == func['name']:  # 필요 시 파일명도 비교할 수 있음
                caller = f"{call['caller_parent']}::{call['caller']}" if call['caller_parent'] else call['caller']
                called = f"{call['called_parent']}::{call['called']}" if call['called_parent'] else call['called']
                matched = True
                called_idx = called_idx+1
                print(f"    ({called_idx}).호출자 - {caller} / 호출된함수:{call['line']} - {called}")
                results.append({
                    'filename': os.path.basename(func['file']),
                    'line': func['line'],
                    'function': function,
                    'caller': caller,
                    'caller_line': call['caller_line'],
                    'caller_file': call['file'],
                })

        if not matched:
            # print(f"not matching : 호출자 - 없음 / 호출된함수 - 없음 / 정의함수 - {func['name']}")
            results.append({
                'filename': os.path.basename(func['file']),
                'line': func['line'],
                'function': function,
                'caller': '-',
                'caller_line': '-',
                'caller_file': '-',
            })

    return results

# 결과 저장 (CSV로)
def save_results_to_csv(results, folder_name):
    save_path = os.path.join(SAVE_DIR, f"{folder_name}.csv")
    with open(save_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['filename', 'line', 'function', 'call', 'call line', 'call file'])
        for row in results:
            writer.writerow([
                row['filename'], row['line'], row['function'],
                row['caller'], row['caller_line'], row['caller_file']
            ])
    print(f"저장 완료: {save_path}")

def main():
    # 로그 파일 열기
    with open('log_output.txt', 'w', encoding='utf-8') as f:
        # 표준 출력을 파일로 변경
        sys.stdout = f
        sys.stderr = f  # 에러도 저장하고 싶으면 추가

        project_path = select_folder("프로젝트 폴더를 선택하세요", DEFAULT_PROJECT_PATH)
        target_path = select_folder("분석할 폴더를 선택하세요", DEFAULT_ANALYSIS_PATH)
        folder_name = os.path.basename(target_path)

        results = analyze_functions(project_path, target_path)
        save_results_to_csv(results, folder_name)

        # 출력 복원 (원하면)
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

if __name__ == "__main__":
    main()
