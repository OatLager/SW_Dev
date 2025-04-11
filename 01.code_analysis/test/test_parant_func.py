import os
import tkinter as tk
from tkinter import filedialog
from clang.cindex import Index, CursorKind, Config

# ✅ Clang DLL 경로 설정 (Windows 기준)
Config.set_library_file("C:/Program Files/LLVM/bin/libclang.dll")

# 지원하는 파일 확장자
VALID_EXTENSIONS = {'.c', '.cpp', '.h', '.hpp'}

def choose_folder(title):
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title=title)

def get_parent_name(cursor):
    """함수의 부모 네임스페이스, 클래스 등을 추출"""
    names = []
    cur = cursor.semantic_parent
    while cur and cur.kind != CursorKind.TRANSLATION_UNIT:
        if cur.spelling:
            names.insert(0, cur.spelling)
        cur = cur.semantic_parent
    return '::'.join(names)

def get_functions_from_file(file_path):
    index = Index.create()
    args = ["-x", "c++", "-std=c++11"]
    tu = index.parse(file_path, args=args)

    functions = []
    for node in tu.cursor.walk_preorder():
        if node.kind in [CursorKind.FUNCTION_DECL, CursorKind.CXX_METHOD]:
            if node.is_definition() and node.location.file and node.location.file.name == file_path:
                parent_name = get_parent_name(node)
                # 부모가 없다면 함수명만 반환
                func_name = f"{parent_name + '::' if parent_name else ''}{node.spelling}"
                line = node.location.line
                functions.append((func_name, line, os.path.basename(file_path)))
    return functions

def collect_functions_from_folder(folder_path):
    all_functions = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(tuple(VALID_EXTENSIONS)):  # 확장자 확인
                file_path = os.path.join(root, file)
                functions = get_functions_from_file(file_path)
                if functions:
                    all_functions[file] = functions
                else:
                    all_functions[file] = "정의된 함수 없음"
    return all_functions

# 🔍 분석할 폴더 선택
analyze_folder = choose_folder("분석할 폴더를 선택하세요")
result = collect_functions_from_folder(analyze_folder)

# ✅ 결과 확인 출력
for file, functions in result.items():
    print(f"\n📄 {file}")
    if functions == "정의된 함수 없음":
        print("정의된 함수 없음")
    else:
        for idx, (func, line, fname) in enumerate(functions, 1):
            print(f"{idx}. {func} (line {line})")
