# core/serializers.py

from rest_framework import serializers

class CrawlRequestSerializer(serializers.Serializer):
    """
    크롤링 요청 API의 입력 데이터를 검증하기 위한 Serializer
    """
    keyword_id = serializers.IntegerField(
        help_text="크롤링할 주제의 키워드 ID"
    )
    url = serializers.URLField(
        help_text="크롤링할 기사의 URL"
    )