# namespace - class - function & val 구조 추출 불가. 
#

import os
import re
import clang.cindex
import json

## clang ==============================================================================================
# Compiler LLVM 라이브러리 위치 경로 설정
clang.cindex.Config.set_library_file("C:/Program Files/LLVM/bin/libclang.dll")
# Function 검출
FUNCTION_DECL = clang.cindex.CursorKind.FUNCTION_DECL
CXX_METHOD = clang.cindex.CursorKind.CXX_METHOD
CONSTRUCTOR = clang.cindex.CursorKind.CONSTRUCTOR
DESTRUCTOR = clang.cindex.CursorKind.DESTRUCTOR
# Variable 검출
VAR_DECL = clang.cindex.CursorKind.VAR_DECL
FIELD_DECL = clang.cindex.CursorKind.FIELD_DECL
# Enum 검출
ENUM_DECL = clang.cindex.CursorKind.ENUM_DECL
# Field 검출
TRANSLATION_UNIT = clang.cindex.CursorKind.TRANSLATION_UNIT
STRUCT_DECL = clang.cindex.CursorKind.STRUCT_DECL
UNION_DECL = clang.cindex.CursorKind.UNION_DECL
CLASS_DECL = clang.cindex.CursorKind.CLASS_DECL
NAMESPACE = clang.cindex.CursorKind.NAMESPACE
# ====================================================================================================

# Step01 : compile_commands.json 파일을 분석하여 컴파일 명령어에서 include 경로 추출
def parse_project(path_source_file, path_compile_commands = None):

    include_flags = []
    print(f"\nParsing compile commands - {os.path.basename(path_source_file)}")
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
        index = clang.cindex.Index.create()
        print(f"🔹 Parsing file - {os.path.basename(path_source_file)}")
        args = ["-x", "c++", "-std=c++11"] + include_flags
        # args = ["-x","c++","-nostdinc++", "-std=gnu++14"] + include_flags
        translation_unit = index.parse(path_source_file, args=args)
                    
    except clang.cindex.TranslationUnitLoadError as e:
        print(f"Error parsing file {os.path.basename(path_source_file)}: {e}")
        return None
    
    return translation_unit.cursor
# ====================================================================================================

