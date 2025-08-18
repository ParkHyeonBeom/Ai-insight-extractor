# config/celery.py
import os
from celery import Celery

# Django의 settings 모듈을 Celery의 기본 설정으로 사용하도록 지정합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 'config'라는 이름으로 Celery 앱을 생성합니다.
app = Celery('config')

# 'CELERY' 네임스페이스를 사용하는 모든 Celery 관련 설정을 Django settings.py에서 불러옵니다.
# 예: CELERY_BROKER_URL
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django 앱 설정에 정의된 task들을 자동으로 로드합니다. (예: core/tasks.py)
app.autodiscover_tasks()