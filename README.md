# SW_Dev

소프트웨어 개발 저장소입니다. 본 저장소는 다양한 소프트웨어 개발 도구와 스크립트를 포함하고 있습니다.

## 포함된 도구

### Code Analysis

코드 분석 도구는 C/C++ 소스 코드를 분석하여 함수, 변수, 구조체 등의 정보를 엑셀 파일로 추출합니다. LLVM과 Clang을 사용합니다.

주요 기능:
- 소스 코드 구조 분석
- 함수 및 변수 추출
- 엑셀 파일 생성
- OpenAI API를 활용한 코드 분석 자동화
- 플로우 차트 자동 생성

### 사용 방법

각 도구의 상세한 사용 방법은 해당 디렉토리의 README.txt 또는 README.md 파일을 참조하세요.

## 요구 사항

- Python 3.x
- LLVM/Clang 17.0.6
- 기타 requirements.txt에 명시된 라이브러리

## 설치 방법

```bash
# 저장소 클론
git clone https://github.com/OatLager/SW_Dev.git

# 필요한 패키지 설치
cd SW_Dev/code_analysis
pip install -r requirements.txt
```
