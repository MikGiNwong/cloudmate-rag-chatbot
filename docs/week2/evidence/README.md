# 2주차 증거 목록과 촬영 안내

실제로 실행한 명령의 결과만 보관한다. 로컬 함수 호출, HTTP 모의 테스트, 실제 AWS HTTP 호출은 서로 구분한다. `api_http.json`은 배포된 URL로 검증한 뒤에만 생성한다. 아직 없는 클라우드 증거를 예시 출력으로 대체하지 않는다.

| 파일 | 증거 내용 |
|---|---|
| environment_versions.txt | OS·CPU·개발 도구 버전과 인증 상태 요약 |
| unit_tests.txt | 단위 테스트 실제 출력과 종료 코드 |
| syntax_check.txt | Python 컴파일 실제 결과 |
| sam_validation.txt | SAM/cfn-lint 실제 검증 결과 |
| sam_build.txt | SAM 빌드 실제 결과 |
| local_handler.json | Lambda 핸들러 직접 호출 결과, AWS/HTTP 실행 아님 |
| aws_preflight.json | 연결 도구로 확인한 STS와 배포 이름 충돌 상태, 식별자 제거 |
| git_status.txt | 로컬 저장소와 원본 문서 제외 확인 결과 |
| 최초_커밋.txt | 첫 구현 커밋 해시와 제목, 후속 문서 커밋보다 앞선 기록 |
| aws_cli_auth.json | 승인된 CLI 단기 로그인 후 STS 성공 및 사전 확인 계정 일치 |
| sam_changeset.txt | 실제 SAM 패키지 저장소·변경 세트 생성 출력 |
| changeset_review.json | Add 7개, 서버 측 사전 검증·실행 역할 검토 |
| cloudformation_stack.json | 실제 스택 CREATE_COMPLETE와 출력 |
| api_http.json | 실제 HTTPS API의 HTTP 200·Content-Type·JSON 계약 일치 |
| s3_transfer.json | 실제 FAQ PUT/GET 200, 원본/다운로드 크기·SHA-256 일치 |
| aws_resource_verification.json | 실제 리소스 상태·S3 보안·IAM 정책·API 연결·로그 |
| lambda_code_verification.json | 실제 Lambda ZIP 해시 및 app.py 원본 일치 |
| cloudwatch_logs.txt | 실제 호출의 CloudWatch 로그 출력 |
| github_remote.json | 비공개 저장소·기본 main·배포 기록 커밋의 로컬/원격 해시 일치 |

사용자 승인 후 실제 클라우드 배포·HTTP 200·S3 저장·Lambda 코드 일치·CloudWatch 로그 확인과 비공개 GitHub 생성·푸시까지 완료했다. 배포 결과 커밋 `86fc9fe`의 로컬/원격 일치를 확인했고 이 확인 증거는 후속 문서 커밋에 포함한다. 계정 ID, 사용자 ARN의 식별 부분, 이름·학번·이메일·절대 경로·토큰은 제거한다. 원본은 `raw/`, 콘솔 이미지는 `screenshots/`에 두면 Git에서 제외된다. 공개할 자료는 검토한 익명화 텍스트만 추가한다. 임시 인증 URL과 인증 코드는 커밋하지 않는다.

## 사용자가 직접 촬영할 콘솔 화면

콘솔 화면을 캡처하지 않았으며 대체 이미지를 생성하지 않았다. 아래 화면은 실제 배포 성공 후 서울 리전에서 촬영한다. 계정 메뉴, ARN의 계정 부분과 원본 문서의 개인정보는 가리거나 잘라낸다.

| 화면 | 이동 경로와 촬영 내용 |
|---|---|
| CloudFormation | Stacks → cloudmate-week2 → Events/Resources/Outputs. 완료 상태와 생성 리소스 |
| S3 | Buckets → 문서 버킷 → Permissions/Properties. 퍼블릭 차단·암호화·버전 관리 |
| S3 문서 | 버킷 → documents/ → aws-faq.txt. 객체 키·크기와 파일 내용 |
| Lambda | Functions → cloudmate-health-check → Code/Configuration. 함수 코드·Python 3.13·arm64·트리거 |
| API Gateway | HTTP API → Routes → GET /health → Integrations, Stages. Lambda 통합·URL·스로틀링 |
| 실제 HTTP | 실제 URL을 브라우저 또는 터미널로 호출. HTTP 상태는 CLI 검증 결과도 함께 제출 |
| CloudWatch | Logs → Log groups → /aws/lambda/cloudmate-health-check → 최신 스트림. START/END/REPORT와 health_check 로그 |
| GitHub | 생성된 저장소의 Code와 Commits. 저장소 주소·프로젝트 구조·커밋 |

현재 결과와 미검증 항목은 상위 `environment_report.md`를 기준으로 한다.
