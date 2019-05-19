from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class LikeCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    liked_num = models.IntegerField(default=0, verbose_name='获赞数')

    class Meta:
        verbose_name_plural = "点赞计数"


class LikeRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='点赞人')
    liked_time = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name_plural = "点赞记录"
