# 코드 분석 도구

이 도구는 소스 코드 분석을 위한 유틸리티입니다.

## 기본 설치 항목

1. LLVM 라이브러리 설치 
    - LLVM Version : 17.0.6
    - 설치 : https://github.com/llvm/llvm-project/releases/tag/llvmorg-17.0.6

2. LLVM 라이브러리 기본 경로/파일 확인 
    - "C:/Program Files/LLVM/bin/libclang.dll"

## Flow Chart 생성 기능 사용시 설치 항목

nodejs 및 mermaid-cli 설치

1. nodejs 설치 필요
    - 설치 : https://nodejs.org/en
    - 확인 : node -v

2. npm으로 mermaid-cli 설치
    - npm install -g @mermaid-js/mermaid-cli

3. 설치 확인 
    - mmdc -v

## 프로그램 사용법

**주의 : 엑셀 파일이 열려있으면 업데이트 불가.**

### 메인 UI (SourCode Analysis)

1. **compile_commands**: px4 build 폴더에서 compile_commands.json 첨부하여 코드 분석
    - Convert : wsl 경로를 windows에서 사용 가능하게 경로 표현 수정하여 저장
    - Browse : 사용할 compile_commands.json 열기 

2. **Source Code Folder**: 코드 분석 할 소스코드의 폴더 선택
    (compile_commands 첨부 시, 해당 빌드 프로젝트에서 선택)

3. **Output Folder**: 코드 분석 결과(엑셀 파일) 생성 경로 선택

4. **Start**: 1~3 선택 후, 코드 분석 시작

5. **OpenAI API**: OpenAI로 함수 분석(요약, 흐름), 파일 flow Chart 자동 생성 후, 엑셀 파일 업데이트
    - API 사용을 위한 별도 창 팝업(Excel OpenAI Processing)

### 서브 UI (Excel OpenAI Processing)

1. **OpenAI API Key**: OpenAI API Key가 기입된 txt 파일 열기
    (OpenAI API 가입/결제 및 API Key 생성 필요)

2. **output template**: 함수 분석(요약, 흐름)을 위한 json 템플릿 선택.
    (기본경로 : 현재 실행파일의 function_template.json 선택됨)

3. **Excel File**: 함수분석을 요청 할 엑셀 파일 선택
    (*SourCode Analysis에서 생성한 엑셀 파일)

4. **Source File List / Select**: 엑셀 파일의 시트 이름(코드 파일 이름과 동일)을 자동으로 읽어옴. 분석 할 코드 파일 선택

5. **Start**: 선택한 코드 파일들을 OpenAI API로 함수 분석(요약, 흐름) 요청 및 엑셀 파일 업데이트

6. **json->xls**: OpenAI API의 함수 분석(요약, 흐름) 응답은 json파일로 저장됨. 수정하여 엑셀에 반영 할 시 사용.

7. **flowchart**: 선택한 코드 파일들의 flowchart만 별도로 생성 할 때 사용. 

8. **Open**: 선택한 엑셀 파일 열기

## 릴리스 노트

### v08 추가/수정 사항
- 클래스는 다르나 함수명이 같은 경우가 있음. 함수명에 클래스명 추가 필요 소스코드(C, CPP)에서는 구분 필요(클래스명::함수명)
- cpp에서 변수가 어느 함수에 포함되어 있는지 field에 추가
- cpp에서 함수가 여러줄에 선언되어 있는 경우 제대로 추출되지 않음. 함수가 선언된 줄 모두 포함하여 처리함 (함수 line 정의 수정) 
- (확인 필요)cpp에서 생성자는 field 정의가 안됨? 추가 수정
- build 결과물인 compile_commands.json 파일을 분석하여 경로를 Windows에서 사용 가능한 경로로 변환 및 분석에 사용
- GUI 수정 및 최적화
- 엑셀 관련, 코드 추출 관련 분리
- source code 변수 및 함수의 접근 제어자 추출
- 함수 내부 변수 추출(함수 내부 변수가 많은 경우 함수 내부 변수 추출 필요)

### v07 추가/수정 사항
- handle_param_exceptions 함수에서 정규식이 매칭되지 않는 경우 수정.
  - PX4 PARAM, Type, Variable name 추출
- 메시지 표기 수정 (경고, 에러, 완료)
  - 디버깅 위해 파일명, 코드라인 추가 표기
- 병렬 처리 4->1로 수정
  (병렬 처리 필요한가? 제대로 되는건지 모르겠음, 처리속도는 다르나 오류 발생이 일정치 않음)

### v06 추가/수정 사항
- GUI 수정 및 최적화

### v05 추가/수정 사항
- Category에서 함수(함수, 생성자, 소멸자자) 선언과 정의 구분 / Function or Function (definition)
- 정규식 기반 소스코드 원본 추출 / type, name, inputs, specifiers
  -> extern "C" __EXPORT 추출 specifiers에 추가
- 함수 예외 처리 (DEFINE_PARAMETERS_CUSTOM_PAREN, DEFINE_PARAMETERS 전처리 함수일 경우 함수 및 내부 변수 param으로 분리)
- 엑셀 시트 목록 순서 변경 
- 변수가 struct 구조인 경우 내부 변수 중복 기입 현상 수정/중복 검토

### v04 추가/수정 사항
- 노드의 구조 관계 추가
- 구조체 이름이 뒤에 있는 경우 처리