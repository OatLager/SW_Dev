

import openai
import json
import time
import tkinter as tk
from tkinter import filedialog
import os
import re

# tkinter를 사용하여 파일 선택 UI 생성
# root = tk.Tk()
# root.withdraw()  # Hide the root window

# 주요 함수 ==================================================================================

# [Function] File Input : Get Selected File Path ----------------------------------------------------------------------------------
def select_file_path(file_type):
    file_path = filedialog.askopenfilename(title=f"Select the {file_type} file", filetypes=[(f"{file_type} files", f"*.{file_type}")])
    if not file_path:
        raise ValueError("No file selected")
    return file_path

# [Function] File Input : OpenAI API Key ----------------------------------------------------------------------------------
def set_openai_api_key(file_path):
    with open(file_path, "r") as file:
        openai.api_key = file.read().strip()
        return openai.api_key

# [Function] File Input : json template ----------------------------------------------------------------------------------
def upload_json_template(file_path):
    json_template_file = openai.files.create(
        file=open(file_path, "rb"),
        purpose="assistants"
    )
    json_template_id = json_template_file.id
    print(f"  🔹 JSON Template File Upload 확인 : {os.path.basename(file_path)}")

    return json_template_id

# [Function] File Input : Source Code  ----------------------------------------------------------------------------------
def upload_code_file(file_path):
    if not file_path:
        raise ValueError("No file selected")

    file = openai.files.create(
        file=open(file_path, "rb"),
        purpose="assistants"
    )
    code_file_id = file.id
    print(f"  🔹 Source Code File Upload 확인 : {os.path.basename(file_path)}")
    return code_file_id

# [Function] API : Create/Delete Assistant ----------------------------------------------------------------------------------
def create_assistant():
    assistant = openai.beta.assistants.create(
        name="API - C/C++ Function Analyzer",
        instructions="""
너는 소스 코드 분석 전문가야. 
내가 "[A]의 [B] 함수 설명"이라고 전달하면 첨부된 소스코드 기반으로 [A]에 속한 함수 [B]에 대한 설명을 해줘. 응답은 첨부된 json 파일과 동일한 형태로 출력 해줘.(**불필요한 텍스트, 코드블록 제거**)
[A]와 [B]는 문자 그대로 전부 사용해줘.
[A]가 없을 시에는 "의 [B] 함수 설명"으로 전달할거야. 그러면 class가 없는 함수에 대한 설명을 해줘.

## 입력 요청 예시 :

        "[A]의 [B] 함수 설명" : "(class)mode의 run 함수 설명"
         -> [A] = (class)mode, [B] = run

## 출력 응답 예시 :

        {
           " class": "(class)mode",
            "name": "run",
            "summary": "MulticopterRateControl의 주 실행 함수",
            "flow": [
                "1. 종료 조건 확인",
                "2. 성능 측정 시작",
                "3. 파라미터 업데이트 확인",
                "   3.1. 파라미터 업데이트가 있을 경우, 업데이트 내용 복사",
                "   3.2. 파라미터 업데이트",
                "4. Gyro 변화에 따른 Rate Controller 실행",
                "   4.1. vehicle angular velocity 업데이트 확인",
                "      4.1.1. 현재 시간(now) 및 dt 계산",
                "      4.1.2. 각속도 및 각가속도 벡터 생성",
                "      4.1.3. vehicle control mode 업데이트",
                "      4.1.4. vehicle land detected 업데이트",
                "      4.1.5. vehicle status 업데이트",
                "  4.2. 수동 제어 모드에서의 vehicle rates setpoint 생성",
                "      4.2.1. manual control setpoint 업데이트 확인",
                "      4.2.2.  vehicle rates setpoint 계산 및 Publish",
                "  4.3. Rate Controller 실행",
                "     4.3.1. Rate Controller 상태 업데이트",
                "     4.3.2. Rate Controller 업데이트 호출",
                "     4.3.3. Publish : torque 및 thrust setpoint ",
                "5. 성능 측정 종료"
            ]
        }

## 출력 언어
1. (문장의 주어와 목적어는 영어 그대로 사용)한국어로 번역.
2. vehicle은 비행체로 번역

## 출력의 flow 작성 조건 : 
1. 함수 내부의 제어 흐름을 **"인덴트 규칙"**에 따라 트리 구조로 분류
2. 분류 한 트리 구조에 번호 부여하고, 하위 트리는 .으로 구분
                    """,
        tools=[{"type": "file_search"}],  # 파일 검색 활성화
        model="gpt-4o-mini"
    )
    assistant_id = assistant.id
    print("  🔹 Create Assistant ID:", assistant_id)
    return assistant_id

def delete_assistant(assistant_id):
    try:
        openai.beta.assistants.delete(assistant_id=assistant_id)
        print(f"  🔸 Delete Assistant ID: {assistant_id}")
    except Exception as e:
        print(f"❌ Error - Failed to delete Assistant: {e}")

def delete_upload_file(file_id):
    try:
        openai.files.delete(file_id=file_id)
        print(f"  🔸 Delete File ID: {file_id}")
    except Exception as e:
        print(f"❌ Error - Failed to delete File: {e}")

# [Function] API : Create Assistant - Thread 
def create_thread():
    thread = openai.beta.threads.create()
    thread_id = thread.id
    print("  🔹 Create Thread ID:", thread_id)
    return thread_id

