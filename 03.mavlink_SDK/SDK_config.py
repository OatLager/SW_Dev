# from datetime import datetime

# def generated_time():
#     return datetime.now()

MAXIMUM_INCLUDE_FILE_NESTING = 5

protocol = {
    "MAVLink":{
        "language": ["c"],          # 지원 언어
        "wire_protocol": ["2.0"],   # 프로토콜 버전
        "output": ["mavlink"]       # 출력 폴더명 
    },
    "MIL_STD":{
        "language": ["not supported"],
        "wire_protocol": ["not supported"],
        "output": ["mil_std"]
    }
}

