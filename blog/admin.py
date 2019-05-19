from django.contrib import admin
from . import models


@admin.register(models.BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'blog_type', 'author', 'get_read_num', 'created_time', 'last_updated_time')

    # 需要搜索的字段
    search_fields = ('blog_type__type_name',)

    list_filter = ('blog_type', 'author', 'created_time', 'last_updated_time')

    # 分页显示，一页的数量
    list_per_page = 20

    date_hierarchy = 'created_time'

    actions_on_top = True

# @admin.register(models.ReadNum)
# class BlogReadNumAdmin(admin.ModelAdmin):
#     list_display = ('read_num', 'blog')
