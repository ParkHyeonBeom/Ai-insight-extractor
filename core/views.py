# core/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import CrawlRequestSerializer
from .tasks import crawl_and_save_article

class CrawlView(APIView):
    """
    URL과 키워드를 받아 크롤링 Celery 작업을 실행시키는 API 뷰
    """
    def post(self, request, *args, **kwargs):
        # 1. 요청 데이터를 Serializer로 검증
        serializer = CrawlRequestSerializer(data=request.data)
        if serializer.is_valid():
            # 2. 검증된 데이터 추출
            keyword_id = serializer.validated_data['keyword_id']
            url = serializer.validated_data['url']

            # 3. Celery 작업 호출 (.delay() 사용)
            crawl_and_save_article.delay(keyword_id, url)

            # 4. 작업이 큐에 추가되었음을 응답
            # HTTP 202 Accepted: 요청이 접수되었으며, 처리는 비동기로 진행될 것임을 의미
            return Response(
                {"message": "크롤링 작업이 성공적으로 요청되었습니다."},
                status=status.HTTP_202_ACCEPTED
            )

        # 데이터가 유효하지 않을 경우 에러 응답
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)