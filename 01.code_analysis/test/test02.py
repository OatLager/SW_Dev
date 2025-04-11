import clang.cindex
import os

# Clang 라이브러리 경로 설정 (필요한 경우)
clang.cindex.Config.set_library_file("C:/Program Files/LLVM/bin/libclang.dll")

# 분석할 파일 경로
file_path = r"\\wsl.localhost\Ubuntu\home\jh\PX4-Autopilot\src\modules\commander\failsafe\failsafe.cpp"

# Clang 파싱 인자 설정 (필요에 따라 수정 가능)
clang_args = [
    '-x', 'c++',
    '-std=c++17',
    '-D__PX4_NUTTX',
    '-I' + os.path.dirname(file_path),  # 현재 파일 위치
    '-I\\wsl.localhost\\Ubuntu\\home\\jh\\PX4-Autopilot',
    '-I\\wsl.localhost\\Ubuntu\\home\\jh\\PX4-Autopilot\\src',
    '-I\\wsl.localhost\\Ubuntu\\home\\jh\\PX4-Autopilot\\platforms\\common\\include'
]

def print_ast(cursor, depth=0, parent_fn=None, file_path=None):
    kind = cursor.kind
    name = cursor.displayname
    file = cursor.location.file

    # 내가 작성한 소스인지 확인 (None이면 무시, source_root로 시작하지 않으면 무시)
    if file is None or (file_path and not str(file).startswith(file_path)):

        # 함수 정의일 경우
        if kind in [clang.cindex.CursorKind.CXX_METHOD, clang.cindex.CursorKind.FUNCTION_DECL]:
            if cursor.is_definition():
                parent_fn = name
                print(f"\n[함수 정의] {name} ({cursor.location.file}:{cursor.location.line})")

        # 함수 호출일 경우
        if kind == clang.cindex.CursorKind.CALL_EXPR and parent_fn:
            print(f"  └─ [함수 호출] {name} → 호출자: {parent_fn} ({cursor.location.line})")

            # 이 CALL_EXPR 내부에 MEMBER_REF_EXPR이 있는지 확인 (멤버 함수 호출인 경우)
            for child in cursor.get_children():
                if child.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR:
                    print(f"     └─ [멤버 함수 호출] {child.displayname} ({child.location.file}:{child.location.line})")

        # 재귀적으로 하위 노드 탐색
        for child in cursor.get_children():
            print_ast(child, depth + 1, parent_fn, file_path)


# AST 파싱 및 출력
index = clang.cindex.Index.create()
translation_unit = index.parse(file_path, args=clang_args)

print("==== AST 구조 출력 ====")
print_ast(translation_unit.cursor, 0, None, file_path)
