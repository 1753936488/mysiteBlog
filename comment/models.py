import threading

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User


from mysiteBlog import settings
from django.template.loader import render_to_string


class SendMail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, '', settings.EMAIL_HOST_USER, [self.email],
                  fail_silently=self.fail_silently, html_message=self.text)


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField(verbose_name='评论内容')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, verbose_name='评论人')
    root = models.ForeignKey('self', related_name="comment_root", null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name="comment_parent", null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def send_email(self):
        #  发送邮件通知
        if self.parent is None:
            #  评论我的博客
            subject = '有人评论了你的博客'
            email = self.content_object.get_email()
        else:
            #  回复评论
            subject = '有人回复了你的博客'
            email = self.reply_to.email
        if email != "":
            context = {
                'comment_text': self.text,
                'url': r'http://127.0.0.1:8000'+self.content_object.get_url(),
            }
            text = render_to_string('comment/send_mail.html', context)
            sendmail = SendMail(subject, text, email)
            sendmail.start()

    class Meta:
        verbose_name_plural = '评论'
        ordering = ['comment_time']
