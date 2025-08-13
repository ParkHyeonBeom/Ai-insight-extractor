# AI Insight Extractor

AI를 활용하여 웹 콘텐츠를 분석하고, RAG(Retrieval-Augmented Generation) 기술을 통해 깊이 있는 인사이트를 도출한 후, 결과를 요약하여 이메일 초안을 생성하는 프로젝트입니다.

## 🌟 주요 기능

-   URL 또는 텍스트 입력을 통한 콘텐츠 분석
-   LangChain 및 LLM(GPT, Gemini 등)을 활용한 내용 요약 및 인사이트 생성
-   VectorDB를 사용한 RAG 파이프라인 구축
-   분석 결과를 기반으로 한 이메일 초안 자동 작성
-   Celery를 이용한 비동기 처리

## 🛠️ 기술 스택

-   **Backend:** Python, Django, Django Rest Framework
-   **AI/LLM:** LangChain, OpenAI API, ChromaDB
-   **Async Task:** Celery, Redis
-   **Database:** PostgreSQL
-   **Infrastructure:** Docker, Nginx
-   **CI/CD:** GitHub Actions

## 🏗️ 시스템 아키텍처

```mermaid
graph TD
    A[👨‍💻 User] -- 1.URL/Text 입력 --> B{Django REST API};
    B -- 2.분석 요청 (Async) --> C[Celery Worker];
    C -- 3.콘텐츠 스크래핑/처리 --> D[Text Processing];
    D -- 4.텍스트 분할 --> E[Chunking];
    E -- 5.텍스트 임베딩 --> F[Embedding Model];
    F -- 6.벡터 저장 --> G[(Vector DB: Chroma)];
    subgraph RAG Pipeline
        C -- 7.요약/인사이트 생성 요청 --> H{LangChain};
        H -- 8.유사도 높은 정보 검색 --> G;
        H -- 9.정보 + 프롬프트 조합 --> I[LLM API];
        I -- 10.생성된 결과 반환 --> H;
    end
    H -- 11.최종 결과 --> C;
    C -- 12.결과 DB 저장 --> J[(PostgreSQL)];
    C -- 13.이메일 초안 생성 --> K[📧 Email Service];
    B -- 즉시 응답 (작업 접수) --> A;
    J -- 결과 조회 API --> B;