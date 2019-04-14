from datetime import datetime

from django.db import models

from user.models import UserProfile
from picture.models import Picture

class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"姓名")
    mobile = models.CharField(max_length=11, verbose_name=u"手机")
    picture_name = models.CharField(max_length=50, verbose_name=u"图片名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户咨询"
        verbose_name_plural = verbose_name


class PictureComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE)
    picture = models.ForeignKey(Picture, verbose_name=u"图片", on_delete=models.CASCADE)
    comments = models.CharField(max_length=200, verbose_name=u"评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"图片评论"
        verbose_name_plural = verbose_name

u"用户收藏"
class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE)
    fav_id = models.IntegerField(default=0, verbose_name=u"数据id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name


"用户浏览历史"
class UserHistory(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE)
    fav_id = models.IntegerField(default=0, verbose_name=u"数据id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户浏览历史"
        verbose_name_plural = verbose_name

#用户消息
class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u"接收用户")
    message = models.CharField(max_length=500, verbose_name=u"消息内容")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name