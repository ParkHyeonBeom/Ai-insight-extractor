# core/admin.py
from django.contrib import admin
from .models import User, Keyword, UserKeyword, Article, Newsletter

admin.site.register(User)
admin.site.register(Keyword)
admin.site.register(UserKeyword)
admin.site.register(Article)
admin.site.register(Newsletter)