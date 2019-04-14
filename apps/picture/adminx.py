# _*_ encoding: utf-8 _*_

__author__ = 'Vincent'
__date__ = '2019/3/20 14:54'

import xadmin
from xadmin import views
from picture.models import Picture, DICOMInformation


class PictureAdmin(object):
    # user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE)
    # name = models.CharField(max_length=50, verbose_name=u"图片名")
    # desc = models.CharField(max_length=300, verbose_name=u"图片描述")
    # image_real = models.ImageField(upload_to="picture/%Y/%m", verbose_name=u"具体图片", max_length=100)
    # url = models.CharField(max_length=200, default="", verbose_name=u"访问地址")
    # visitors = models.IntegerField(default=0, verbose_name=u'浏览人数')
    # fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    # image_mark = models.ImageField(upload_to="picture/%Y/%m", verbose_name=u"封面图", max_length=100)
    # click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    # add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    list_display = ['user', 'name', 'url', "visitors", 'fav_nums', 'click_nums']  # 展示
    search_fields = ['user', 'name', 'url', "visitors", 'fav_nums', 'click_nums']  # 搜索
    list_filter = ['user', 'name', 'url', "visitors", 'fav_nums', 'click_nums']  # 筛选


class DICOMInformationAdmin(object):
    # picture = models.ForeignKey(Picture, verbose_name=u"图片", on_delete=models.CASCADE)
    #
    # # Patient Tag
    # patientID = models.CharField(max_length=50, verbose_name=u'患者ID')
    # patientName = models.CharField(max_length=50, verbose_name=u'患者姓名')
    # patientBirthDate = models.CharField(max_length=100, verbose_name=u'患者出生日期')
    # patientBirthTime = models.CharField(max_length=100, verbose_name=u'患者出生时间')
    # patientSex = models.CharField(choices=(("male", u"男"), ("female", u"女")), default="female", max_length=10)
    # patientWeight = models.CharField(max_length=100, verbose_name=u'患者体重')
    # patientStatus = models.CharField(choices=(("male", u"未怀孕"), ("female", u"已怀孕")), default="female", max_length=10)
    #
    # # Study Tag
    #
    # studyID = models.CharField(max_length=50, verbose_name=u'检查ID')
    # accessionNumber = models.CharField(max_length=50, verbose_name=u'检查号')
    # studyInstanceUID = models.CharField(max_length=50, verbose_name=u'检查实例号')
    # studyDate = models.CharField(max_length=50, verbose_name=u'检查日期')
    # studyTime = models.CharField(max_length=50, verbose_name=u'检查时间')
    # modalitiesinStudy = models.CharField(max_length=50, verbose_name=u'检查类型')
    # bodyPartExamined = models.CharField(max_length=50, verbose_name=u'检查的部位')
    # studyDescription = models.CharField(max_length=300, verbose_name=u"检查的描述")
    # patientAge = models.CharField(max_length=300, verbose_name=u"真实年龄")
    #
    # # Series Tag
    # seriesNumber = models.CharField(max_length=50, verbose_name=u'序列号')
    # seriesInstanceUID = models.CharField(max_length=50, verbose_name=u'序列实例号')
    # modality = models.CharField(max_length=50, verbose_name=u'检查模态')
    # seriesDescription = models.CharField(max_length=300, verbose_name=u'检查描述')
    # seriesDate = models.CharField(max_length=50, verbose_name=u'检查日期')
    # seriesTime = models.CharField(max_length=50, verbose_name=u'检查时间')
    # bodyPartExamined = models.CharField(max_length=50, verbose_name=u'身体部位')
    # # Image Tag
    # sOPInstanceUID = models.CharField(max_length=50, verbose_name=u'SOP实例UID')
    # contentDate = models.CharField(max_length=50, verbose_name=u'影像拍摄的日期')
    # contentTime = models.CharField(max_length=50, verbose_name=u'影像拍摄的时间')
    # instanceNumber = models.CharField(max_length=50, verbose_name=u'图像码')
    list_display = ['patientID', 'patientName', 'studyTime', "modalitiesinStudy", 'modality', 'bodyPartExamined',
                    'instanceNumber']  # 展示
    search_fields = ['patientID', 'patientName', 'studyTime', "modalitiesinStudy", 'modality', 'bodyPartExamined',
                     'instanceNumber']  # 搜索
    list_filter = ['patientID', 'patientName', 'studyTime', "modalitiesinStudy", 'modality', 'bodyPartExamined',
                   'instanceNumber']  # 筛选


xadmin.site.register(Picture, PictureAdmin)
xadmin.site.register(DICOMInformation, DICOMInformationAdmin)