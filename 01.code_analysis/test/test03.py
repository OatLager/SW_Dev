#!/usr/bin/env python3
import sys
import os
import re
from clang.cindex import Index, CursorKind, TranslationUnit, Config
Config.set_library_file("C:/Program Files/LLVM/bin/libclang.dll")

def find_function_calls(file_path):
    """
    Find all function calls in a C/C++ source file using clang.
    
    Args:
        file_path: Path to the C/C++ source file
    
    Returns:
        List of tuples containing (caller_function, called_function, line_number, column)
    """
    # Create an index
    index = Index.create()
    
    # Try to find libclang.dll automatically if not already configured
    if not Config.loaded:
        try:
            # 이 경로는 시스템에 따라 달라질 수 있습니다
            clang_paths = [
                "C:/Program Files/LLVM/bin/libclang.dll"
            ]
            
            for path in clang_paths:
                if os.path.exists(path):
                    Config.set_library_file(path)
                    break
        except Exception as e:
            print(f"Warning: Could not set libclang path: {e}")
    
    # Parse the source file
    try:
        # Use -I flag to specify include directories if needed
        tu = index.parse(file_path, args=['-xc++', '-std=c++14'])
    except Exception as e:
        print(f"Error parsing file: {e}")
        return []
    
    if not tu:
        print(f"Failed to parse {file_path}")
        return []
    
    function_calls = []
    all_functions = {}  # Store function declarations/definitions
    
    # First pass: find all function declarations
    def get_function_name(cursor):
        """Get the fully qualified function name"""
        if cursor is None:
            return ""
        
        name = cursor.spelling
        if name == "":
            return ""
        
        parent = cursor.semantic_parent
        if parent and parent.kind != CursorKind.TRANSLATION_UNIT:
            parent_name = get_function_name(parent)
            if parent_name != "":
                return f"{parent_name}::{name}"
        
        return name
    
    def find_all_functions(cursor):
        """Find all function declarations/definitions"""
        if cursor.kind in [CursorKind.FUNCTION_DECL, CursorKind.CXX_METHOD]:
            func_name = get_function_name(cursor)
            start_line = cursor.extent.start.line
            end_line = cursor.extent.end.line
            all_functions[func_name] = (start_line, end_line)
            
        for child in cursor.get_children():
            find_all_functions(child)
    
    # Get all function declarations/definitions first
    find_all_functions(tu.cursor)
    
    # Second pass: find function calls and determine their callers
    def get_parent_function(line):
        """Get the name of the function containing this line"""
        for func_name, (start_line, end_line) in all_functions.items():
            if start_line <= line <= end_line:
                return func_name
        return "Unknown"  # If we can't find a parent function
    
    def find_calls_in_cursor(cursor):
        """Find function calls in the cursor tree"""
        if cursor.kind == CursorKind.CALL_EXPR:
            line = cursor.location.line
            column = cursor.location.column
            called_func = cursor.spelling
            
            # Get the caller function
            caller_func = get_parent_function(line)
            
            # Add to our list of function calls
            if called_func:  # Skip empty function names
                function_calls.append((caller_func, called_func, line, column))
        
        # Also check for member function calls that might be missed
        if cursor.kind == CursorKind.MEMBER_REF_EXPR:
            # Check if this member reference is a method call (has arguments)
            children = list(cursor.get_children())
            if len(children) > 0:
                line = cursor.location.line
                column = cursor.location.column
                called_func = cursor.spelling
                
                # Get the caller function
                caller_func = get_parent_function(line)
                
                if called_func:  # Skip empty function names
                    function_calls.append((caller_func, called_func, line, column))
        
        # Recursively process children
        for child in cursor.get_children():
            find_calls_in_cursor(child)
    
    # Start the function call search
    find_calls_in_cursor(tu.cursor)
    
    # Also use regex to catch function calls that might be missed by clang
    with open(file_path, 'r') as f:
        content = f.read()
    
    # 함수 호출 패턴 정의 (일반 함수 호출 및 멤버 함수 호출 포함)
    pattern = r'(\w+(?:::\w+)*)\s*\('
    regex_calls = re.finditer(pattern, content)
    
    for match in regex_calls:
        func_name = match.group(1)
        if func_name not in ['if', 'for', 'while', 'switch', 'return', 'sizeof']:  # 키워드 제외
            line_num = content[:match.start()].count('\n') + 1
            col_num = match.start() - content[:match.start()].rfind('\n')
            
            # Get the parent function
            caller_func = get_parent_function(line_num)
            
            # Check if this call is already in our list
            is_duplicate = False
            for caller, called, line, col in function_calls:
                if called == func_name and abs(line - line_num) < 2:  # 근접한 위치에 있는 경우
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                function_calls.append((caller_func, func_name, line_num, col_num))
    
    # 멤버 함수 호출 패턴 (obj.method() 형태)
    pattern2 = r'(\w+)\.(\w+)\s*\('
    regex_calls2 = re.finditer(pattern2, content)
    
    for match in regex_calls2:
        obj_name = match.group(1)
        method_name = match.group(2)
        func_name = f"{obj_name}.{method_name}"
        
        line_num = content[:match.start()].count('\n') + 1
        col_num = match.start() - content[:match.start()].rfind('\n')
        
        # Get the parent function
        caller_func = get_parent_function(line_num)
        
        # Check if this call is already in our list
        is_duplicate = False
        for caller, called, line, col in function_calls:
            if (called == method_name or called == func_name) and abs(line - line_num) < 2:
                is_duplicate = True
                break
        
        if not is_duplicate:
            function_calls.append((caller_func, func_name, line_num, col_num))
    
    # 멤버 함수 호출 패턴 (obj->method() 형태)
    pattern3 = r'(\w+)->(\w+)\s*\('
    regex_calls3 = re.finditer(pattern3, content)
    
    for match in regex_calls3:
        obj_name = match.group(1)
        method_name = match.group(2)
        func_name = f"{obj_name}->{method_name}"
        
        line_num = content[:match.start()].count('\n') + 1
        col_num = match.start() - content[:match.start()].rfind('\n')
        
        # Get the parent function
        caller_func = get_parent_function(line_num)
        
        # Check if this call is already in our list
        is_duplicate = False
        for caller, called, line, col in function_calls:
            if (called == method_name or called == func_name) and abs(line - line_num) < 2:
                is_duplicate = True
                break
        
        if not is_duplicate:
            function_calls.append((caller_func, func_name, line_num, col_num))
    
    return function_calls

