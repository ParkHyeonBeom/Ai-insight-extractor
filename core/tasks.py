import requests
from bs4 import BeautifulSoup
from celery import shared_task
import ollama # openai 대신 ollama를 임포트 (또는 추가)
from .models import Keyword, Article, Summary  # Topic -> Keyword로 변경

@shared_task
def crawl_and_save_article(keyword_id, article_url): # topic_id -> keyword_id로 변경
    """
    주어진 URL의 웹 페이지를 크롤링하여 기사(Article)로 저장하는 Celery Task.
    """
    try:
        # 1. 해당 키워드 가져오기
        keyword = Keyword.objects.get(id=keyword_id) # Topic -> Keyword로 변경

        # 2. 이미 처리된 URL인지 확인 (중복 방지)
        if Article.objects.filter(url=article_url).exists():
            return f"Skipped: Article from {article_url} already exists."

        # 3. 웹 페이지 요청 및 파싱
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(article_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # 4. 제목과 본문 추출
        title = soup.title.string if soup.title else "No Title"
        paragraphs = soup.find_all('p')
        content = '\n'.join([p.get_text() for p in paragraphs])

        if not content:
            content = "Content could not be extracted."

        # 5. Article 객체 생성 및 저장
        new_article = Article.objects.create(
            keyword=keyword,
            title=title,
            url=article_url,
            content=content,
            published_at='2025-08-16 00:00:00Z'
        )

        # 6. 저장 후, 요약 작업을 바로 호출! (체이닝)
        summarize_article_task.delay(new_article.id)

        return f"Successfully crawled and saved article from {article_url}. Summarization task queued."

    except Keyword.DoesNotExist: # Topic -> Keyword로 변경
        return f"Error: Keyword with id {keyword_id} not found."
    except requests.RequestException as e:
        return f"Error crawling {article_url}: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

@shared_task
def summarize_article_task(article_id):
    """
    주어진 아티클 ID에 해당하는 아티클을 찾아 Ollama로 요약하고 결과를 저장하는 Celery Task.
    """
    try:
        article = Article.objects.get(id=article_id)

        if Summary.objects.filter(article=article).exists():
            return f"Summary for Article {article_id} already exists."

        # Ollama 클라이언트 초기화
        # 이제 Docker 서비스 이름으로 직접 접속합니다.
        # 'localhost' 대신 'host.docker.internal'을 사용해야 합니다.
        client = ollama.Client(host='http://ollama:11434')

        # AI에게 보낼 프롬프트 작성
        prompt_text = f"""
        Please summarize the following article content in Korean, focusing on the key points.
        The summary should be concise and easy to understand.

        Article Content:
        {article.content[:4000]}
        """

        # Ollama API 호출
        response = client.chat(
            model="llama3:8b", # 다운로드한 모델 이름
            messages=[
                {"role": "user", "content": prompt_text}
            ]
        )

        summary_text = response['message']['content']

        # Summary 객체 생성 및 저장
        Summary.objects.create(
            article=article,
            summary_text=summary_text
        )

        return f"Successfully summarized with Ollama and saved for Article ID: {article_id}"

    except Article.DoesNotExist:
        return f"Error: Article with id {article_id} not found."
    except Exception as e:
        return f"An unexpected error occurred during summarization for Article ID {article_id}: {e}"