[기본 설치 항목]
1. LLVM 라이브러리 설치 
    - LLVM Version : 17.0.6
    - 설치 : https://github.com/llvm/llvm-project/releases/tag/llvmorg-17.0.6

2. LLVM 라이브러리 기본 경로/파일 확인 
    - "C:/Program Files/LLVM/bin/libclang.dll"


[flow chart 생성 기능 사용시 설치 항목] 
nodejs 및 mermaid-cli 설치

1. nodejs 설치 필요
    설치 : https://nodejs.org/en
    확인 : node -v

2. npm으로 mermaid-cli 설치
    npm install -g @mermaid-js/mermaid-cli

3. 설치 확인 
    mmdc -v


[프로그램 사용법]

 *주의 : 엑셀 파일이 열려있으면 업데이트 불가.

    (main ui : SourCode Analysis) ------------------------------------------------

    1. compile_commands: px4 build 폴더에서 compile_commands.json 첨부하여 코드 분석
            - Convert : wsl 경로를 windows에서 사용 가능하게 경로 표현 수정하여 저장
            - Browse : 사용할 compile_commands.json 열기 

    2. Source Code Folder: 코드 분석 할 소스코드의 폴더 선택
                        (compile_commands 첨부 시, 해당 빌드 프로젝트에서 선택)

    3. Output Folder: 코드 분석 결과(엑셀 파일) 생성 경로 선택

    4. Start : 1~3 선택 후, 코드 분석 시작

    5. OpenAI API : OpenAI로 함수 분석(요약, 흐름), 파일 flow Chart 자동 생성 후, 엑셀 파일 업데이트
            - API 사용을 위한 별도 창 팝업(Excel OpenAI Processing)                    


    (sub ui : Excel OpenAI Processing) ------------------------------------------

    1. OpenAI API Key : OpenAI API Key가 기입된 txt 파일 열기
                        (OpenAI API 가입/결제 및 API Key 생성 필요)

    2. output template : 함수 분석(요약, 흐름)을 위한 json 템플릿 선택.
                        (기본경로 : 현재 실행파일의 function_template.json 선택됨)

    3. Excel File : 함수분석을 요청 할 엑셀 파일 선택
                        (*SourCode Analysis에서 생성한 엑셀 파일)

    4. Source File List / Select
        엑셀 파일의 시트 이름(코드 파일 이름과 동일)을 자동으로 읽어옴. 분석 할 코드 파일 선택

    5. Start : 선택한 코드 파일들을 OpenAI API로 함수 분석(요약, 흐름) 요청 및 엑셀 파일 업데이트

    6. json->xls : OpenAI API의 함수 분석(요약, 흐름) 응답은 json파일로 저장됨. 수정하여 엑셀에 반영 할 시 사용.

    7. flowchart : 선택한 코드 파일들의 flowchart만 별도로 생성 할 때 사용. 

    8. Open : 선택한 엑셀 파일 열기