def main():
    # 분석할 파일 경로를 직접 지정합니다
    file_path = "C:\\Users\\ypelec\\Desktop\\SW_Dev\\code_analysis\\test\\sample_code.cpp"
    
    # 샘플 코드 생성
    with open(file_path, 'w') as f:
        f.write("""
FailsafeBase::Action Failsafe::checkModeFallback(const failsafe_flags_s &status_flags, 		uint8_t user_intended_mode) const { 	Action action = Action::None;  	// offboard signal 	if (status_flags.offboard_control_signal_lost && (status_flags.mode_req_offboard_signal & (1u << user_intended_mode))) { 		action = fromOffboardLossActParam(_param_com_obl_rc_act.get(), user_intended_mode);  		// for this specific case, user_intended_mode is not modified, we shouldn't check additional fallbacks 		if (action == Action::Disarm) { 			return action; 		} 	}  	// posctrl 	switch (position_control_navigation_loss_response(_param_com_posctl_navl.get())) { 	case position_control_navigation_loss_response::Altitude_Manual: // AltCtrl/Manual  		// PosCtrl -> AltCtrl 		if (user_intended_mode == vehicle_status_s::NAVIGATION_STATE_POSCTL 		    && !modeCanRun(status_flags, user_intended_mode)) { 			action = Action::FallbackAltCtrl; 			user_intended_mode = vehicle_status_s::NAVIGATION_STATE_ALTCTL; 		}  		// AltCtrl -> Stabilized 		if (user_intended_mode == vehicle_status_s::NAVIGATION_STATE_ALTCTL 		    && !modeCanRun(status_flags, user_intended_mode)) { 			action = Action::FallbackStab; 			user_intended_mode = vehicle_status_s::NAVIGATION_STATE_STAB; 		}  		break;  	case position_control_navigation_loss_response::Land_Descend: // Land/Terminate  		// PosCtrl -> Land 		if (user_intended_mode == vehicle_status_s::NAVIGATION_STATE_POSCTL 		    && !modeCanRun(status_flags, user_intended_mode)) { 			action = Action::Land; 			user_intended_mode = vehicle_status_s::NAVIGATION_STATE_AUTO_LAND;  			// Land -> Descend 			if (!modeCanRun(status_flags, user_intended_mode)) { 				action = Action::Descend; 				user_intended_mode = vehicle_status_s::NAVIGATION_STATE_DESCEND; 			} 		}  		break; 	}   	// Last, check can_run for intended mode 	if (!modeCanRun(status_flags, user_intended_mode)) { 		action = Action::RTL; 		user_intended_mode = vehicle_status_s::NAVIGATION_STATE_AUTO_RTL; 	}  	return action; }
        """)
    
    function_calls = find_function_calls(file_path)
    
    if not function_calls:
        print("No function calls found or could not parse the file.")
        return
    
    print(f"Found {len(function_calls)} function calls:")
    print("=" * 90)
    print(f"{'CALLER':<45} | {'CALLED':<35} | {'LINE:COL':<10}")
    print("-" * 90)
    
    # Sort by line number
    function_calls.sort(key=lambda x: (x[2], x[3]))
    
    # Remove duplicates
    unique_calls = []
    for call in function_calls:
        if call not in unique_calls:
            unique_calls.append(call)
    
    for caller, called, line, col in unique_calls:
        # Skip some common operators that might be detected as functions
        if called in ["operator==", "operator!=", "operator<", "operator>", "operator<=", "operator>=", "operator&"]:
            continue
        print(f"{caller:<45} | {called:<35} | {line}:{col}")
    
    # 시각화된 정보로 함수 호출 관계 출력
    print("\n함수 호출 관계 요약:")
    print("=" * 80)
    
    # 호출자별로 그룹화
    caller_groups = {}
    for caller, called, line, col in unique_calls:
        if caller not in caller_groups:
            caller_groups[caller] = []
        if called not in ["operator==", "operator!=", "operator<", "operator>", "operator<=", "operator>=", "operator&"]:
            caller_groups[caller].append(called)
    
    for caller, called_funcs in caller_groups.items():
        # 중복 제거
        called_funcs = list(set(called_funcs))
        print(f"{caller} 함수는 다음 함수들을 호출합니다:")
        for func in called_funcs:
            print(f"  └─ {func}")
        print()

if __name__ == "__main__":
    main()
