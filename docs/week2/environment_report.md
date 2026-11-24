# CloudMate 2주차 AWS 및 개발 환경 구성 보고서 초안

작성일: 2026-11-25 (Asia/Seoul)

현재 결과는 **로컬 구현·단위 테스트·SAM 검증·빌드 완료, AWS 실제 배포와 GitHub 원격 변경은 승인 대기**다. 실제 배포 API 주소와 HTTP 실행 결과는 아직 없다. 연결 도구의 읽기 인증과 로컬 CLI 인증을 구분했으며, 수행하지 않은 배포·업로드를 성공으로 기록하지 않았다.

## 1. 실습 목적

- 수행: 1주차 설계를 바탕으로 Python 상태 API, AWS 인프라 코드, 문서 데이터와 개발·검증 절차를 준비했다.
- 이유: 이후 RAG 개발 전에 실행 환경과 배포 경로를 검증할 수 있는 작은 기반이 필요하다.
- 실제 결과: 프로젝트 파일과 로컬 실행 증거를 생성했다. AWS 리소스 생성·모델 호출·원격 저장소 생성·푸시는 실행하지 않았다. 도구 설치는 사용자 승인 후 수행했다.

## 2. 1주차 설계와 2주차 구현 범위

- 수행: `docs/week1/`의 원본 DOCX에서 본문, AWS 서비스 구성표, 포함된 아키텍처 JPEG를 추출하고 이미지를 직접 확인했다. 개인정보를 제외한 [설계 요약](../week1/design_summary.md)을 작성했다.
- 이유: 서비스 목적, 데이터 처리 흐름과 선정 기술을 유지하기 위해서다.
- 실제 결과: AWS 학습자 대상 서비스이며, 데이터 준비는 S3 → Knowledge Bases 추출·분할 → Titan V2 임베딩 → S3 Vectors, 질문 처리는 React/Amplify → API Gateway → Lambda → 문서 검색·근거 검증 → Claude Sonnet → 답변·출처 표시임을 확인했다. 아키텍처 이미지는 구성 요소 추출 → JSON/그래프 → AWS 아이콘 뷰어도 포함한다.

이번 주 구현은 비공개 S3 원본 저장소의 선언과 `GET /health`다. 검색·임베딩·추론·실습 절차 생성·아키텍처 시각화·프론트엔드 호스팅은 구현하지 않았다. CloudTrail은 원래 설계의 감사 서비스로 유지하되 새 Trail을 만들지 않았다. 원본 DOCX는 로컬에서 보존하며 Git에서 제외했다.

## 3. 개발 환경 및 도구

- 수행: OS·CPU·버전·Git 상태·도구 존재 여부·인증 상태를 확인하고 `.venv`와 프로젝트 내부 `.tools`를 구성했다.
- 이유: Python 3.13 및 Apple Silicon 빌드 호환성을 확인하고 시스템 Python 변경을 피하기 위해서다.
- 실제 결과:

| 항목 | 실제 확인 결과 |
|---|---|
| OS / CPU | macOS 27.2.1 / arm64 |
| 프로젝트 Python | 3.13.17 |
| Git | 2.54.0 (Apple Git-157) |
| 초기 Git 상태 | 저장소와 원격 연결 없음. 기존 원본 DOCX 및 Finder 메타데이터 보존 |
| AWS CLI | 초기 미설치 → 승인 후 공식 서명 검증 설치, 2.42.2 |
| SAM CLI | 초기 미설치 → `.venv`에 설치, 1.174.0 |
| cfn-lint | SAM 의존성으로 설치, 1.58.0 |
| GitHub CLI | 초기 미설치 → 공식 arm64 ZIP과 SHA-256 검증 설치, 2.105.0 |
| VS Code | 앱 설치 확인. `code` 명령은 PATH에 없음 |
| Docker | 미설치. 외부 런타임 패키지 없는 이번 SAM 빌드는 성공 |
| AWS 연결 도구 | STS GetCallerIdentity 성공. 계정·사용자 ARN은 제외 |
| 로컬 AWS CLI | STS 실행, 종료 253 / NoCredentials. 플러그인 인증이 로컬로 전달되지 않음 |
| GitHub 연결 도구 | 인증된 프로필 조회 성공. 이메일·식별 정보는 제외 |
| 로컬 GitHub CLI | `gh auth status` 종료 1 / 로그인 필요 |

AWS CLI 배포본에 포함된 Python 버전은 CLI 자체의 내부 런타임이며, Lambda 및 개발용 Python 3.13과 별개다. `requirements-dev.txt`에 검증한 SAM 버전을 고정했다. [버전 및 인증 요약](evidence/environment_versions.txt)에 익명화 결과를 저장했다.

