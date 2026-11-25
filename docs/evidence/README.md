# CloudMate 현재 환경 실행 증거

2026-11-25 과제 제출 후 CloudMate AWS 환경을 삭제했습니다. 이 폴더의 실행 검증은 제출 당시의 기록이며 현재 API는 종료됐습니다.

이 폴더는 텀프로젝트용 `cloudmate` 스택으로 이름을 정리한 이후의 검증 결과를 보관합니다. `docs/week2/evidence/`는 최초 구성 당시의 기록이므로 현재 환경과 구분합니다.

| 파일 | 실제 확인 내용 |
|---|---|
| environment_versions.txt | 개발 도구·OS·CPU 구성 |
| unit_tests.txt | 상태 API와 HTTP 검증기 단위 테스트 10개 성공 |
| syntax_check.txt | Python 문법 검사 성공 |
| sam_validation.txt | 현재 SAM 템플릿과 cfn-lint 검증 성공 |
| sam_build.txt | Python 3.13/arm64 빌드 성공 |
| migration_template_validation.txt | 리소스 보존용 템플릿 검증 성공 |
| stack_import_review.json | 기존 리소스 7개를 가져오는 변경 세트 확인 |
| sam_update_review.json | 실제 이름·태그·코드 변경 범위와 최소 권한 확인 |
| resource_migration.json | 기존 스택 삭제, 물리 ID·API 주소·문서 버전 보존, 주차 이름 제거 |
| retained_resource_cleanup.json | 이전 IAM 역할과 Lambda 호출 권한 삭제 |
| api_http.json | 이전 후 실제 HTTP 200·JSON 응답 검증 |
| s3_document_verification.json | FAQ 실제 다운로드와 원본 바이트·SHA-256 일치 |
| aws_resource_verification.json | 현재 리소스 상태·보안·IAM·API·로그 설정 조회 |
| lambda_code_verification.json | 실제 배포 ZIP 및 app.py 원본 일치 |
| cloudwatch_logs.txt | 이전 후 실제 함수 호출 로그 |
| sam_changeset.txt | 프로젝트 스택의 SAM 배포 출력 |
| cleanup_before.json | 삭제 직전 리소스와 S3 객체 버전 목록 |
| cloudwatch_logs_before_cleanup.txt | 삭제 직전 실제 로그 백업 |
| storage_cleanup.json | 모든 S3 객체 버전·문서 버킷·로그 정리 결과 |
| resource_cleanup.json | CloudMate 삭제 완료 시점의 스택·잔여 리소스 확인 |
| additional_lab_cleanup.json | 추가 승인된 기존 ECS 실습 스택 삭제와 미연결 Elastic IP 반환 |
| final_cleanup_verification.json | CloudMate 및 추가 실습 정리 후 최종 잔여 자원 확인 |

계정 번호·사용자 ARN의 식별 부분·개인 경로·인증 URL과 토큰은 공개 증거에서 제외합니다. 원본 출력과 콘솔 캡처를 보관하는 `raw/`, `screenshots/`는 Git에서 제외합니다. 현재 콘솔 캡처는 직접 수행하지 않았으며 [제출 안내](../submission_guide.md)의 절차에 따라 실제 화면을 첨부할 수 있습니다.
