# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

# Django의 기본 User 모델을 확장하여 사용합니다.
# 나중에 프로필 이미지나 추가 정보 필드를 더하기 용이합니다.
class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='이메일')

    # USERNAME_FIELD를 email로 설정하여 이메일로 로그인하도록 합니다.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # createsuperuser 시 username도 물어보도록 설정

    def __str__(self):
        return self.email


# 사용자가 관심을 가질 키워드를 저장하는 모델
class Keyword(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='키워드명')

    def __str__(self):
        return self.name

# User와 Keyword의 관계를 정의하는 중간 모델 (다대다 관계)
# 어떤 유저가 어떤 키워드에 관심 있는지 저장합니다.
class UserKeyword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자')
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, verbose_name='키워드')

    class Meta:
        unique_together = ('user', 'keyword') # 유저-키워드 조합은 유일해야 함

    def __str__(self):
        return f"{self.user.email} - {self.keyword.name}"


# 스크래핑(수집)한 아티클 정보를 저장하는 모델
class Article(models.Model):
    keyword = models.ForeignKey(Keyword, on_delete=models.SET_NULL, null=True, verbose_name='키워드')
    title = models.CharField(max_length=255, verbose_name='제목')
    url = models.URLField(unique=True, verbose_name='URL')
    content = models.TextField(verbose_name='내용')
    published_at = models.DateTimeField(verbose_name='게시일')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    def __str__(self):
        return self.title


# 생성된 뉴스레터 정보를 저장하는 모델
class Newsletter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='수신자')
    title = models.CharField(max_length=255, verbose_name='뉴스레터 제목')
    content = models.TextField(verbose_name='뉴스레터 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name='발송일')

    def __str__(self):
        return f"[{self.user.email}] {self.title}"


class Topic(models.Model):
    """
    사용자가 구독할 관심 주제 모델
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="주제명"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="생성일"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "관심 주제"
        verbose_name_plural = f"{verbose_name} 목록"
        ordering = ['-created_at']