로컬 AWS 로그인에는 AWS CLI 2.32.0 이상에서 지원하는 `aws login`의 단기 자격증명을 사용할 수 있다. 실제 로그인 명령은 별도 확인 후 실행할 예정이며 키 생성·입력을 요청하지 않았다. [AWS CLI 설치](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), [CLI 로그인](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html), [SAM 가상환경 설치](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/manage-sam-cli-versions.html)를 참고했다.

## 4. AWS 리소스 구성

- 수행: `infrastructure/template.yaml`과 `samconfig.toml`을 작성하고 연결된 AWS 계정에서 예정 리소스 이름의 존재 여부를 읽기 전용으로 확인했다.
- 이유: 이후 배포를 재현하고 기존 리소스와의 충돌을 예방하기 위해서다.
- 실제 결과: 템플릿과 빌드는 검증됐다. 조회 시점에 예정된 Lambda 함수, 문서 버킷, 정확히 일치하는 로그 그룹, `cloudmate-week2`와 SAM 관리 스택은 존재하지 않았다. 생성 권한은 아직 검증하지 않았다.

| 배포 예정 리소스 | 설정 | 현재 상태 |
|---|---|---|
| S3 문서 버킷 | `cloudmate-docs-<AWS_ACCOUNT_ID>-ap-northeast-2`, `documents/` 접두사 | 미생성 |
| Lambda | `cloudmate-health-check`, Python 3.13/arm64, 128 MB, 3초 | 미배포 |
| IAM 역할 | Lambda 신뢰, 지정 로그 그룹 쓰기 전용 | 미생성 |
| CloudWatch 로그 그룹 | `/aws/lambda/cloudmate-health-check`, 7일 보존 | 미생성 |
| HTTP API | `GET /health`, Lambda payload 2.0, 기본 스테이지 | 미생성 |
| SAM 생성 부가 리소스 | 기본 스테이지, API Gateway의 Lambda 호출 허용, API 내부 라우트·통합 | 미생성 |
| SAM 패키지 저장소 | 새 SAM 관리 스택·S3 버킷·버킷 정책 | 미생성 |

함수 이름은 과제의 지정값이라 고정했다. 같은 계정·리전에 중복 배포할 수 없으며, 재개 시 존재 여부를 다시 확인한다. [AWS 사전 조회 증거](evidence/aws_preflight.json)는 계정·ARN을 제거했다.

## 5. IAM 및 S3 보안 설정

- 수행: S3 퍼블릭 차단 4개 항목, AES256 기본 암호화, BucketOwnerEnforced, 버전 관리, 보존 정책을 선언했다. Lambda 역할은 `logs:CreateLogStream`, `logs:PutLogEvents`만 전용 로그 그룹 ARN에 허용했다.
- 이유: 문서 공개와 불필요한 서비스 접근을 막고 원본과 실행 증거를 보존하기 위해서다.
- 실제 결과: 템플릿 검증은 성공했다. 클라우드에 적용됐는지는 배포 후 확인해야 한다. S3·Bedrock 호출 권한, 관리자 정책, VPC·네트워크 리소스를 추가하지 않았다. 실행 로그에는 이벤트 본문·토큰·예외 상세를 남기지 않는다.

SAM 1.174.0의 로컬 bootstrap 코드를 확인한 결과, SAM이 자동 준비하는 **패키지 버킷은 문서 버킷과 별개**이며 퍼블릭 차단·SSE-KMS 기본 암호화·버전 관리와 버킷 정책을 사용한다. 새 고객 관리 KMS 키를 직접 선언하지는 않지만 패키지 처리의 KMS 요청 과금 가능성도 고려한다. 배포 전 생성 리소스 설명에 포함한다.

## 6. Lambda 테스트 API 구현

- 수행: `backend/health/app.py`에 독립 응답 생성 함수와 Lambda 핸들러를 구현했다. JSON Content-Type, 프록시 응답 형식, 400/404/405/500 응답과 민감 정보 없는 고정 로그를 적용했다.
- 이유: 실제 AWS 서비스 호출 없이 실행 환경을 검증하고 후속 기능을 별도 경로로 확장하기 위해서다.
- 실제 결과: 응답 계약과 예외·로그 테스트를 통과했다. [직접 핸들러 호출 증거](evidence/local_handler.json)는 로컬 결과이며 실제 AWS 또는 HTTP 응답이 아니다.

아래는 구현한 정상 응답 계약이다.

```json
{
  "status": "ok",
  "service": "CloudMate",
  "message": "AWS Lambda is working",
  "week": 2
}
```

## 7. API Gateway 배포 및 실행 결과

