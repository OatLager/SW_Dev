import tkinter as tk
from tkinter import filedialog
from customtkinter import *
import os
import SDK_config 
from Protocol_Generator.MAVLink import mav_gen 

# Args 클래스 정의
class Args:
    def __init__(self, output, language, wire_protocol, max_include_file, definitions, exit_code=True):  # exit_code 항상 True
        self.output = output
        self.language = language
        self.wire_protocol = wire_protocol
        self.max_include_file = max_include_file
        self.definitions = definitions
        self.exit_code = exit_code

# 현재 실행 파일의 위치를 가져옴
current_directory = os.path.dirname(os.path.abspath(__file__))

# XML 파일을 선택할 때 호출될 함수
def add_xml_file():
    filename = filedialog.askopenfilename(
        initialdir=current_directory,
        filetypes=[("XML Files", "*.xml")])
    if filename:
        input_dir.set(filename)  # 선택된 파일을 input_dir에 저장

# 출력 디렉토리를 선택할 때 호출될 함수
def select_output_directory():
    directory = filedialog.askdirectory(initialdir=current_directory)
    if directory:
        output_dir.set(directory)

# 프로토콜 옵션을 선택할 때 하위 옵션을 업데이트하는 함수
def update_options(*args):
    selected_protocol = protocol_var.get()
    if selected_protocol in SDK_config.protocol:
        options = SDK_config.protocol[selected_protocol]

        # 언어 목록 업데이트
        new_languages = options.get("language", ["Not specified"])
        language_menu.configure(values=new_languages)
        language_var.set(new_languages[0])

        # 프로토콜 버전 목록 업데이트
        new_versions = options.get("wire_protocol", ["Not specified"])
        wire_protocol_menu.configure(values=new_versions)
        wire_protocol_var.set(new_versions[0])

# 코드 생성 버튼 클릭 시 호출될 함수
def generate_code():
    # 현재 선택된 옵션 가져오기
    selected_protocol = protocol_var.get()
    language = language_var.get()
    wire_protocol = wire_protocol_var.get()
    base_output_directory = output_dir.get()
    xml_file = input_dir.get()  # 단일 XML 파일

    # XML 파일을 선택하지 않았다면 경고 메시지 표시
    if not xml_file:
        show_custom_popup("Error", "Please select an XML file.", popup_type="error")
        return

    # 출력 디렉토리가 설정되지 않았다면 경고 메시지 표시
    if not base_output_directory:
        show_custom_popup("Error", "Please select an output directory.", popup_type="error")
        return

    # 프로토콜에 따라 출력 폴더 결정
    if selected_protocol in SDK_config.protocol:
        output_subfolder = SDK_config.protocol[selected_protocol]["output"][0]
        final_output_directory = os.path.join(base_output_directory, output_subfolder)

        # 출력 폴더가 없으면 생성
        if not os.path.exists(final_output_directory):
            os.makedirs(final_output_directory)
    else:
        show_custom_popup("Error", f"The protocol '{selected_protocol}' is not configured properly.", popup_type="error")
        return

    # Args 객체 생성
    args = Args(
        output=final_output_directory,
        language=language,
        wire_protocol=wire_protocol,
        max_include_file=SDK_config.MAXIMUM_INCLUDE_FILE_NESTING,
        definitions=[xml_file],  # 선택한 단일 XML 파일 목록
        exit_code=True  # 항상 True로 설정
    )

    # 프로토콜에 따른 분기 처리
    if selected_protocol == "MAVLink":
        # MAVLink일 때, mavgen 함수 호출
        try:
            ok = mav_gen.mavgen(args, args.definitions)
            if ok:
                show_custom_popup("Success", "Code generation completed successfully!", popup_type="success", directory=final_output_directory)
            else:
                show_custom_popup("Error", "Code generation failed.", popup_type="error")
                if args.exit_code:
                    exit(1)
        except Exception as e:
            show_custom_popup("Error", f"Code generation failed: {str(e)}", popup_type="error")
    else:
        # 아직 지원되지 않는 프로토콜에 대한 처리
        show_custom_popup("Info", f"The protocol '{selected_protocol}' is not supported yet.", popup_type="info")

# GUI : Custom message box =================================================================================
def show_custom_popup(title, message, popup_type="info", directory=None):
    # 팝업 창 생성
    popup = CTkToplevel()
    popup.title(title)
    popup.iconbitmap("app_icon.ico")
    popup.geometry("300x150")
    popup.resizable(False, False)  # 크기 조정 불가
    
    # 팝업 창을 앱 기준으로 표시
    popup.transient(app)  # app 창과 연동

    # 앱 창 기준으로 중앙에 위치 설정
    app_x = app.winfo_x()
    app_y = app.winfo_y()
    app_width = app.winfo_width()
    app_height = app.winfo_height()
    popup.geometry(f"+{app_x + app_width//2 - 150}+{app_y + app_height//2 - 75}")

    # 버튼 색상 설정
    fg_color = "#1E90FF"  # 기본 파란색

    # 메시지 및 버튼 추가
    CTkLabel(popup, text=message, font=("Arial", 12), wraplength=250).pack(pady=20)

    # 코드 생성 경로 열기 버튼 (성공 팝업에만 표시, 주황색)
    if popup_type == "success" and directory is not None:
        def open_directory():
            os.startfile(directory)  # 생성된 폴더 경로 열기
        open_button = CTkButton(popup, text="Open Directory", command=open_directory, fg_color="#D2691E", hover_color="#A0522D")
        open_button.pack(pady=5)
    
    # 닫기 버튼
    close_button = CTkButton(popup, text="Close", command=popup.destroy, fg_color=fg_color)
    close_button.pack(pady=10)


