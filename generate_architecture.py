# final_architecture_korean.py
from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.queue import Celery
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.client import User
from diagrams.onprem.vcs import Github
from diagrams.onprem.ci import GithubActions
from diagrams.programming.framework import Django

# 다이어그램에 사용할 로고 이미지 URL
openai_logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/OpenAI_Logo.svg/1200px-OpenAI_Logo.svg.png"
# 아래 LangChain 로고 URL을 텍스트가 포함된 버전으로 변경했습니다.
langchain_logo_url = "https://raw.githubusercontent.com/langchain-ai/langchain/master/libs/langchain/langchain/img/langchain-logo-wordmark.png"
chromadb_logo_url = "https://www.trychroma.com/logo.png"

with Diagram("AI 뉴스레터 서비스 - 최종 RAG 아키텍처", show=False, filename="final_architecture_korean") as diag:

    user = User("사용자")

    with Cluster("개발 및 CI/CD"):
        github_repo = Github("GitHub 저장소")
        actions = GithubActions("GitHub Actions")
        github_repo >> Edge(label="코드 Push") >> actions

    with Cluster("클라우드 서버 환경"):
        nginx = Nginx("Nginx (리버스 프록시)")
        actions >> Edge(label="배포") >> nginx

        with Cluster("애플리케이션 계층"):
            django_app = Django("Django API (web)")
            celery_worker = Celery("Celery 워커")
            redis_broker = Redis("Redis (브로커)")

        with Cluster("AI 및 데이터 계층"):
            db = PostgreSQL("PostgreSQL (데이터베이스)")
            vector_db = Custom("벡터 DB (Chroma)", "./다운로드2.png")
            # LangChain 노드가 이제 새로운 로고를 사용합니다.
            langchain = Custom("LangChain 오케스트레이터", "./다운로드.jpeg")
            llm_api = Custom("LLM\n(Ollama)", "./다운로드3.png")

    # --- 전체 시스템 흐름 연결 ---
    user >> nginx >> django_app

    django_app >> Edge(label="크롤링 작업 등록") >> redis_broker
    celery_worker << Edge(label="작업 가져오기") >> redis_broker
    celery_worker >> Edge(label="원본 아티클 저장") >> db
    celery_worker >> Edge(label="LangChain으로 처리") >> langchain

    langchain >> Edge(label="임베딩 생성") >> llm_api
    langchain >> Edge(label="벡터 저장") >> vector_db

    django_app >> Edge(label="사용자 질문 (RAG)", style="dotted", color="darkgreen") >> langchain
    langchain >> Edge(label="유사 문서 검색", style="dotted", color="darkgreen") >> vector_db
    langchain >> Edge(label="문맥 기반 답변 생성", style="dotted", color="darkgreen") >> llm_api

diag