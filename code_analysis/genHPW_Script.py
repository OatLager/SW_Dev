import win32com.client as win32
import pandas as pd
import tkinter as tk
from tkinter import filedialog

def select_file():
    root = tk.Tk()
    root.withdraw()  # Tkinter 창 숨기기

    print("파일 선택 대화 상자 열기")
    file_path = filedialog.askopenfilename(
        title="엑셀 파일 선택",
        filetypes=(("Excel files", "*.xlsx;*.xls"), ("All files", "*.*"))
    )

    if not file_path:
        print("파일을 선택하지 않았습니다.")
        exit(1)

    print(f"선택한 파일: {file_path}")
    return file_path

def get_sheet_names(file_path):
    try:
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        print(f"시트 목록: {sheet_names}")
        return sheet_names
    except Exception as e:
        print(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {e}")
        exit(1)

def select_sheet(sheet_names):
    sheet_window = tk.Tk()
    sheet_window.title("시트 선택")

    tk.Label(sheet_window, text="시트 이름을 선택하세요:").pack()

    selected_sheet = tk.StringVar(sheet_window)
    selected_sheet.set(sheet_names[0])  # 기본값 설정

    sheet_menu = tk.OptionMenu(sheet_window, selected_sheet, *sheet_names)
    sheet_menu.pack()

    def on_select():
        global sheet_name
        sheet_name = selected_sheet.get()
        print(f"선택한 시트: {sheet_name}")
        progress_window = tk.Toplevel(sheet_window)
        progress_window.title("진행 상황")

        progress_label = tk.Label(progress_window, text="")
        progress_label.pack()

        # 엑셀 데이터 읽기
        data = read_excel_data(file_path, sheet_name)
        function_data = filter_function_data(data)
        hwp = create_hwp_document()

        total_functions = len(function_data)
        current_function = 0

        # 필터링된 데이터를 기반으로 표 생성
        for index, row in function_data.iterrows():
            current_function += 1
            progress_label.config(text=f"총 {total_functions}개 중 {current_function}번째 함수 생성 중: {row['Name']}")
            progress_window.update()

            print(f"표 생성 시작: {row['Name']}")

            hwp.HAction.GetDefault("TableCreate", hwp.HParameterSet.HTableCreation)
            hwp.HParameterSet.HTableCreation.Rows = 6  # 행 개수
            hwp.HParameterSet.HTableCreation.Cols = 2  # 열 개수
            hwp.HAction.Execute("TableCreate", hwp.HParameterSet.HTableCreation)

            # 표에 데이터 채우기
            hwp.MovePos(2)  # 첫 번째 셀로 이동
            hwp.PutText("기능")
            hwp.MovePos(4)  # 오른쪽으로 이동
            hwp.PutText(row['Name'])  # 함수 이름

            hwp.MovePos(2)  # 다음 행으로 이동
            hwp.PutText("소스 파일명")
            hwp.MovePos(4)
            hwp.PutText(row['File Name'])  # 소스 파일명

            hwp.MovePos(2)
            hwp.PutText("입력")
            hwp.MovePos(4)
            hwp.PutText(row['Input'] if not pd.isnull(row['Input']) else "없음")  # 입력 데이터

            hwp.MovePos(2)
            hwp.PutText("출력")
            hwp.MovePos(4)
            hwp.PutText(row['Output'] if not pd.isnull(row['Output']) else "없음")  # 출력 데이터

            print(f"표 생성 완료: {row['Name']}")

        save_hwp_document(hwp)
        progress_window.destroy()

    tk.Button(sheet_window, text="확인", command=on_select).pack()

    print("mainloop 시작")  # 디버그 메시지 추가
    sheet_window.mainloop()
    print("mainloop 종료")  # 디버그 메시지 추가

    return sheet_name

def read_excel_data(file_path, sheet_name):
    try:
        print(f"선택한 시트에서 데이터 읽기: {sheet_name}")
        data = pd.read_excel(file_path, sheet_name=sheet_name)
        print("엑셀 데이터 읽기 완료")
        return data
    except Exception as e:
        print(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {e}")
        exit(1)

def filter_function_data(data):
    print("Function 카테고리 데이터 필터링")
    function_data = data[data['Category'] == 'Function']
    print(f"필터링된 함수 개수: {len(function_data)}")
    return function_data

def create_hwp_document():
    try:
        print("한컴오피스 HWP 객체 생성")
        hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
        print("HWP 객체 생성 완료")
    except Exception as e:
        print(f"HWP 객체를 생성하는 중 오류가 발생했습니다: {e}")
        exit(1)

    print("새 문서 열기")
    hwp.XHwpDocuments.Add(isTab=False)  # isTab 매개 변수를 False로 설정
    print("새 문서 열기 완료")

    return hwp

def save_hwp_document(hwp):
    save_path = filedialog.asksaveasfilename(
        defaultextension=".hwp",
        filetypes=(("HWP files", "*.hwp"), ("All files", "*.*")),
        title="한글 파일 저장"
    )

    if save_path:
        hwp.SaveAs(save_path)
        print(f"HWP 파일이 {save_path}에 저장되었습니다.")
    else:
        print("파일 저장이 취소되었습니다.")

    print("HWP 파일 생성이 완료되었습니다.")

def main():
    global file_path
    file_path = select_file()
    sheet_names = get_sheet_names(file_path)
    select_sheet(sheet_names)

if __name__ == "__main__":
    main()