# GUI : APP ================================================================================================

app = CTk()
app.geometry("260x430")                 # app 창 크기 설정
app.resizable(False, False)             # app 창 크기 조절 불가
app.title("SDK Protocol")               # app title 이름
app.iconbitmap("app_icon.ico")          # app icon 설정 / 같은 경로에 app_icon.ico 파일 적용
set_appearance_mode("dark")             # app 색상 테마 CTK 패키지의 light/dark 모드 설정

# [ Frame_01 : Generation Settings ] ----------------------------------------------------------------------------------------------------
# Input XML 및 Output Directory 프레임 설정
file_frame = CTkFrame(app)
file_frame.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
CTkLabel(file_frame, text="Generation Settings", font=("Arial", 12, "bold"), text_color="grey").grid(row=0, column=0, columnspan=2, pady=4)

# - Input : XML 파일 선택
CTkLabel(file_frame, text=" •  Input XML file", font=("Arial", 13)).grid(row=1, column=0, padx=4, pady=4, sticky="w")
input_dir = tk.StringVar(app)
input_button = CTkButton(file_frame, text="Browse", font=("Arial", 12), command=add_xml_file, width=60, height=25)
input_button.grid(row=1, column=1, padx=4, pady=4, sticky="e")
input_label = CTkEntry(file_frame, textvariable=input_dir, width=230, state='readonly')  # 수정 불가능하게 설정
input_label.grid(row=2, column=0, columnspan=2, padx=4, pady=4, sticky="ew")

# - Output : Directory 선택
CTkLabel(file_frame, text=" •  Output Directory", font=("Arial", 13)).grid(row=3, column=0, padx=4, pady=4, sticky="w")
output_dir = tk.StringVar(app)
output_button = CTkButton(file_frame, text="Browse", font=("Arial", 12), command=select_output_directory, width=60, height=25)
output_button.grid(row=3, column=1, padx=4, pady=4, sticky="e")
output_label = CTkEntry(file_frame, textvariable=output_dir, width=230, state='readonly')  # 수정 불가능하게 설정
output_label.grid(row=4, column=0, columnspan=2, padx=4, pady=4, sticky="ew")

# [ Frame_02 : Protocol Settings ] ----------------------------------------------------------------------------------------------------
# Frame : Protocol, Version, Language 설정 프레임
option_frame = CTkFrame(app)
option_frame.grid(row=1, column=0, padx=8, pady=8, sticky="ew")
CTkLabel(option_frame, text="Protocol Settings", font=("Arial", 12, "bold"), text_color="grey").grid(row=0, column=0, columnspan=2, pady=4)

# - Protocol 선택 (기본 프로토콜을 "MAVLink v2.0"으로 설정)
default_protocol = "MAVLink v2.0" if "MAVLink v2.0" in SDK_config.protocol else list(SDK_config.protocol.keys())[0]

CTkLabel(option_frame, text=" •  Protocol: ").grid(row=1, column=0, sticky="w", padx=4, pady=4)
protocol_var = tk.StringVar(app)
protocol_var.set(default_protocol)
protocol_menu = CTkComboBox(master=option_frame, variable=protocol_var, values=list(SDK_config.protocol.keys()), state='readonly', width=150)
protocol_menu.grid(row=1, column=1, sticky="w", padx=4)

# - Version 선택
CTkLabel(option_frame, text=" •  Version: ").grid(row=2, column=0, sticky="w", padx=4, pady=4)
wire_protocol_var = tk.StringVar(app)
wire_protocol_menu = CTkComboBox(master=option_frame, variable=wire_protocol_var, state='readonly', width=150)
wire_protocol_menu.grid(row=2, column=1, sticky="w", padx=4)

# - Language 선택
CTkLabel(option_frame, text=" •  Language: ").grid(row=3, column=0, sticky="w", padx=4, pady=4)
language_var = tk.StringVar(app)
language_menu = CTkComboBox(master=option_frame, variable=language_var, state='readonly', width=150)
language_menu.grid(row=3, column=1, sticky="w", padx=4)

# ----------------------------------------------------------------------------------------------------

# 코드 생성 버튼 추가 (하단 중앙 배치)
generate_button = CTkButton(app, text="Generate Code", command=generate_code, fg_color="#D2691E", hover_color="#A0522D", font=("Arial", 14, "bold"), width=180, height=40)
generate_button.grid(row=2, column=0, pady=15, sticky="n")

# 프로토콜 선택 시 옵션 업데이트 연결
protocol_var.trace('w', update_options)

# 초기 옵션 설정
protocol_var.set(default_protocol)
update_options()

app.mainloop()