- 수행: HTTP API에 `GET /health`, Lambda 프록시 payload 2.0, 초당 2건·버스트 5건의 기본 스로틀링과 HTTPS URL 출력을 선언했다. 실제 HTTP 상태·Content-Type·JSON을 함께 확인하는 `scripts/verify_api.py`를 작성했다.
- 이유: 테스트 경로를 작게 유지하고 실제 HTTP 검증과 실패 시 종료 코드 1을 제공하기 위해서다.
- 실제 결과: **배포 승인 대기이며 API 주소는 아직 없다. 실제 HTTP 200을 확인하지 않았다.** 검증기의 URL·응답·네트워크 실패 처리는 로컬 단위 테스트로 확인했다. 배포 후 실제 출력 URL을 전달해 `evidence/api_http.json`을 생성해야 한다.

스로틀링은 최선 노력 방식이며 과금 상한은 아니다. 현재 인증 없는 경로는 공개 상태 확인 용도이며, 후속 챗봇의 인증 정책은 별도 설계가 필요하다.

## 8. S3 업로드 검증

- 수행: `data/aws-faq.txt`에 IAM·EC2·S3·Lambda FAQ 7개를 직접 작성했다. 문항 ID, 서비스명, 질문·답변, 출처 제목·URL을 포함하고 공식 서비스 개념 문서를 확인했다.
- 이유: 이후 Knowledge Bases에 넣을 수 있는 작은 한국어 문서를 준비하기 위해서다.
- 실제 결과: 로컬 파일 준비 완료. **버킷 미생성으로 `documents/aws-faq.txt` 업로드·저장 검증은 미실행**이다. 배포 승인 후 새 버킷에 업로드하고 HeadObject의 객체 크기·Content-Type·암호화와 원본 내용 일치를 검증한다.

## 9. CloudWatch 로그 확인

- 수행: 함수 로그 그룹과 7일 보존, 함수 실행 시 `health_check status=ok week=2` 로그를 선언·구현했다. 로그에 민감 입력이 들어가지 않는지 단위 테스트했다.
- 이유: 실제 배포 호출의 운영 증거를 확보하되 불필요한 데이터와 장기 보관을 줄이기 위해서다.
- 실제 결과: 로컬 로그 테스트 성공. **CloudWatch 실제 호출 로그는 아직 없다.** 배포 API 호출 후 로그 스트림의 START/END/REPORT 및 애플리케이션 로그를 확인하고 익명화한 증거를 추가한다.

## 10. Git 및 GitHub 저장소

- 수행: 빈 프로젝트에 `main` 로컬 Git 저장소를 초기화하고 `.gitignore`로 인증 파일·가상환경·빌드·도구·원본 DOCX·비공개 제출 자료를 제외했다. 공개 가능한 텍스트 증거와 구현 파일을 검토한다.
- 이유: 원본 개인정보를 공개하지 않고 코드 및 IaC 변경을 추적하기 위해서다.
- 실제 결과: 로컬 저장소 초기화 및 최초 구현 커밋 `1fe7d84` 완료. 전체 해시와 제목은 `evidence/최초_커밋.txt`에 기록했다. 이 보고서의 커밋 기록 보완은 이후 문서 커밋에 포함된다. GitHub 원격 URL은 **미설정**이다. 연결된 계정에서 기본 저장소 이름을 조회했으나 404가 반환되어 접근 가능한 기존 저장소를 확인하지 못했다. 이는 다른 비공개 저장소의 부재까지 보장하지 않는다.

GitHub 공개 여부와 원격 생성·푸시는 승인 대기다. 기본 저장소 이름은 `cloudmate-rag-chatbot`이다. CLI 로그인 후 공개 범위 확인 및 원격 작업 승인을 반영한다.

## 11. 문제 및 해결 과정

| 문제 | 원인 | 처리와 실제 결과 |
|---|---|---|
| Git 상태 확인 실패 | 초기 `.git` 없음 | 기존 원본을 보존하고 main 저장소 초기화 |
| AWS/SAM/GitHub CLI 없음 | 초기 설치되지 않음 | 사용자 설치 승인 후 프로젝트 내부 설치 완료 |
| 패키지 다운로드 DNS 실패 | 실행 샌드박스 네트워크 제한 | 도구 실행 권한 확인 후 공식 배포처 다운로드 성공 |
| SAM 전역 메타데이터 쓰기 경고 | 홈 디렉터리 쓰기 제한 | 권한 확인 후 검증·빌드 재실행, 종료 0 및 경고 없는 증거 확보 |
| `.git` 초기화 쓰기 제한 | 보호된 Git 메타데이터 경로 | 권한 확인 후 초기화 성공 |
| AWS 사전 조회 스크립트 첫 시도 거부 | 연결 도구가 `getattr()`를 차단 | 예외의 명시적 속성 접근으로 수정, 읽기 조회 완료 |
| 예정 리소스 조회 Not Found | 아직 배포하지 않음 | 예상 결과로 기록. 기존 리소스를 수정하지 않음 |
| 로컬 AWS CLI NoCredentials | 플러그인과 CLI 로그인 별개 | 단기 로그인 절차 준비, 실행 확인 대기 |
| gh 로그인 안 됨 | 플러그인과 CLI 로그인 별개 | 원격 변경 승인 후 웹 인증 필요 |

