from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from .models import LikeCount, LikeRecord


def success_response(liked_num):
    data = {
        'status': 'SUCCESS',
        'liked_num': liked_num,
    }
    return JsonResponse(data)


def err_response(code, message):
    data = {
        'code': code,
        'message': message,
        'status': 'ERROR',
    }
    return JsonResponse(data)


def like_change(request):
    # 获取数据
    user = request.user
    if not user.is_authenticated:
        return err_response(400, '你还未登陆')
    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return err_response(401, '对象不存在')
    # 处理数据
    if request.GET.get('is_like') == 'true':  # 要点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:  # 未点赞过
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return success_response(like_count.liked_num)
        else:  # 已经点赞，不能重复点赞
            return err_response(402, '你已经点赞过啦')
    else:  # 取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():  # 有点赞过，可以取消
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            #  点赞总数-1
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:  # 不是新建的
                like_count.liked_num -= 1
                like_count.save()
                return success_response(like_count.liked_num)
            else:
                return err_response(404, '数据错误')
        else:  # 没点赞过自然不能取消
            return err_response(403, '你还未点赞过')
