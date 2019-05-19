from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'content_object', 'comment_time', 'user')
    # 分页显示，一页的数量
    list_per_page = 30
