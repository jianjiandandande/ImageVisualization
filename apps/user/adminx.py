# _*_ encoding: utf-8 _*_

__author__ = 'Vincent'
__date__ = '2019/3/4 20:31'

import xadmin
from xadmin import views
from user.models import EmailVerifyRecord,Banner,UserProfile

#主题的添加
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

#全局logo的添加
class GlobalSettings(object):
    site_title = "Vincent的空间"
    site_footer = "Vincent在线网"
    menu_style = "accordion"


class UserProfileAdmin(object):
    # nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default='')
    # birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    # gender = models.CharField(choices=(("male", u"男"), ("female", u"女")), default="female", max_length=10)
    # address = models.CharField(max_length=100, default=u"")
    # mobile = models.CharField(max_length=11, null=True, blank=True)
    # image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100)
    list_display = ['username', 'nick_name', 'mobile', "gender"]  # 展示
    search_fields = ['username', 'nick_name', 'mobile', "gender"]  # 搜索
    list_filter = ['username', 'nick_name', 'mobile', "gender"]  # 筛选


class EmailVerifyRecordAdmin(object):

    list_display = ['code', 'email', 'send_type', "send_time"] #展示
    search_fields = ['code', 'email', 'send_type'] # 搜索
    list_filter = ['code', 'email', 'send_type', "send_time"] # 筛选


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)