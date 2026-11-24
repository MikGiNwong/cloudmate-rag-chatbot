# CloudMate RAG Chatbot

CloudMate는 AWS 공식 문서와 실습 가이드, 직접 작성한 FAQ를 근거로 AWS 학습자의 질문에 답하는 RAG 챗봇 프로젝트다. 답변의 출처와 실습 절차를 제공하고, 이후 AWS 공식 아이콘을 사용하는 실습 아키텍처 시각화를 구현한다.

2주차는 비공개 원본 문서 저장소와 `GET /health` 테스트 API를 준비하는 단계다. **로컬 구현과 AWS 실제 배포 결과는 [환경 보고서](docs/week2/environment_report.md)에서 구분한다.** 원본 1주차 DOCX는 로컬에만 보존한다.

## 사용 기술

Python 3.13 · Lambda arm64 · API Gateway HTTP API · S3 · SAM/CloudFormation · IAM · CloudWatch · Git/GitHub · VS Code/Codex를 사용한다. 리전은 서울 `ap-northeast-2`다. 후속 기술은 React/Amplify Hosting, Bedrock Knowledge Bases, S3 Vectors, Titan Text Embeddings V2, Claude Sonnet 계열이다.

## 디렉터리 구조

```text
backend/health/          Lambda 코드와 런타임 의존성
backend/tests/           표준 unittest 기반 계약·오류 처리 테스트
frontend/README.md      React/Amplify 후속 범위
data/aws-faq.txt         출처가 있는 자체 작성 FAQ
infrastructure/          SAM 템플릿과 리소스·검증 설명
docs/week1/              로컬 원본 DOCX와 공개 가능한 설계 요약
docs/week2/              한국어 보고서와 익명화된 실행 증거
scripts/verify_api.py    실제 HTTP 응답 검증과 JSON 증거 저장
samconfig.toml           서울 리전·스택·빌드·변경 세트 확인 설정
requirements-dev.txt     검증된 SAM CLI 버전
AGENTS.md               코드·테스트·보안 작업 지침
```

## 개발 환경과 로컬 테스트

Python 3.13이 필요하다. 설치된 도구는 프로젝트 내부 `.venv`, `.tools`에 있고 Git에서 제외한다. 새 환경에서 도구를 설치할 때에는 사용자 승인을 먼저 받는다.

```sh
python3.13 -m venv .venv
source .venv/bin/activate
# 새 환경에서 승인 후 실행
python -m pip install -r requirements-dev.txt
export PATH="$PWD/.tools/bin:$PATH"
export SAM_CLI_TELEMETRY=0
python -m compileall -q backend scripts
python -m unittest discover -s backend/tests -v
sam validate --lint --template-file infrastructure/template.yaml --region ap-northeast-2
sam build
```

Lambda 코드는 외부 패키지가 없어 Docker 없이 빌드할 수 있다. `sam local`의 Lambda 에뮬레이션은 Docker가 필요하지만 이번 주 필수 검증에는 포함하지 않는다. `.venv`의 인터프리터를 VS Code에서 선택하면 된다. `code` 명령이 PATH에 없어도 설치된 VS Code 앱으로 폴더를 열 수 있다.

## AWS 배포

**아래 리소스 생성과 FAQ 업로드는 사용자 승인 후에만 실행한다.** 현재 승인·배포 상태는 환경 보고서를 확인한다.

`cloudmate-week2` 스택은 비공개 S3 버킷, 전용 Lambda 로그 그룹, IAM 실행 역할, Lambda 함수, HTTP API와 기본 스테이지, API Gateway 호출 허용 리소스를 생성한다. SAM의 `resolve_s3`는 별도의 `aws-sam-cli-managed-default` 스택과 배포 패키지용 S3 버킷을 생성할 수 있다. 기존 동일 이름 리소스가 있으면 덮어쓰거나 가져오지 말고 소유 관계부터 확인한다.

로컬 CLI의 자격증명은 연결된 AWS 플러그인 인증과 별개다. AWS CLI 2.32.0 이상에서 지원하는 `aws login`을 통한 단기 인증을 사용한다. 로그인 실행도 확인 후 진행하며 키를 채팅이나 저장소에 입력하지 않는다. 조직의 기존 SSO 프로파일이 있으면 그 방식을 유지한다.

```sh
source .venv/bin/activate
export PATH="$PWD/.tools/bin:$PATH"
export SAM_CLI_TELEMETRY=0
# 승인 후 로그인한 로컬 프로파일 사용
export AWS_PROFILE=cloudmate
# 이 명령의 원본 출력에는 계정·ARN이 있으므로 공개 증거에 그대로 저장하지 않는다.
aws sts get-caller-identity --region ap-northeast-2
sam validate --lint --template-file infrastructure/template.yaml --region ap-northeast-2
sam build
sam deploy
```

`samconfig.toml`에는 스택 `cloudmate-week2`, 리전, `CAPABILITY_IAM`, `confirm_changeset=true`, 패키지 버킷 자동 준비 설정을 보존했다. 첫 실행에서 변경 세트의 생성 대상과 기존 리소스 충돌 여부를 검토한다. IAM 역할은 이름을 직접 지정하지 않아 `CAPABILITY_NAMED_IAM`이 필요하지 않다. 배포 권한과 Lambda 실행 권한은 서로 다르다. 배포 주체에는 CloudFormation·S3·Lambda·API Gateway·Logs·IAM 생성/조회 권한과 새 실행 역할로 제한한 `iam:PassRole` 등이 필요하며, STS 인증 성공만으로 배포 권한을 보장하지 않는다.