# [Function] API : Run Assistant Thread (with message & json Template & Source Code) 
def run_assistant(thread_id, assistant_id, code_file_id, json_template_id, message_content):
    # 요청 메시지 생성 (파일 참조)

    attachments = [{"file_id": code_file_id, "tools": [{"type": "file_search"}]}]
    if json_template_id:
        attachments.append({"file_id": json_template_id, "tools": [{"type": "file_search"}]})

    message = openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_content,
        attachments=attachments
    )

    # Run 실행 (API 요청)
    run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    return run.id, message.id

# [Function] API : Wait for API Response
def wait_for_run_completion(thread_id, run_id):
    while True:
        run_status = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run_status.status == "completed":
            break
        elif run_status.status in ["failed", "cancelled"]:
            print(f"❌ Error - OpenAI 응답 생성 실패: {run_status.status}")
            return None
        time.sleep(2)  

# [Function] API : Get API Response 
def get_api_response(thread_id):
    messages = openai.beta.threads.messages.list(thread_id=thread_id)
    for msg in messages.data:
        if msg.role == "assistant":  
            return msg.content[0].text.value  
    return None

# [Function] API : Save API Response as JSON 
def response_save_json(response_text, save_path, json_file_name):
    
    # json_file = open(cleaned_response_text, "r")
    if response_text:
        # JSON 변환 시도
        json_function_list = []
        try:
            json_data = [json.loads(item) for item in response_text]
            json_data_function = {
                "functions": json_data
            }
            # print(f'json_data_function : \n{json_data_function}')


            # save_path에 'function_description' 폴더를 생성
            folder_path = os.path.join(save_path, "function_description")

            # 폴더가 존재하지 않으면 생성
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # json 파일 저장 경로
            full_save_path = os.path.join(folder_path, f"{json_file_name}.json")

            # full_save_path = f"{save_path}/{json_file_name}.json"
            with open(full_save_path, "w", encoding="utf-8") as json_file:
                json.dump(json_data_function, json_file, ensure_ascii=False, indent=4)
            print(f"  🔸 JSON 파일 저장 완료: {full_save_path}")
            classes = [func['class'] for func in json_data_function["functions"]]
            names = [func['name'] for func in json_data_function["functions"]]
            summaries = [func['summary'] for func in json_data_function["functions"]]
            flows = [func['flow'] for func in json_data_function["functions"]]
            json_function_list.append((classes, names, summaries, flows))

            return json_function_list
        
        except json.JSONDecodeError as e:
            print("❌ Error - JSON 변환 실패: API 응답 메시지 확인.", e)
    else:
        print("❌ Error - API 응답 메시지 수신 불가")
        return None

# [Main Function] API : API 실행 함수(AIP 요청 메시지, 업로드할 파일 경로, JSON 템플릿 파일 경로)
def execute_openai_assistant(message_content_list, code_file_path=None, json_template_file_path=None):
    
    # Input date files upload
    code_file_id = upload_code_file(code_file_path) if code_file_path else None
    json_template_id = upload_json_template(json_template_file_path) if json_template_file_path else None

    # Assistant & Thread 기존 생성 사용
    assistant_id = None #'asst_8T6sSyVDzDdzOMYt42LWfbnu' # None
    thread_id = None

    if not assistant_id:
        assistant_id = create_assistant()
    if not thread_id:
        thread_id = create_thread()

    # API에서 분석중인 코드 파일 확인 및 분석, 결과 확인
    current_file_name = os.path.basename(code_file_path)
    responses = []
    for message_content in message_content_list:
        # Run Assistant with message
        run_id, message_id = run_assistant(thread_id, assistant_id, code_file_id, json_template_id, message_content)

        current_msg_content = f"({message_content_list.index(message_content) + 1}/{len(message_content_list)})"
        print(f"\n  🔹 {current_file_name}{current_msg_content} - {message_content} 생성 중... : ") 

        # Wait for run completion
        wait_for_run_completion(thread_id, run_id)   
        response = get_api_response(thread_id)
        responses.append(response)

        formatted_response = "\n     ".join(response.split("\n"))
        print(f"  🔹 API Response msg\n     {formatted_response}")

    # delete_assistant(assistant_id)
    return responses, assistant_id, code_file_id, json_template_id

# [Main Function] API : Flowchart 생성 함수
def execute_openai_assistant_to_create_flowchart(code_file_path):
    message_content = "cpp 코드에 대한 mermaid Flowchart 요청"
    if code_file_path:
        code_file_id = upload_code_file(code_file_path)
        
    # flowchart assistant 생성
    assistant = openai.beta.assistants.create(
        name="API - C/C++ File Flowchart",
        instructions="""
소스 코드 분석

# 출력 형식
mermaid flowchart 형식으로 출력(불필요한 텍스트 제거)

# 예제

출력:
```mermaid
graph TD
    A["함수 시작"] --> B["조건 X 확인"]
    B --> C{"X가 참이면 동작 A 실행"}
    C -->|참| D["동작 A 실행"]
    C -->|거짓| E["동작 B 실행"]
    E --> F["함수 종료"]
    D --> F
    F -->|함수 종료| G["함수 종료"]
```
                    """,
        tools=[{"type": "file_search"}],  # 파일 검색 활성화
        model="gpt-4o-mini"
    )

    thread_id = create_thread()
    # run assistant with message
    run_id, message_id = run_assistant(thread_id, assistant.id, code_file_id, None, message_content)
    wait_for_run_completion(thread_id, run_id)
    response_text =  get_api_response(thread_id)

    cleaned_response_text = re.sub(r"```mermaid\n|\n```", "", response_text)
    formatted_response = "\n     ".join(cleaned_response_text.split("\n"))
    print(f"  🔹 API Response msg\n     {formatted_response}")

    delete_assistant(assistant.id)
    delete_upload_file(code_file_id)

    return cleaned_response_text

