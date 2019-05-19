from django.contrib import admin
from . import models


@admin.register(models.LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'liked_num')
    # 分页显示，一页的数量
    list_per_page = 30


@admin.register(models.LikeRecord)
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    # 分页显示，一页的数量
    list_per_page = 20

