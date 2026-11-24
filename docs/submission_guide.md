# 환경 구성 보고서 제출 안내

제출 문서는 [CloudMate 환경 구성 보고서](environment_report.md)를 기준으로 작성합니다. 사용한 AWS 서비스, 개발 환경, GitHub 저장소와 실제 실행 검증 결과를 포함하고, 아래 순서로 기본 실행 확인 화면을 첨부합니다.

## 1. 보고서 본문 준비

보고서에는 다음 내용을 순서대로 배치합니다.

1. 프로젝트 목적과 현재 구현 범위
2. 사용한 AWS 서비스와 각 서비스의 역할
3. Python·Git·AWS CLI·SAM CLI 등 개발 환경 구성
4. API Gateway → Lambda → CloudWatch 실행 흐름과 S3 문서 저장 구조
5. 실제 API 응답, 문서 저장, 보안 설정과 테스트 결과
6. GitHub 저장소 주소와 코드 관리 결과
7. 기본 실행 확인 화면과 화면별 설명
8. 향후 RAG 구현 계획

보고서의 AWS 스택 이름은 `cloudmate`, API 표시 이름은 `cloudmate-http-api`를 사용합니다. 문서·함수·로그 등 실제 이름은 보고서의 리소스 표와 대조합니다. 주차별 과제 구분과 AWS 리소스 이름을 분리합니다.

## 2. 기본 실행 확인 화면

아래 화면은 실제 환경에서 직접 촬영합니다. 콘솔이나 실행 결과를 대신하는 이미지를 만들지 않습니다. 캡처 전에 개인 경로, 학번·이름, 계정 번호, ARN의 계정 부분과 인증 정보를 가리거나 화면에서 제외합니다.

### 그림 1 상태 API 실행 결과

VS Code 터미널에서 프로젝트 가상환경을 활성화하고 다음 명령을 실행합니다.

```sh
source .venv/bin/activate
export SSL_CERT_FILE="$(python -m certifi)"
python scripts/verify_api.py https://b1prf542b3.execute-api.ap-northeast-2.amazonaws.com/health
```

실제 URL, `http_status: 200`, `passed: true`와 응답 본문이 한 화면에 나오도록 촬영합니다. 본문은 status, service, message 세 필드이며 주차 정보는 포함하지 않습니다.

그림 설명 예시: “API Gateway의 GET /health 요청이 Lambda에 전달되어 HTTP 200과 CloudMate 정상 상태 JSON을 반환하는 것을 확인하였다.”

### 그림 2 AWS 리소스 구성

서울 리전의 CloudFormation → Stacks → `cloudmate` → Resources에서 스택 완료 상태와 리소스 목록을 촬영합니다. 화면에 계정 번호가 있는 헤더나 ARN은 가립니다.

그림 설명 예시: “CloudFormation의 cloudmate 스택에서 Lambda, HTTP API, S3, IAM 역할과 로그 그룹을 관리하며, 리소스 이름에 주차 정보를 사용하지 않도록 구성하였다.”

### 그림 3 GitHub 저장소

https://github.com/MikGiNwong/cloudmate-rag-chatbot 의 Code 화면에서 저장소 주소, 공개 상태, 프로젝트 폴더와 README를 촬영합니다. Commits 화면에서 최종 문서 커밋을 추가 촬영할 수 있습니다.

그림 설명 예시: “공개 GitHub 저장소에서 소스 코드, SAM 인프라 코드, 환경 구성 보고서와 실행 증거를 관리하였다.”

### 개발 환경과 추가 증거

개발 환경 화면이 필요하면 가상환경을 활성화한 터미널에서 `python --version`, `git --version`, `sam --version`, `aws --version`을 실행해 촬영합니다. `aws` 명령이 없다면 설치된 CLI 경로 또는 `.tools/bin/aws`를 사용합니다. 인증 확인 명령의 계정·ARN 출력은 제출 화면에 포함하지 않습니다.

S3 검증은 S3 → 문서 버킷 → `documents/aws-faq.txt`, 로그 검증은 CloudWatch → Log groups → `/aws/lambda/cloudmate-health-check`의 최신 로그 스트림에서 추가 촬영할 수 있습니다. 최신 로그의 `health_check status=ok`를 확인합니다.

## 3. 파일과 그림 정리

원본 화면은 로컬 `docs/evidence/screenshots/`에 `01-health-api.png`, `02-cloudformation.png`, `03-github.png`처럼 저장합니다. 이 폴더는 개인정보 검토 전 원본 공개를 막기 위해 Git에서 제외합니다.

Word 또는 한글 문서에 보고서 본문을 옮긴 뒤, 각 검증 항목 아래에 캡처와 그림 설명을 삽입합니다. Markdown으로 제출할 경우 검토한 이미지 파일을 보고서와 함께 묶고 다음과 같이 상대 경로로 연결할 수 있습니다.

```markdown
![그림 1 상태 API의 실제 HTTP 200 응답](evidence/screenshots/01-health-api.png)
```

온라인 저장소에서 그림도 보여야 한다면 개인정보를 가린 제출용 복사본을 별도 경로에 두고 검토 후 추가합니다. 원본 콘솔 화면이나 인증 자료를 그대로 공개하지 않습니다.

## 4. 최종 확인

보고서의 서비스명과 실제 AWS 설정, API 응답, GitHub 주소가 일치하는지 확인합니다. CLI 기반 실행 증거는 `docs/evidence/`에서 확인할 수 있습니다. 이 안내서는 캡처 절차를 제공하며, 실제 화면 파일을 촬영했다고 기록하지 않습니다.
