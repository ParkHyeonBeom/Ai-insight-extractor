# core/tasks.py

import requests
from bs4 import BeautifulSoup
from celery import shared_task
from .models import Keyword, Article # Topic -> Keyword로 변경

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

        # 5. Article 객체 생성 및 저장 (가장 중요한 변경!)
        Article.objects.create(
            keyword=keyword, # topic=topic -> keyword=keyword 로 변경
            title=title,
            url=article_url,
            content=content,
            published_at='2025-08-16 00:00:00Z'  # published_at 필드가 있으므로 임시 값을 넣어줍니다. (나중에 실제 값으로 파싱해야 함)
        )

        return f"Successfully crawled and saved article from {article_url}"

    except Keyword.DoesNotExist: # Topic -> Keyword로 변경
        return f"Error: Keyword with id {keyword_id} not found."
    except requests.RequestException as e:
        return f"Error crawling {article_url}: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"