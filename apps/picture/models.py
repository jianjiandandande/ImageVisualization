from django.db import models
from datetime import datetime
from user.models import UserProfile


# Create your models here.


class Picture(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE)
    name = models.CharField(max_length=500, verbose_name=u"图片名")
    desc = models.CharField(max_length=300, verbose_name=u"图片描述")
    image_real = models.ImageField(upload_to="picture/%Y/%m", verbose_name=u"具体图片", max_length=100)
    url = models.CharField(max_length=200, default="", verbose_name=u"访问地址")
    visitors = models.IntegerField(default=0, verbose_name=u'浏览人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image_mark = models.ImageField(upload_to="picture/%Y/%m", verbose_name=u"封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"图片"
        verbose_name_plural = verbose_name


class DICOMInformation(models.Model):

    def setInfo(self, information, username):
        # self.picture = picture
        self.patientID = information['patient']['PatientID']
        self.patientName = information['patient']['PatientName']
        self.patientBirthDate = information['patient']['PatientBirthDate']
        self.patientBirthTime = information['patient']['PatientBirthTime']
        self.patientSex = information['patient']['PatientSex']
        self.patientWeight = information['patient']['PatientWeight']
        self.patientStatus = information['patient']['PatientStatus']

        self.studyID = information['study']['StudyID']
        self.accessionNumber = information['study']['AccessionNumber']
        self.studyInstanceUID = information['study']['StudyInstanceUID']
        self.studyDate = information['study']['StudyDate']
        self.studyTime = information['study']['StudyTime']
        self.modalitiesinStudy = information['study']['ModalitiesinStudy']
        self.bodyPartExamined = information['study']['BodyPartExamined']
        self.studyDescription = information['study']['StudyDescription']
        self.patientAge = information['study']['PatientAge']

        self.seriesNumber = information['series']['SeriesNumber']
        self.seriesInstanceUID = information['series']['SeriesInstanceUID']
        self.modality = information['series']['Modality']
        self.seriesDescription = information['series']['SeriesDescription']
        self.seriesDate = information['series']['SeriesDate']
        self.seriesTime = information['series']['SeriesTime']

        self.sOPInstanceUID = information['instance']['SOPInstanceUID']
        self.instanceNumber = information['instance']['InstanceNumber']

        self.columns = information['instance']['Columns']
        self.rows = information['instance']['Rows']
        self.acquisitionNumber = information['instance']['AcquisitionNumber']
        self.photometricInterpretation = information['instance']['PhotometricInterpretation']
        self.bitsAllocated = information['instance']['BitsAllocated']
        self.bitsStored = information['instance']['BitsStored']
        self.pixelRepresentation = information['instance']['PixelRepresentation']
        self.samplesPerPixel = information['instance']['SamplesPerPixel']
        self.pixelSpacing = str(information['instance']['PixelSpacing'][0]) + '\\' + \
                            str(information['instance']['PixelSpacing'][1])
        self.highBit = information['instance']['HighBit']
        self.rescaleSlope = information['instance']['RescaleSlope']
        self.rescaleIntercept = information['instance']['RescaleIntercept']
        self.imageOrientation = str(information['instance']['ImageOrientation'][0]) + '\\' + \
                                str(information['instance']['ImageOrientation'][1]) + '\\' + \
                                str(information['instance']['ImageOrientation'][2]) + '\\' + \
                                str(information['instance']['ImageOrientation'][3]) + '\\' + \
                                str(information['instance']['ImageOrientation'][4]) + '\\' + \
                                str(information['instance']['ImageOrientation'][5])
        self.imagePosition = str(information['instance']['ImagePosition'][0]) + '\\' + \
                             str(information['instance']['ImagePosition'][1]) + '\\' + \
                             str(information['instance']['ImagePosition'][2])
        self.frameOfReferenceUID = information['instance']['FrameOfReferenceUID']
        self.imageType = information['instance']['ImageType'][0] + '\\' + \
                         information['instance']['ImageType'][1] + '\\' + \
                         information['instance']['ImageType'][2]
        self.username = username

    # Patient Tag
    patientID = models.CharField(max_length=50, verbose_name=u'患者ID')
    patientName = models.CharField(max_length=50, verbose_name=u'患者姓名')
    patientBirthDate = models.CharField(max_length=100, verbose_name=u'患者出生日期')
    patientBirthTime = models.CharField(max_length=100, verbose_name=u'患者出生时间')
    patientSex = models.CharField(choices=(("male", u"男"), ("female", u"女")), default="female", max_length=10)
    patientWeight = models.CharField(max_length=100, verbose_name=u'患者体重')
    patientStatus = models.CharField(choices=(("male", u"未怀孕"), ("female", u"已怀孕")), default="female", max_length=10)

    # Study Tag
    studyID = models.CharField(max_length=50, verbose_name=u'检查ID')
    accessionNumber = models.CharField(max_length=50, verbose_name=u'检查号')
    studyInstanceUID = models.CharField(max_length=500, verbose_name=u'检查实例号')
    studyDate = models.CharField(max_length=50, verbose_name=u'检查日期')
    studyTime = models.CharField(max_length=50, verbose_name=u'检查时间')
    modalitiesinStudy = models.CharField(max_length=50, verbose_name=u'检查类型')
    bodyPartExamined = models.CharField(max_length=50, verbose_name=u'检查的部位')
    studyDescription = models.CharField(max_length=300, verbose_name=u"检查的描述")
    patientAge = models.CharField(max_length=300, verbose_name=u"真实年龄")

    # Series Tag
    seriesNumber = models.CharField(max_length=50, verbose_name=u'序列号')
    seriesInstanceUID = models.CharField(max_length=500, verbose_name=u'序列实例号')
    modality = models.CharField(max_length=200, verbose_name=u'检查模态')
    seriesDescription = models.CharField(max_length=300, verbose_name=u'检查描述')
    seriesDate = models.CharField(max_length=50, verbose_name=u'检查日期')
    seriesTime = models.CharField(max_length=50, verbose_name=u'检查时间')

    # instance Tag
    sOPInstanceUID = models.CharField(max_length=500, verbose_name=u'SOP实例UID')
    instanceNumber = models.CharField(max_length=50, verbose_name=u'图像码')
    columns = models.CharField(max_length=50, verbose_name=u'列')
    rows = models.CharField(max_length=50, verbose_name=u'行')
    acquisitionNumber = models.CharField(max_length=50, verbose_name=u'获取码')
    photometricInterpretation = models.CharField(max_length=50, verbose_name=u'图片矩阵解释')
    bitsAllocated = models.CharField(max_length=50, verbose_name=u'bitsAllocated')
    bitsStored = models.CharField(max_length=50, verbose_name=u'BitsStored')
    pixelRepresentation = models.CharField(max_length=50, verbose_name=u'PixelRepresentation')
    samplesPerPixel = models.CharField(max_length=50, verbose_name=u'SamplesPerPixel')
    pixelSpacing = models.CharField(max_length=50, verbose_name=u'PixelSpacing')
    highBit = models.CharField(max_length=50, verbose_name=u'HighBit')
    rescaleSlope = models.CharField(max_length=50, verbose_name=u'RescaleSlope')
    rescaleIntercept = models.CharField(max_length=50, verbose_name=u'RescaleIntercept')
    imageOrientation = models.CharField(max_length=500, verbose_name=u'ImageOrientation')
    imagePosition = models.CharField(max_length=500, verbose_name=u'ImagePosition')
    frameOfReferenceUID = models.CharField(max_length=500, verbose_name=u'FrameOfReferenceUID')
    imageType = models.CharField(max_length=500, verbose_name=u'ImageType')
    username = models.CharField(max_length=50, verbose_name=u'上传用户')
    picture = models.ForeignKey(Picture, verbose_name=u"用户", on_delete=models.CASCADE)
    class Meta:
        verbose_name = u"DICOM信息"
        verbose_name_plural = verbose_name


class MedicalImageInfo(models.Model):
    imagePath = models.CharField(max_length=200, default="", verbose_name=u"图片上传地址")
    originalPath = models.CharField(max_length=200, default="", verbose_name=u"原始处理图片的地址")
    elasticPath = models.CharField(max_length=200, default="", verbose_name=u"弹性方式图片的地址")
    baseName = models.CharField(max_length=200, default="", verbose_name=u"图片名称")

    class Meta:
        verbose_name = u"医学影像信息"
        verbose_name_plural = verbose_name


class MedicalHandleInfo(models.Model):

    medicalImageInfo = models.ForeignKey(MedicalImageInfo, verbose_name=u"医学影像信息", on_delete=models.CASCADE)
    handleMode = models.CharField(choices=(("elastic", u"弹性图像"), ("original", u"原始图像"),('double',u'两种方式')), default="original", max_length=10)
    benignResult = models.FloatField(default=0.0, verbose_name=u"良性结果值")
    malignantResult = models.FloatField(default=0.0, verbose_name=u"恶性结果值")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"医学处理结果信息"
        verbose_name_plural = verbose_name
