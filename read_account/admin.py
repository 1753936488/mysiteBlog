from django.contrib import admin
from .models import ReadNum, ReadDetail


@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'content_object')
    # 分页显示，一页的数量
    list_per_page = 20


@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'date', 'content_object')
    # 分页显示，一页的数量
    list_per_page = 20
