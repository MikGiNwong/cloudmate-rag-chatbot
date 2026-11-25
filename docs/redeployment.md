# CloudMate 개발 재개 및 AWS 재배포

2026년 11월 25일 과제 제출 후 CloudMate의 AWS 리소스를 삭제했습니다. 로컬 개발 환경, GitHub 소스, SAM 설정, FAQ와 실행 증거는 보존했습니다. 아래 명령은 다음 개발을 재개할 때 실행합니다. 재배포하면 AWS 사용료가 다시 발생할 수 있습니다.

## 1. 로컬 환경 준비

기존 프로젝트 폴더에서 실행합니다. `.venv`와 `.tools`는 로컬에 유지되어 있습니다.

```sh
source .venv/bin/activate
export PATH="$PWD/.tools/bin:$PATH"
export SAM_CLI_TELEMETRY=0
python --version
sam --version
aws --version
```

새 컴퓨터에서 저장소를 복제했다면 Python 3.13, AWS CLI v2를 준비하고 가상환경을 만든 뒤 `python -m pip install -r requirements-dev.txt`로 SAM CLI를 설치합니다. Git에 제외된 `.venv`와 `.tools`는 저장소 복제만으로 생기지 않습니다.

## 2. AWS 인증 및 로컬 검증

프로파일의 단기 인증이 만료됐으면 브라우저 로그인을 다시 진행합니다. 기존 자격증명이 유효하면 로그인 단계를 생략할 수 있습니다.

```sh
aws login --profile cloudmate --region ap-northeast-2
export AWS_PROFILE=cloudmate
python -m unittest discover -s backend/tests -v
sam validate --lint --template-file infrastructure/template.yaml --region ap-northeast-2
sam build
```

AWS 키를 만들거나 소스에 입력할 필요가 없습니다. 로그인은 동일 프로젝트를 배포할 AWS 계정으로 완료합니다.

## 3. 새 AWS 환경 생성

```sh
sam deploy
```

`samconfig.toml`에 저장된 `cloudmate` 스택과 서울 리전 설정을 사용합니다. 삭제된 스택을 새로 생성하며 문서 버킷, 함수, HTTP API, 최소 권한 역할, 로그 그룹과 SAM 패키지 버킷을 준비합니다. 변경 세트를 검토한 뒤 실행합니다. 예전 리소스를 가져오는 작업은 필요하지 않습니다.

## 4. 새 API 주소 확인

이전 API 주소는 종료됐습니다. 새 배포의 출력값을 조회하며, 과거 주소를 다시 사용하지 않습니다.

```sh
CLOUDMATE_HEALTH_URL="$(aws cloudformation describe-stacks --stack-name cloudmate --region ap-northeast-2 --query 'Stacks[0].Outputs[?OutputKey==`HealthApiUrl`].OutputValue | [0]' --output text)"
curl -i "$CLOUDMATE_HEALTH_URL"
python scripts/verify_api.py "$CLOUDMATE_HEALTH_URL"
```

macOS Python에서 CA 인증서 오류가 나면 `export SSL_CERT_FILE="$(python -m certifi)"`를 지정한 후 검증합니다. 정상 결과는 HTTP 200과 status, service, message의 세 필드입니다.

## 5. FAQ 다시 업로드

S3에 보관했던 FAQ는 로컬 및 GitHub의 `data/aws-faq.txt`에서 복원할 수 있습니다.

```sh
CLOUDMATE_BUCKET="$(aws cloudformation describe-stacks --stack-name cloudmate --region ap-northeast-2 --query 'Stacks[0].Outputs[?OutputKey==`DocumentsBucketName`].OutputValue | [0]' --output text)"
aws s3 cp data/aws-faq.txt "s3://$CLOUDMATE_BUCKET/documents/aws-faq.txt" --content-type 'text/plain; charset=utf-8' --region ap-northeast-2
aws s3api head-object --bucket "$CLOUDMATE_BUCKET" --key documents/aws-faq.txt --region ap-northeast-2
```

새 API를 호출하면 새 CloudWatch 로그 스트림이 만들어집니다. 과거 제출용 실행 증거와 삭제 직전 로그 백업은 `docs/evidence/`에 남아 있으며, 새 검증 결과와 구분합니다. 새 API URL은 README와 후속 보고서에 갱신합니다.
