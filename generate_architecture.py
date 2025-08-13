# generate_architecture.py
from diagrams import Diagram, Cluster
from diagrams.custom import Custom  # OpenAI 로고를 위한 Custom import
from diagrams.aws.network import ELB
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.onprem.queue import Celery
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.client import User
from diagrams.generic.place import Datacenter
from diagrams.onprem.vcs import Github
from diagrams.onprem.ci import GithubActions
from diagrams.programming.framework import Django

with Diagram("AI Insight Extractor - System Architecture", show=False, filename="architecture_logo") as diag:
    user = User("User")

    # 다운로드한 로고 이미지 파일을 사용
    openai_logo = "openai-logo.png"
    llm = Custom("LLM API", openai_logo)

    with Cluster("Cloud Server (AWS/GCP)"):
        with Cluster("CI/CD"):
            actions = GithubActions("GitHub Actions")

        with Cluster("Request Flow"):
            ingress = ELB("Nginx")
            django_app = Django("Django API")

        with Cluster("Async Task Processing"):
            celery = Celery("Celery Worker")
            redis_broker = Redis("Redis Broker")

        with Cluster("Data & AI"):
            db = RDS("PostgreSQL")
            vector_db = S3("Vector DB (Chroma)")
            langchain = Datacenter("LangChain")

    # CI/CD Flow
    github = Github("GitHub Repo") >> actions >> ingress

    # Main Flow
    user >> ingress >> django_app
    django_app >> celery
    celery >> redis_broker
    celery >> langchain

    # RAG Flow
    langchain >> vector_db
    langchain >> llm

    # Data Storage
    celery >> db

diag