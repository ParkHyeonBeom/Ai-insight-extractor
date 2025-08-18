# config/__init__.py

# 이 코드는 Django가 시작될 때 항상 Celery 앱이 임포트되도록 보장하여,
# @shared_task 데코레이터가 우리가 만든 앱을 사용하게 합니다.
from .celery import app as celery_app

__all__ = ('celery_app',)