배포 후 스택 출력의 실제 API 주소로 검증한다.

```sh
aws cloudformation describe-stacks --stack-name cloudmate-week2 --region ap-northeast-2 --query 'Stacks[0].StackStatus' --output text
CLOUDMATE_HEALTH_URL="$(aws cloudformation describe-stacks --stack-name cloudmate-week2 --region ap-northeast-2 --query 'Stacks[0].Outputs[?OutputKey==`HealthApiUrl`].OutputValue | [0]' --output text)"
python scripts/verify_api.py "$CLOUDMATE_HEALTH_URL" --output docs/week2/evidence/api_http.json
CLOUDMATE_BUCKET="$(aws cloudformation describe-stacks --stack-name cloudmate-week2 --region ap-northeast-2 --query 'Stacks[0].Outputs[?OutputKey==`DocumentsBucketName`].OutputValue | [0]' --output text)"
aws s3 cp data/aws-faq.txt "s3://$CLOUDMATE_BUCKET/documents/aws-faq.txt" --content-type 'text/plain; charset=utf-8' --region ap-northeast-2
aws s3api head-object --bucket "$CLOUDMATE_BUCKET" --key documents/aws-faq.txt --region ap-northeast-2
aws logs tail /aws/lambda/cloudmate-health-check --since 10m --region ap-northeast-2
```

정상 응답 계약은 HTTP 200, JSON Content-Type과 다음 본문이다. 아래는 **계약 예시**이며 클라우드 실행 증거가 아니다.

```json
{"status":"ok","service":"CloudMate","message":"AWS Lambda is working","week":2}
```

실제 `head-object` 결과와 로그는 계정 ID, ARN, 개인 경로를 검토·익명화한 뒤 증거 폴더에 저장한다. 공개 API에는 인증을 붙이지 않고 초당 2건·버스트 5건의 기본 스로틀링을 둔다. 스로틀링은 비용 상한을 보장하지 않는다.

## GitHub

로컬 커밋 후 저장소 공개 여부와 원격 생성·푸시 승인을 받는다. 기본 이름은 `cloudmate-rag-chatbot`이다. GitHub 플러그인 연결과 `gh auth`도 별도이므로 CLI 로그인 상태를 확인한다.

```sh
gh auth status
git status --short
# 승인된 공개 범위에 맞춰 --private 또는 --public 중 하나 사용
gh repo create cloudmate-rag-chatbot --private --source=. --remote=origin --push
```

승인이 없으면 위 생성·푸시 명령을 실행하지 않는다. 기존 원격이 있으면 먼저 `git remote -v`로 확인하고 그대로 사용한다. 원본 DOCX, 가상환경, 도구, 인증 정보와 원본 증거는 커밋하지 않는다.

## 비용과 환경 정리

과금 항목은 HTTP API 요청, Lambda 요청·실행 시간, S3 문서·버전·배포 패키지 저장/요청, CloudWatch 로그 수집/보관, 해당되는 데이터 전송이다. SAM 관리 패키지 버킷은 기본적으로 SSE-KMS를 사용하므로 KMS 요청 비용도 발생할 수 있다. 소량 실습을 전제로 하지만 무료 여부는 계정 조건에 따라 다르다. [API Gateway](https://aws.amazon.com/api-gateway/pricing/), [Lambda](https://aws.amazon.com/lambda/pricing/), [S3](https://aws.amazon.com/s3/pricing/), [CloudWatch](https://aws.amazon.com/cloudwatch/pricing/), [KMS](https://aws.amazon.com/kms/pricing/) 요금을 확인한다. NAT Gateway, EC2, RDS, OpenSearch, Bedrock 리소스·추론은 사용하지 않는다.

**정리는 별도 삭제 승인을 받은 후에만 수행한다.** 먼저 스택과 실제 리소스 목록을 확인한다. 보존 정책 때문에 스택 삭제만으로 모든 리소스가 사라지지 않는다.

```sh
# 별도 삭제 승인 후에만 실행
aws cloudformation delete-stack --stack-name cloudmate-week2 --region ap-northeast-2
aws cloudformation wait stack-delete-complete --stack-name cloudmate-week2 --region ap-northeast-2
```

위 삭제 후에도 원본 문서 S3 버킷과 로그 그룹은 `Retain`으로 남는다. 로그 이벤트는 7일 보존 정책에 따라 만료된다. 문서 버킷을 완전히 제거하려면 백업 여부를 확인한 뒤 **모든 객체 버전과 삭제 마커**를 검토·삭제하고 버킷을 삭제해야 한다. `aws s3 rm --recursive`만으로 버전 버킷이 비워지지 않는다. 남은 로그 그룹 삭제와 SAM 관리 패키지 버킷/스택 정리는 별도로 승인받고, 다른 SAM 프로젝트의 사용 여부를 확인한다. 보존된 버킷·로그 이름이 재배포와 충돌하면 기존 것을 임의 삭제하지 않는다.
