# config/urls.py
from django.contrib import admin
from django.urls import path, include # include를 import 해주세요.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')), # '/api/' 라는 주소로 요청이 오면 core.urls를 보도록 설정
]