# (Field) 부모 이름을 재귀적으로 추적하여 전체 경로를 구성
def extract_full_field(node):
    full_field = ''
    names = []
    while node is not None and node.kind != TRANSLATION_UNIT:
        if node.spelling:
            prefix = ""
            if node.kind == CLASS_DECL:
                prefix = "(class)"
            elif node.kind == STRUCT_DECL:
                prefix = "(struct)"
            elif node.kind == UNION_DECL:
                prefix = "(union)"
            elif node.kind == NAMESPACE:
                prefix = "(namespace)"
            # 익명 구조체 처리 (unnamed... anonymous... 등)
            if node.spelling.startswith("("):
                with open(node.location.file.name, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    start_line = node.extent.start.line - 1
                    end_line = node.extent.end.line - 1
                    struct_code = "".join(lines[start_line:end_line + 1])
                    match = re.search(r'\}\s*(\w+);', struct_code)
                    if match:
                        names.append(prefix + match.group(1))
                    else:
                        names.append(prefix + "<unnamed>")
            else:
                names.append(prefix + node.spelling)
        node = node.semantic_parent
        full_field = "::".join(reversed(names))
    return full_field

# (Inputs) 함수 입력 추출(다중 괄호 안의 내용을 추출)
def extract_arguments(line):
    # 중첩된 괄호를 처리할 수 있도록 쪼개기
    parts = []
    count = 0
    temp = ''
    for char in line:
        if char == '(':
            count += 1
            temp += char
        elif char == ')':
            count -= 1
            temp += char
            if count == 0:
                parts.append(temp[1:-1].strip())  # 첫 번째, 마지막 괄호를 제외
                temp = ''
        elif count > 0:
            temp += char

    return parts if parts else None

# 코드 원본 표기 추출 / type, name, inputs
def extract_contents_details(node, line):
    category, return_type, name, inputs, specifiers, field = "", "", "", "", "", ""

    # 함수 추출 정규식 (함수)
    if node.kind in [FUNCTION_DECL, CXX_METHOD, CONSTRUCTOR, DESTRUCTOR]:
        # 선언과 정의 구분
        if node.is_definition():
            if node.kind == CONSTRUCTOR:
                category = "Constructor (definition)" 
            elif node.kind == DESTRUCTOR:
                category = "Destructor (definition)"
            else:
                category = "Function (definition)"
        else:
            if node.kind == CONSTRUCTOR:
                category = "Constructor"
            elif node.kind == DESTRUCTOR:
                category = "Destructor"
            else:
                category = "Function"

        # 함수명 위치 기준으로 front/back 분리
        name = node.spelling
        add_length_column = 0

        # 함수 반환형을 윗줄에 적는 ㅈ경우 처리
        if node.location.line != node.extent.start.line:
            line_a = line.splitlines()[0]
            add_length_column = len(line_a.strip())+1       # 함수명 이전 문자열

        start_line_col = node.extent.start.column            # 함수 선언의 시작 컬럼 위치 (파일 코드라인 기준)
        start_name_col = node.location.column +add_length_column                # 함수명의 시작 컬럼 위치 (파일 코드라인 기준)
        start_col =  start_name_col - start_line_col         # 함수명의 시작 컬럼 위치 (추출한 line 기준 기준)

        front_line = line[:start_col].strip()                # 함수명 이전 문자열
        back_line = line[start_col:].strip()                 # 함수명 이후 문자열(함수명 포함)

        def remove_func_class_part(line):
            parts = line.split()  # 공백을 기준으로 나누기
            result_parts = []     # 결과를 담을 리스트
            class_part = ""       # 함수 클래스 부분 추출을 위한 변수 (함수 클래스명이 있는 경우)
            for part in parts:
                if not part.endswith("::"):    # 함수명 앞에 클래스가 붙은 경우 제외, ('클래스::')
                    result_parts.append(part)  # 제외하지 않은 부분은 결과 리스트에 추가
                else:
                    class_part = part.strip("::").strip()  # 클래스명 추출
            return " ".join(result_parts), class_part

        modified_front_line, func_class_name = remove_func_class_part(front_line)

        # 함수 return type 추출 / with keyword(extern "C", __EXPORT, ...)
        front_pattern = re.compile(r'''
                                    ^\s*                    # 라인의 시작 및 선택적 공백
                                    (extern\s+"C"\s+)?      # 선택적 "extern C" 선언
                                    (__EXPORT\s+)?          # 선택적 "__EXPORT" 지시어
                                    (.*)?                   # 나머지 부분 (반환형 등)                       
                                    ''', re.VERBOSE)
                                    
        front_match = front_pattern.search(modified_front_line)
        
        if front_match:
            specifiers = f"""{(front_match.group(1) if front_match.group(1) else "")
                        + (front_match.group(2) if front_match.group(2) else "")}"""     
            return_type = front_match.group(3) if front_match.group(3) else ""
            # print(f"🔹 {name} / line : {modified_front_line} / front_match : {front_match} / return_type : {node.result_type.spelling} / {node.type.spelling}")
            if func_class_name:
                field = f"(class){func_class_name}"
        else:
            specifiers = "(No front)"
            return_type = node.result_type.spelling
            name = node.spelling
            print(f"⚠️  ({node.location.line}) {category} not.match front - line: {line} / match: {front_line}")

        back_match = extract_arguments(back_line)

        if back_match:
            inputs = ', '.join(back_match)
        else:
            inputs = ", ".join([f"{arg.type.spelling} {arg.spelling}" for arg in node.get_arguments()])
            print(f"⚠️  ({node.location.line}) {category} not.match back - line: {line} / match: {back_line}")
        
        # if front_match and back_match:
            # print(f"🔹 ({node.location.line}) {category} match - {name}")

    # 변수 추출 (변수, 필드)
    elif node.kind in [VAR_DECL, FIELD_DECL]:

        category = "Variable"
        name = node.spelling

        start_line_col = node.extent.start.column            # 변수 선언의 시작 컬럼 위치 (파일 코드라인 기준)
        start_name_col = node.location.column                # 변수명의 시작 컬럼 위치 (파일 코드라인 기준)
        start_col =  start_name_col - start_line_col         # 변수명의 시작 컬럼 위치 (추출한 line 기준 기준)
        return_type = line[:start_col].strip()
        if not return_type:
            return_type = node.type.spelling
            specifiers = "(Plz Check Return Type)"
            print(f"⚠️  ({node.location.line}) {category} return type not found - line : {line} / return_type : {return_type} ")
        # else:
            # print(f"🔹 ({node.location.line}) {category} match - {name}")        
 
        # 변수 추출시 함수 내부 변수인지 확인 및 field에 함수명 표기
        parent_function = node.semantic_parent
        while parent_function and parent_function.kind not in [FUNCTION_DECL, CXX_METHOD, CONSTRUCTOR, DESTRUCTOR]:
            parent_function = parent_function.semantic_parent

        if parent_function:
            function_name = parent_function.spelling
            field = f"(func){function_name}"

    # 열거형 추출
    elif node.kind == ENUM_DECL:
        category = "Enum"
        return_type = node.enum_type.spelling
        name = node.spelling
        inputs = [child.spelling for child in node.get_children()] # 열거형 상수 추출
        # print(f"🔹 ({node.location.line}) {category} match - {name} / components : {inputs}")

     # code_line, access, attributes, parent_name, category, return_type, name, inputs, specifiers, field
    return category, return_type, name, inputs, specifiers, field

# 함수 예외 처리 (DEFINE_PARAMETERS_CUSTOM_PARENT 전처리 함수일 경우)
def extract_param_exceptions(node, line):
    if node.spelling in ["DEFINE_PARAMETERS_CUSTOM_PARENT", "DEFINE_PARAMETERS"]:
        
        if line:
            param_pattern = re.compile(r'\(Param\w+<px4::params::[^>]+>\)\s+_\w+')
            params = param_pattern.findall(line)
            param_list = []
            for param in params:
                param = param.strip()
                # type
                param_type_match = re.search(r'Param(\w+)', param)
                param_type_match = param_type_match.group(1)
                # px4 param
                param_px4_match = re.search(r'<px4::params::([^>]+)>', param)
                param_px4_match = (param_px4_match.group(1).split('::'))[0]
                # param variable
                param_name_match = re.search(r'>\)\s+(\w+)', param).group(1)
            
                if param_type_match and param_name_match and param_px4_match:
                    param_list.append((param_type_match, param_name_match, param_px4_match))
                else:
                    print(f"⚠️ ({node.location.line}) Warning ( line:{line} ): Parameter '{param}' does not follow naming convention")

            if param_list:
                category = "Param Variable"
                return category, param_list
            for param in param_list:
                print(f'param : {param}')
    return None

# -----------------------------------------------------------------------------------------------

#  Step02 : 코드 추출
def extract_source_code(cursor, file_path):

    print(f"\nStep02. Extracting source code - {os.path.basename(file_path)}")
    # return : (functions, constructors, destructors, variables, enums, param)
    functions, constructors, destructors, variables, enums, param = [], [], [], [], [], []

    field_names = set()  # 필드 이름을 저장하는 집합

    # 파일 내의 모든 함수와 변수를 추출(변수, 함수, 생성자, 소멸자, 열거형)
    def visit_node(node, parent=None):
        # return : (file name, code line, access, attributes, field, category, return type, name, inputs, summary, description)
        # 타겟 파일 내의 노드만 추출
        
        if node.location.file and node.location.file.name == file_path:
            code_line = node.location.line
            parent_name = extract_full_field(parent) if parent else ""
            attributes = []

            # 접근 제어자 추출
            def extract_access_specifier(node):
                    # 접근 제어자 추출
                    with open(file_path, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                        for i in range(node.location.line - 1, -1, -1):
                            line = lines[i].strip()
                            if line.startswith("private:"):
                                access = "private"
                                break
                            elif line.startswith("protected:"):
                                access = "protected"
                                break
                            elif line.startswith("public:"):
                                access = "public"
                                break
                            else:
                                access = node.access_specifier.name.lower()
                    return access
            access = extract_access_specifier(node)
            # 함수 키워드 추출 : virtual, pure virtual, static, const, override, inline
            def extract_contents_keywards(node):
                # Attributes : 함수의 key words 추출(virtual, pure virtual, static, const, override, inline)
                attributes = []
                if node.is_virtual_method():                        
                    if node.is_pure_virtual_method():
                        attributes.append("pure virtual")
                    else:
                        attributes.append("virtual")
                if node.is_static_method():
                    attributes.append("static")
                if node.is_const_method():
                    attributes.append("const")

                # 'override' 키워드 확인
                for child in node.get_children():
                    if child.kind == clang.cindex.CursorKind.CXX_OVERRIDE_ATTR:
                        attributes.append("override")

                # 'inline' 확인 (Token 분석 사용)
                tokens = [t.spelling for t in node.get_tokens()]
                if "inline" in tokens:
                    attributes.append("inline")
                return attributes
           
            # 소스코드 라인 추출
            def extract_source_code_line(node):
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    line = ""
                    start_line = node.extent.start.line - 1     # 현재 노드의 시작 줄 번호 (0-based 인덱스)
                    start_column = node.extent.start.column -1  # 현재 노드의 시작 열 번호 (0-based 인덱스)
                    end_line = node.extent.end.line - 1         # 현재 노드의 끝 줄 번호 (0-based 인덱스)
                    end_column = node.extent.end.column -1      # 현재 노드의 끝 열 번호 (0-based 인덱스)

                    if node.kind in [FUNCTION_DECL, CXX_METHOD, CONSTRUCTOR, DESTRUCTOR, VAR_DECL, FIELD_DECL, ENUM_DECL]:

                        if start_line == end_line:
                            line = lines[start_line][start_column:end_column+1].strip()
                            
                        else:
                            contents_definition = []                # 여러 줄을 추적하기 위한 리스트

                            for i in range(start_line, end_line+1):
                                line = lines[i].strip()
                                contents_definition.append(line)
                            line = '\n'.join(contents_definition).strip()
                            
                        # 라인에서 { 이후 문자 제거
                        line = line.split('{')[0].strip()
                return line
            line = extract_source_code_line(node)

            # 함수 (함수, 생성자, 소멸자)
            if node.kind in [FUNCTION_DECL, CXX_METHOD, CONSTRUCTOR, DESTRUCTOR]:

                attributes = extract_contents_keywards(node)
                
                category, return_type, name, inputs, specifiers, field = extract_contents_details(node, line)
                if specifiers:
                    attributes.append(specifiers)

                # 매크로 함수 처리 (DEFINE_PARAMETERS_CUSTOM_PARENT|DEFINE_PARAMETERS 전처리 함수일 경우)
                exception_result = extract_param_exceptions(node, line)
                if exception_result:
                    category = "Param MACRO"
                    param.append((os.path.basename(file_path), code_line, access, "", parent_name, category, return_type, name, ""))
                    param_category, param_list = exception_result
                    for param_type, param_name, px4_param in param_list:
                        code_line += 1
                        param.append((os.path.basename(file_path), code_line, access, "", parent_name, param_category, param_type, param_name, px4_param))
                    return

                if not parent_name:
                    parent_name = field

                if node.kind == CONSTRUCTOR:
                    constructors.append((os.path.basename(file_path), code_line, access, ", ".join(attributes), parent_name, category, return_type, name, inputs))
                elif node.kind == DESTRUCTOR:
                    destructors.append((os.path.basename(file_path), code_line, access, ", ".join(attributes), parent_name, category, return_type, name, inputs))
                else:
                    functions.append((os.path.basename(file_path), code_line, access, ", ".join(attributes), parent_name, category, return_type, name, inputs))

            # 변수 (변수, 필드, 열거형)
            elif node.kind in [VAR_DECL, FIELD_DECL, ENUM_DECL]:
                category, return_type, name, inputs, specifiers, field = extract_contents_details(node, line)

                if "(unnamed struct at" in return_type:
                    return_type = re.sub(r'\(unnamed struct at [^)]+\)', '', return_type)
                if "(anonymous struct at" in return_type:
                    return_type = re.sub(r'\(anonymous [^)]+\)', '', return_type)

                # 필드 중복 확인, struct 구조일 경우 변수 선언 중복 추출 방지
                if node.kind in [VAR_DECL, FIELD_DECL]:
                    if parent and parent.kind == clang.cindex.CursorKind.STRUCT_DECL:
                        field_key = (parent_name, name)
                        if field_key not in field_names:
                            field_names.add(field_key)
                            variables.append((os.path.basename(file_path), code_line, access, ", ".join(attributes), parent_name, category, return_type, name, ""))
                        # else:
                        #     print(f"⚠️  Warning ({os.path.basename(file_path)} / line:{code_line} ): Duplicate field '{name}' in '{parent_name}'")
                    else:
                        if not parent_name:
                            parent_name = field
                        variables.append((os.path.basename(file_path), code_line, access, ", ".join(attributes), parent_name, category, return_type, name, ""))
                if node.kind == ENUM_DECL:
                    enums.append((os.path.basename(file_path), code_line, access, ", ".join(attributes), parent_name, category, return_type, name, ", ".join(inputs)))

        for child in node.get_children():
            visit_node(child, node)
    visit_node(cursor)
    return functions, constructors, destructors, variables, enums, param
# # -----------------------------------------------------------------------------------------------

# # # ====================================================================================================
# # 소스 파일 경로(테스트 용)
# path_source_file = r"\\wsl.localhost\Ubuntu\home\jh\PX4-Autopilot\src\modules\fw_pos_control\launchdetection\LaunchDetector.cpp"
# path_source_file = r"\\wsl.localhost\Ubuntu\home\jh\PX4-Autopilot\src\modules\mavlink\mavlink_main.cpp"
# path_compile_commands = r'C:\Users\ypelec\Desktop\SW_Dev\code_analysis\converted_compile_commands.json'
# # path_compile_commands = r"\\wsl.localhost\Ubuntu\home\jh\PX4-Autopilot/build/px4_fmu-v6x_default/compile_commands.json"


# # 실행 테스트
# # cursor = parse_cpp_file(path_source_file)
# cursor = parse_project(path_source_file, path_compile_commands)

# # find_methods(cursor)
# functions, constructor, destructor, variables, enums, param = extract_source_code(cursor, path_source_file)

# count_func = 0
# count_var = 0
# count_enum = 0
# count_param = 0

# # # print("\n\nResult ======================================================================================\n")
# for functions in functions:
#     count_func += 1
#     print(f"functions({count_func}) : {functions}")
# # for variables in variables:
# #     count_var += 1
# #     print(f"variables({count_var}) : {variables}")
# # for enums in enums:
# #     count_enum += 1
# #     print(f"enums({count_enum}) : {enums}")
# # for param in param:
# #     count_param += 1
# #     print(f"param({count_param}) : {param}")
    
