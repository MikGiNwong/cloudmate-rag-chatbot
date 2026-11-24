# CloudMate 1주차 설계 요약

원본 서비스 기획서 DOCX의 본문, 데이터 종류 표, AWS 서비스 구성표와 포함된 아키텍처 JPEG를 확인했다. 원본의 이름·학번·학교 및 문서 속성은 이 요약에 옮기지 않는다. 원본 DOCX는 로컬 참고용으로 보존하며 Git에서 제외한다.

## 서비스 목적과 대상

AWS 공식 기술 문서, 공개 실습 가이드, 직접 작성한 FAQ를 바탕으로 클라우드 학습자의 질문에 답한다. 대상은 AWS를 처음 배우는 학생, 클라우드 수업 수강생, 실습 중인 개발자다. 답변과 출처를 확인하고 실제 학습과 실습을 이어갈 수 있어야 한다.

## 데이터와 질문 처리 흐름

데이터 준비는 문서 수집 → S3 원본 저장 → Bedrock Knowledge Bases의 텍스트 추출·분할 → Titan Text Embeddings V2 임베딩 → S3 Vectors 인덱스 저장 순서다. 문서 추가·수정 후 데이터 소스를 다시 동기화한다.

질의 처리는 React 화면 → API Gateway → Lambda → Knowledge Bases 검색 → 근거 충분성 확인 → Claude Sonnet 계열 모델의 근거 기반 답변 → 답변·문서 제목·출처 URL 표시 순서다. 근거가 부족하면 임의 답변을 생성하지 않는다.

## 선정 기술

| 역할 | 1주차 선정 기술 | 2주차 범위 |
|---|---|---|
| 웹 화면 | React + Amplify Hosting | 폴더와 개발 범위 문서 |
| 백엔드 | API Gateway + Lambda | HTTP API GET /health, Python 3.13 |
| 원본 문서 저장 | Amazon S3 | 비공개 암호화 버킷 정의 및 FAQ 준비 |
| RAG 검색 관리 | Bedrock Knowledge Bases | 향후 구현 |
| 벡터 검색 | Amazon S3 Vectors | 향후 구현 |
| 임베딩 | Titan Text Embeddings V2 | 향후 구현 |
| 답변 모델 | Bedrock의 Claude Sonnet 계열 | 향후 구현, 모델 버전 확정 안 함 |
| 모니터링 | CloudWatch | 함수 로그, 7일 보존 |
| 권한 | IAM | 함수 전용 최소 로그 권한 |
| 관리 작업 감사 | CloudTrail | 후속 검토, 새 Trail 생성 안 함 |

## 실습 아키텍처 시각화

원본 이미지는 문서 기반 구성 요소 추출 → Diagram JSON / graph structure → AWS 공식 아이콘을 사용하는 프론트엔드 아키텍처 뷰어 흐름을 보여 준다. 서비스 연결 관계, 구성 요소 역할, 실습 순서를 함께 안내하는 기능이다. 2주차에 이 기능을 구현하거나 다른 기술로 대체하지 않는다.

## 이후 주요 기능

AWS 질문·답변, 근거 문서 및 출처 표시, 등록 가이드에 근거한 단계별 실습 절차, 아키텍처 시각화, 근거 부족 시 답변 제한을 구현한다. 현재 health API는 실행 환경 확인용이며 챗봇 API가 아니다.
