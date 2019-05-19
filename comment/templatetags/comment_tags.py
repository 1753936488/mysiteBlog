from django import template
from django.db.models.fields import exceptions
from read_account.models import ReadNum
from ..forms import CommentForm
from ..models import Comment
from django.contrib.contenttypes.models import ContentType
register = template.Library()


@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()


@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    data = {
        'content_type': content_type.model,
        'object_id': obj.pk,
        'reply_comment_id': 0,
    }
    form = CommentForm(initial=data)
    return form


@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comment = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comment.order_by('-comment_time')


@register.simple_tag
def get_read_num(obj):
    try:
        ct = ContentType.objects.get_for_model(obj)
        readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        return readnum.read_num
    except exceptions.ObjectDoesNotExist:
        return 0