## 12. 최종 결과와 향후 계획

- 수행: 코드·IaC·설계 요약·FAQ·배포/정리 안내·익명화된 증거와 콘솔 촬영 목록을 작성했다.
- 이유: 현재 완료 범위와 실제 클라우드 검증이 필요한 범위를 명확히 남기기 위해서다.
- 실제 결과: 아래 로컬 검증은 성공했다. AWS 배포·GitHub 원격 작업은 명시적 승인 전이므로 완료 항목으로 처리하지 않는다.

| 검증 | 실제 결과 | 근거 |
|---|---|---|
| Python 문법 | 성공, 종료 0 | [syntax_check.txt](evidence/syntax_check.txt) |
| 단위 테스트 | 10개 성공, 종료 0 | [unit_tests.txt](evidence/unit_tests.txt) |
| SAM 검증 | cfn-lint 포함 성공, 종료 0 | [sam_validation.txt](evidence/sam_validation.txt) |
| SAM 빌드 | Python 3.13/arm64 성공, 종료 0 | [sam_build.txt](evidence/sam_build.txt) |
| cfn-guard | 별도 실행하지 않음. 템플릿 보안 설정은 수동 검토 | 템플릿과 본 보고서 5절 |
| 서버 측 변경 세트 사전 검증 | 승인 전 미실행 | AWS 실제 배포 후 추가 |
| 실제 AWS HTTP·S3·로그 | 승인 전 미실행 | 실제 증거 아직 없음 |
| GitHub 원격 저장소 | 공개 범위·생성/푸시 승인 전 | 원격 URL 없음 |

다음 주에는 실제 배포 검증 후 문서 수집·메타데이터 규칙, Knowledge Bases/S3 Vectors, 임베딩, 근거 충분성 기준과 출처 반환, React 화면, 실습 아키텍처 JSON/그래프 및 아이콘 뷰어를 순차 구현한다. 현재 Lambda에 후속 서비스 권한을 미리 추가하지 않았다.

### 비용 영향과 승인 범위

실제 배포는 문서 S3와 SAM 패키지 S3, Lambda 요청/실행, HTTP API 요청, 로그 수집/보관, 패키지 버킷의 KMS 요청 및 해당 데이터 전송 비용을 발생시킬 수 있다. 소량 검증이라도 무료를 보장하지 않으며 계정의 크레딧·무료 사용 조건을 확인해야 한다. 예상 호출은 승인 후 정상 응답 확인용 소수 요청이며 대량·부하 테스트는 수행하지 않는다. 고정 서버·NAT·데이터베이스·생성 모델 호출은 없다.

요금 근거: [API Gateway](https://aws.amazon.com/api-gateway/pricing/), [Lambda](https://aws.amazon.com/lambda/pricing/), [S3](https://aws.amazon.com/s3/pricing/), [CloudWatch](https://aws.amazon.com/cloudwatch/pricing/), [KMS](https://aws.amazon.com/kms/pricing/). 현재 문서는 청구서나 서울 리전의 확정 견적이 아니다. 리소스 삭제는 별도 승인 후 진행하며 S3 버전·보존 로그·패키지 버킷은 스택 삭제 뒤에도 남을 수 있다.

### 최종 검증 체크리스트

- [x] 프로젝트 구조 생성
- [x] 1주차 텍스트·표·이미지 및 설계 일관성 확인
- [x] Python 상태 API 작성
- [x] 단위 테스트 10개 성공
- [x] SAM 템플릿 검증 성공
- [x] SAM 빌드 성공
- [ ] AWS S3 생성 및 테스트 문서 저장
- [ ] Lambda 배포
- [ ] API Gateway 연결
- [ ] 실제 GET /health HTTP 200
- [ ] 실제 CloudWatch 로그
- [ ] GitHub 저장소 및 원격 커밋 확인
- [x] 환경 구성 보고서 초안
- [x] 실제 로컬 증거 및 스크린샷 촬영 목록

실제 콘솔 화면 캡처는 수행하지 않았다. [촬영 안내](evidence/README.md)에 배포 후 촬영할 화면 경로와 익명화 항목을 정리했다. 가짜 콘솔 이미지나 실행 결과를 만들지 않았다.
