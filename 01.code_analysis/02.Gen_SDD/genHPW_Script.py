# 한글 2024 버전에서 작동하는 코드
# 소프트웨어 설계 기술서(SDD) 변수/함수 목록 및 함수 내역 작성 코드

# 추가할 기능 내용 
# 1. 변수/함수 목록 채우기
# 3. 각 파일 병합 기능

from pyhwpx import Hwp
import pandas as pd
from openpyxl import load_workbook
import time
import os
import tkinter as tk
from tkinter import ttk, filedialog


class SDD:
    def __init__(self):
        
        # 템플릿 파일 경로
        current_dir  = os.path.dirname(os.path.abspath(__file__))
        context_file = "SDD_함수목록.hwp"
        function_file = "SDD_함수내역.hwp"
        self.insert_context_table = os.path.join(current_dir, context_file)
        self.insert_function_table = os.path.join(current_dir, function_file)

        # test용 경로 및 설정, 추후 ui 연동 필요
        self.ExcelFile = self.select_input_file()
        self.save_file_path = os.path.splitext(self.ExcelFile)[0]


    def select_input_file(self):
    # 파일 다이얼로그 열기
        file_path = filedialog.askopenfilename(
        title="Select a Excel File",
        filetypes=[("Excel", "*.xls *.xlsx"), ("All files", "*.*")]
        )
        if file_path:
            print("Selected Excel file:", file_path)
        else:
            print("No Excel file selected.")

        return os.path.join(file_path)
    
    # output 경로 선택
    def select_output_path(self, output_file):
        output_path = filedialog.askdirectory()
        return os.path.join(output_path, output_file)


    # 엑셀파일에서 테이블 정보 추출
    def ExcelToDataFrame(self, file_path):
        # 필요한 컬럼 리스트
        function_to_extract = ["File Name", "Field", "Name", "Input", "Type", "Summary", "Description"]
        variable_to_extract = ["File Name", "Field", "Name", "Type", "Summary"]
        # 결과 저장 리스트
        function_list = []
        variable_list = []

        # 엑셀 파일 로드
        xls = pd.ExcelFile(file_path, engine="openpyxl")

        for sheet in xls.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet, engine="openpyxl")
            print(sheet)
            # Category 컬럼이 있는지 확인
            if "Category" in df.columns:
                
                # 시트명이 헤더 파일인 경우에만 변수 추출
                if sheet.endswith(".h") or sheet.endswith(".hpp"):
                    # variable : Variable을 포함하는 행 필터링 및 Access가 private인 행 필터링
                    var_filtered_df = df[(df["Category"].astype(str).str.contains(r"Variable", na=False, regex=True)) & (df["Access"].astype(str).str.contains(r"private", na=False, regex=True))]
                    # 필요한 컬럼만 선택 (컬럼이 존재하는 경우만 선택)
                    var_extracted_columns = [col for col in variable_to_extract if col in var_filtered_df.columns]
                    var_filtered_df = var_filtered_df[var_extracted_columns]
                    # NaN 값을 빈 문자열("")로 변환
                    var_filtered_df = var_filtered_df.fillna("")
                    var_filtered_df = var_filtered_df.replace(r"\(class\)|\(struct\)|\(namespace\)", "", regex=True)
                    # 시트별로 데이터를 저장
                    # variable_list[sheet] = var_filtered_df.to_dict(orient="records")
                    variable_list.extend(var_filtered_df.to_dict(orient="records"))

                # 함수 추출
                # function : (definition)을 포함하는 행 필터링
                func_filtered_df = df[df["Category"].astype(str).str.contains(r"\(definition\)", na=False, regex=True)]
                # 필요한 컬럼만 선택 (컬럼이 존재하는 경우만 선택)
                func_extracted_columns = [col for col in function_to_extract if col in func_filtered_df.columns]
                func_filtered_df = func_filtered_df[func_extracted_columns]
                # NaN 값을 빈 문자열("")로 변환
                func_filtered_df = func_filtered_df.fillna("")
                func_filtered_df = func_filtered_df.replace(r"\(class\)|\(struct\)|\(namespace\)", "", regex=True)
                # 시트별로 데이터를 저장
                # function_list[sheet] = func_filtered_df.to_dict(orient="records")
                function_list.extend(func_filtered_df.to_dict(orient="records"))
               

        # 결과 출력(시트별 함수, 변수)
        return function_list, variable_list

    def insert_template_file(self, path):
        self.hwpx.insert_file(path)

    def main(self):
       
        # 엑셀 파일에서 모든 시트 - 테이블 정보 추출 
        function_list, variable_list = self.ExcelToDataFrame(self.ExcelFile)
        # print(f"함수 리스트 : {function_list}")
        # print(f"변수 리스트 : {variable_list}")
        file_name = os.path.splitext(os.path.basename(self.ExcelFile))[0]
        # 시트별로 한글 문서 작성
        # for sheet_name, sheet_data in function_list.items():
        if function_list or variable_list:
            # 한글 문서 생성
            self.hwpx = Hwp(new=True, visible=False)
            time.sleep(0.1)

            # 한글 문서 작성
            # step 1 - 변수/함수 목록
            # step 1.1 - 변수/함수 목록 페이지 삽입 (table 0)
            self.insert_template_file(self.insert_context_table)
            # print(f'insert {self.insert_context_table}')
            # step 1.2 - 페이지 개요 작성
            self.hwpx.insert_text(f"{file_name} 변수․함수 목록")
            # step 1.3 - 테이블에 변수/함수 목록 작성
            self.hwpx.get_into_nth_table(0) # 테이블 이동
            self.hwpx.ShapeObjTableSelCell() # 해당 테이블 첫번째 셀 선택
            self.hwpx.TableRightCell() # 셀 오른쪽 이동
            self.hwpx.TableLowerCell() # 셀 아래 이동 : 변수 목록 시작 셀

            # 변수 목록 작성
            if variable_list:
                print(f"변수 : {len(variable_list)}")
                for i, var in enumerate(variable_list):
                    # 기존 테이블 2행 처리
                    if i >= len(variable_list) - 2:
                        # print(f"변수 {i+1}/{len(variable_list)}")
                        self.hwpx.insert_text(f"{var['Type']}")
                        self.hwpx.TableRightCell()
                        self.hwpx.insert_text(f"{var['Field']}::{var['Name']}")
                        self.hwpx.TableRightCell()
                        self.hwpx.insert_text(f"{var['Summary']}")
                        self.hwpx.TableLeftCell()
                        self.hwpx.TableLeftCell()
                        self.hwpx.TableLowerCell()
                        if i == len(variable_list) - 1:
                            if len(variable_list) == 1:
                                self.hwpx.TableLowerCell()
                            break
                    else:    
                        self.hwpx.insert_text(f"{var['Type']}")
                        self.hwpx.TableRightCell()
                        self.hwpx.insert_text(f"{var['Field']}::{var['Name']}")
                        self.hwpx.TableRightCell()
                        self.hwpx.insert_text(f"{var['Summary']}")
                        self.hwpx.TableAppendRow()
                        self.hwpx.TableLeftCell()
                        self.hwpx.TableLeftCell()               
            else:
                print("변수 목록이 없습니다.")
                self.hwpx.TableLowerCell()
                self.hwpx.TableLowerCell()

            # 함수 목록 작성
            if function_list:
                print(f"함수 : {len(function_list)}")
                 
                for i, func in enumerate(function_list):
                    # 기존 테이블 2행 처리
                    if i >= len(function_list) - 2:
                        self.hwpx.insert_text(f"{func['Type']}")
                        self.hwpx.TableRightCell()
                        self.hwpx.insert_text(f"{func['Field']}::{func['Name']}")
                        self.hwpx.TableRightCell()
                        self.hwpx.insert_text(f"{func['Summary']}")
                        self.hwpx.TableLeftCell()
                        self.hwpx.TableLeftCell()
                        self.hwpx.TableLowerCell()
                        if i == len(function_list) - 1:
                            break
                    else:
                        self.hwpx.insert_text(f"{func['Type']}")
                        self.hwpx.TableRightCell() # 셀 오른쪽 이동
                        self.hwpx.insert_text(f"{func['Field']}::{func['Name']}")
                        self.hwpx.TableRightCell()
                        self.hwpx.insert_text(f"{func['Summary']}")
                        self.hwpx.TableAppendRow() # 테이블 행(row) 추가 / 자동으로 커서 이동
                        self.hwpx.TableLeftCell() # 셀 왼쪽 이동
                        self.hwpx.TableLeftCell() # 셀 왼쪽 이동
                        
                    
                # step 1.4 - 변수/함수 목록 표 캡션 작성
                self.hwpx.get_into_table_caption()   # 표 캡션(번호) 이동
                self.hwpx.move_pos(14) # 표 캡션 번호 뒤로 이동
                self.hwpx.insert_text(f" {file_name} 변수․함수 목록") # 표 캡션 작성

                # step 2 - 함수 내역
                i = 0
                for i, func in enumerate(function_list):
                    time.sleep(0.1)
                    i+=1
                    self.hwpx.MoveDocEnd() # 커서를 문서 끝으로 이동
                    self.hwpx.BreakPage()  # 페이지 나누기
                    time.sleep(0.1)
                    # step 2.1 - 함수 내역 페이지 삽입 (table 1~)
                    self.insert_template_file(self.insert_function_table)
                    # print(f'insert {self.insert_function_table}')

                    # step 2.2 - 페이지 개요 작성
                    self.hwpx.insert_text(f"{func['Field']}::{func['Name']}() 함수")
                
                    # step 2.3 - 테이블에 함수 내용 추가
                    # - 테이블 이동, 셀 선택으로 정해진 템플릿에 맞게 셀 이동하여 내용 삽입.
                    self.hwpx.get_into_nth_table(i) # 테이블 이동
                    self.hwpx.ShapeObjTableSelCell() # 해당 테이블 첫번째 셀 선택
                    # 기능
                    self.hwpx.TableRightCell() # 셀 오른쪽 이동
                    self.hwpx.insert_text(f"{func['Summary']}")
                    # 모함수명
                    self.hwpx.TableLowerCell() # 셀 아래 이동
                    self.hwpx.insert_text("")
                    # 소스파일명
                    self.hwpx.TableRightCell() # 셀 오른쪽 이동
                    self.hwpx.TableRightCell() # 셀 오른쪽 이동
                    self.hwpx.insert_text(f"{func['File Name']}")
                    # 출력
                    self.hwpx.TableLowerCell() # 셀 아래 이동
                    self.hwpx.insert_text(f"{func['Type']}")
                    # 입력
                    self.hwpx.TableLeftCell() # 셀 왼쪽 이동
                    self.hwpx.TableLeftCell() # 셀 왼쪽 이동
                    if func['Input']:
                        input_lines = func['Input'].split(',')
                        for i, line in enumerate(input_lines):
                            self.hwpx.insert_text(line)
                            if i != len(input_lines) - 1:  # 마지막 줄이 아니면 개행
                                self.hwpx.insert_text(",")
                                self.hwpx.BreakPara() # 엔터, 줄바꿈
                    # 처리
                    self.hwpx.TableLowerCell() # 셀 아래 이동
                    self.hwpx.TableLowerCell() # 셀 아래 이동
                    description_lines = func['Description'].split('\n')
                    for i, line in enumerate(description_lines):
                        self.hwpx.insert_text(line)
                        self.hwpx.BreakPara()

                    # step 2.4 - 테이블 캡션 작성
                    # self.hwpx.ShapeObjInsertCaptionNum() # 표 캡션 번호 삽입
                    self.hwpx.get_into_table_caption()   # 표 캡션(번호) 이동
                    self.hwpx.move_pos(14) # 표 캡션 번호 뒤로 이동
                    self.hwpx.insert_text(f" {func['Field']}::{func['Name']}() 함수 내역") # 표 캡션 작성

        # step 3 - 한글 문서 저장
        save_file = self.hwpx.SaveAs(self.save_file_path+".hwp")
        time.sleep(1)
        self.hwpx.clear()
        print(f"file : {save_file}")
        # time.sleep(1)

if __name__ == "__main__":
    sdd = SDD()
    sdd.main()