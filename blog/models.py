from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

from read_account.models import ReadNumExpandMethod, ReadDetail


class BlogType(models.Model):
    type_name = models.CharField(max_length=15, verbose_name='博客类型')

    class Meta:
        verbose_name_plural = "博客类型"

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50, verbose_name='标题')
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE, verbose_name='博客类型')
    content = RichTextUploadingField(verbose_name='内容')
    read_details = GenericRelation(ReadDetail, verbose_name='博客详情')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='发表日期')
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_email(self):
        return self.author.email

    def __str__(self):
        # return '<标题:%s>' % self.title
        return self.title

    class Meta:
        verbose_name_plural = "博客信息"
        ordering = ['-created_time']


# class ReadNum(models.Model):
#     read_num = models.IntegerField(default=0)
#     # blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
#     blog = models.OneToOneField(Blog, on_delete=models.CASCADE)
