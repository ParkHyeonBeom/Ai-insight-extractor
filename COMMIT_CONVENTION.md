# Commit Convention

이 프로젝트는 **Conventional Commits** 명세를 따릅니다. 커밋 메시지는 명확하고 일관성 있게 작성하여 변경 이력을 쉽게 추적할 수 있도록 합니다.

---

## 커밋 메시지 구조

커밋 메시지는 아래와 같은 구조를 가집니다.

` <type>: <subject> `

`<body>`

`<footer>`

-   **type**: 커밋의 종류 (필수)
-   **scope**: 커밋의 영향 범위 (선택)
-   **subject**: 50자 이내의 간결한 요약 (필수)
-   **body**: 변경 이유, 상세 내용 (선택)
-   **footer**: 관련된 이슈 번호 (선택)

---

## Type 종류

-   **feat**: 새로운 기능 추가
-   **fix**: 버그 수정
-   **docs**: 문서 수정 (README.md, API 문서 등)
-   **style**: 코드 스타일 변경 (세미콜론 추가, 들여쓰기 수정 등 기능 변경은 없음)
-   **refactor**: 코드 리팩토링 (기능 변경 없이 내부 구조 개선)
-   **test**: 테스트 코드 추가 또는 수정
-   **chore**: 빌드 관련 파일 수정, 패키지 매니저 설정 변경 등 기타 잡다한 작업
-   **ci**: CI/CD 관련 설정 변경
-   **perf**: 성능 개선

---

## 예시

### 제목만 있는 경우

feat: Add user authentication API


### 상세 내용이 있는 경우

fix: Correct password validation logic

비밀번호 최소 길이를 8자에서 10자로 변경

특수문자 포함 요구사항 추가