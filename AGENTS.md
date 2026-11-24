# CloudMate 작업 지침

## 프로젝트 목적

AWS 학습자에게 공식 문서에 근거한 답변과 출처, 실습 절차, AWS 아이콘 기반 아키텍처를 제공하는 RAG 챗봇이다. `docs/week1/design_summary.md`를 설계 기준으로 삼는다. 2주차 구현은 S3 문서 저장소와 공개 읽기 전용 `GET /health`로 한정한다.

## 코드 작성

- Python 3.13과 표준 라이브러리를 우선 사용한다. Lambda 런타임 의존성과 개발 도구 의존성을 분리한다.
- 함수는 작게 작성하고 응답 생성 로직을 핸들러에서 분리한다. 오류 응답에는 내부 예외나 식별 정보를 넣지 않는다.
- `infrastructure/template.yaml`로 리소스를 관리한다. 기존 사용자 파일과 AWS 리소스를 보존한다.
- 프론트엔드, RAG 검색, 임베딩, 모델 호출, 시각화는 후속 주차 범위다. 빈 구현이나 가짜 성공 결과를 만들지 않는다.
- 문서와 보고서는 한국어로 쓰고, 수행 내용·목적·실제 결과를 구분한다.

## 테스트

- `python -m unittest discover -s backend/tests -v`를 실행한다.
- 응답 계약, 잘못된 경로·메서드, 예외 처리, 로그의 민감 정보 누락을 검증한다.
- 인프라 변경 시 `sam validate --lint --template-file infrastructure/template.yaml --region ap-northeast-2`와 `sam build --template-file infrastructure/template.yaml`을 실행한다.
- AWS 호출과 로컬 모의 실행을 구분한다. 실제 엔드포인트 검증은 `scripts/verify_api.py`로 수행한다.
- 실행하지 않았거나 승인 대기인 항목은 미검증으로 기록한다.

## AWS 보안과 승인

- 리전은 `ap-northeast-2`다. AWS 리소스 생성·비용 발생 작업과 GitHub 원격 생성·푸시는 변경 및 비용 설명 후 사용자 승인을 받는다.
- 도구 설치도 사용자 승인 후 수행한다. 기존 승인 범위를 반복해서 묻지 않는다.
- S3 퍼블릭 액세스를 전부 차단하고 기본 암호화와 BucketOwnerEnforced를 유지한다.
- Lambda 실행 역할은 지정 로그 그룹의 CreateLogStream·PutLogEvents만 허용한다. S3/Bedrock 권한을 미리 주지 않는다.
- 액세스 키나 비밀번호를 생성·출력·커밋하지 않는다. 단기 로그인과 기존 연결을 우선 사용한다.
- 계정 ID, 사용자 ARN, 학번·이름·이메일·로컬 절대 경로와 원본 DOCX를 공개 자료에서 제외한다.
- S3와 로그의 보존 정책을 설명하고, 생성한 리소스도 별도 삭제 승인 없이 정리하지 않는다.
- NAT Gateway, EC2, RDS, OpenSearch, Knowledge Bases, S3 Vectors 및 생성 모델 호출은 이번 주에 사용하지 않는다.
