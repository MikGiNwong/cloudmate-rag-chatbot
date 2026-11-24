# 2주차 AWS 구성

`template.yaml`은 1주차 설계 중 원본 문서 저장과 HTTP API 실행 경로만 선언한다. 배포 리전은 `ap-northeast-2`, 설정 파일은 루트 `samconfig.toml`이다.

| 논리 리소스 | 실제 구성과 목적 |
|---|---|
| DocumentsBucket | `cloudmate-docs-<AWS_ACCOUNT_ID>-ap-northeast-2`, 향후 원본 데이터의 `documents/` 접두사 |
| HealthLogGroup | `/aws/lambda/cloudmate-health-check`, 7일 보존 |
| HealthExecutionRole | Lambda 서비스 신뢰, 위 로그 그룹에 스트림 생성·이벤트 쓰기만 허용 |
| HealthHttpApi | 공개 `GET /health`, `$default` 스테이지, 초당 2건·버스트 5건 |
| HealthFunction | `cloudmate-health-check`, Python 3.13/arm64, 128 MB, 3초 제한 |

SAM 변환으로 API 기본 스테이지와 Lambda 호출 허용 리소스가 추가된다. 라우트와 Lambda 프록시 통합은 API 정의에 포함된다. 실행 역할에는 S3·Bedrock 권한과 관리자 관리형 정책을 부여하지 않는다. 로그 그룹 ARN에 포함되는 `:*`는 해당 그룹 안의 로그 스트림을 가리키며 전체 계정 리소스 접근이 아니다.

버킷은 네 가지 퍼블릭 차단 설정을 전부 켜고, SSE-S3 AES256 기본 암호화, BucketOwnerEnforced(ACL 비활성화), 버전 관리를 적용한다. 원본 버킷과 로그 그룹은 삭제·교체 시 보존한다. Knowledge Bases 연동용 역할이나 벡터 인덱스는 이번 주 만들지 않는다.

함수 이름은 과제 지정값을 그대로 사용했다. 따라서 계정·리전당 이 이름으로 하나만 배포할 수 있다. 버킷은 계정·리전 조합으로 고유화했다. 같은 이름의 기존 리소스가 있으면 이 스택에서 임의 수정·삭제하지 않는다.

## 검증과 배포

루트에서 가상환경을 활성화한 뒤 실행한다.

```sh
sam validate --lint --template-file infrastructure/template.yaml --region ap-northeast-2
sam build
# 리소스와 비용 설명 후 사용자 배포 승인을 받아 실행
sam deploy
```

`sam validate --lint`는 cfn-lint를 이용한 템플릿·스키마 검증이다. 별도 cfn-guard 실행과 AWS 변경 세트의 서버 측 사전 검증은 실행 여부를 보고서에 구분한다. 로컬 성공은 AWS 배포 성공을 뜻하지 않는다.

SAM은 코드 ZIP 업로드를 위해 별도 관리 스택 `aws-sam-cli-managed-default`와 패키지 버킷을 생성할 수 있다. 이 부가 S3 저장/요청 비용도 배포 승인 범위에 포함해야 한다. 이후 동일 설정으로 재배포하려면 루트 설정 파일을 사용하고, 패키지 버킷 공유 상태를 먼저 확인한다.

배포 주체에는 스택 수명주기 관리, 버킷 보안·암호화·버전 설정, 함수/HTTP API/로그 그룹 생성·태깅, IAM 역할/인라인 정책 관리와 해당 역할을 Lambda에 전달할 권한이 필요하다. 광범위 관리자 정책을 자동 부여하지 않는다. 연결 계정의 STS 읽기 권한만 확인한 상태에서는 생성 권한을 확정할 수 없다.

출력은 `HealthApiUrl`, `DocumentsBucketName`, `DocumentsPrefix`, `HealthFunctionName`, `HealthLogGroupName`이다. 버킷명과 ARN에는 계정 ID가 포함될 수 있으므로 그대로 공개하지 않는다. 정리는 루트 README의 보존 정책과 별도 삭제 승인 절차를 따른다.
