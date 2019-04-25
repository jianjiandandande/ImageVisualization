# _*_ encoding: utf-8 _*_

__author__ = 'Vincent'
__date__ = '2019/3/18 15:09'

import pydicom
import matplotlib.pyplot as plt
from skimage import img_as_float
import numpy as np
import SimpleITK as s
import os
import time
import cv2

import leancloud

from django.conf import settings
from picture.models import MedicalImageInfo


import os
import shutil
import stat
def delete_file(filePath):
    if os.path.exists(filePath):
        for fileList in os.walk(filePath):
            for name in fileList[2]:
                os.chmod(os.path.join(fileList[0],name), stat.S_IWRITE)
                os.remove(os.path.join(fileList[0],name))
        shutil.rmtree(filePath)
        return True
    else:
        return False

# 创建文件夹
def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        return True
    else:
        return False


# 将DICOM文件存在本地
def storeDICOM(file, username):
    mkdir(settings.MEDIA_ROOT + username + '/DICOM')
    fname = settings.MEDIA_ROOT + username + '/DICOM/' + file.name
    with open(fname, 'wb') as pic:
        for c in file.chunks():
            pic.write(c)
    return fname

def storeMR(file, username):
    mkdir(settings.MEDIA_ROOT + username + '/MR')
    fname = settings.MEDIA_ROOT + username + '/MR/' + file.name
    with open(fname, 'wb') as pic:
        for c in file.chunks():
            pic.write(c)
    return fname

def Mr2Png(filePath,username):
    mkdir(settings.MEDIA_ROOT + username + '/PNG')
    fileName = os.path.basename(filePath)
    img = s.ReadImage(filePath)
    fa = s.GetArrayFromImage(img)
    fa = fa.astype(np.uint8)
    print(fa.shape)
    for i in range(80, fa.shape[0]):
        print(i)
        if np.max(fa[i]) != 0:
            cv2.imwrite(settings.MEDIA_ROOT + username + '/PNG/' + fileName + '.png', fa[i])
            break

# 存储源图片
def storeSrcImage(file, username):

    mkdir(settings.MEDIA_ROOT + username + '/src')
    filePath = (settings.MEDIA_ROOT + username + '/src/' + file.name).replace('\\', '/')
    with open(filePath, 'wb') as pic:
        for c in file.chunks():
            pic.write(c)
    return filePath,file.name


# 存储普通的医疗图片
def storeOriginalImage(file, username):

    mkdir(settings.MEDIA_ROOT + username + '/original')
    fname = settings.MEDIA_ROOT + username + '/SRC/' + file.name
    with open(fname, 'wb') as pic:
        for c in file.chunks():
            pic.write(c)
    return fname


# 存储弹性医疗图片
def storeElasticImage(file, username):

    mkdir(settings.MEDIA_ROOT + username + '/elastic')
    fname = settings.MEDIA_ROOT + username + '/elastic/' + file.name
    with open(fname, 'wb') as pic:
        for c in file.chunks():
            pic.write(c)
    return fname


# 将DICOM格式中图片信息解析出来，转化成png格式
def dicom_2png(filePath, username):
    dcm = pydicom.dcmread(filePath)
    fileName = os.path.basename(filePath)
    imageX = dcm.pixel_array
    temp = imageX.copy()
    print("shape ----", imageX.shape)
    picMax = imageX.max()
    vmin = imageX.min()
    vmax = temp[temp < picMax].max()
    imageX[imageX > vmax] = 0
    imageX[imageX < vmin] = 0
    image = img_as_float(imageX)
    mkdir(settings.MEDIA_ROOT + username + '/PNG')
    plt.cla()
    plt.figure('adjust_gamma', figsize=(10.24, 10.24))
    plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
    plt.imshow(image, 'gray')
    plt.axis('off')
    plt.savefig(settings.MEDIA_ROOT + username + '/PNG/' + fileName + '.png')
    # time.sleep(1)


def cutPicture(imgSX, imgSY, imgEX, imgEY,
               firstSX, firstSY, firstEX, firstEY,
               secondSX, secondSY, secondEX, secondEY,
               url, username,model,baseName):
    img = cv2.imread(url, 1)
    # cv2.imshow('img', img)

    width = imgEX - imgSX
    height = imgEY - imgSY
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
    # cv2.imshow('new_img', img)

    # print("firstX = ", firstSX - imgSX, "width = ", firstEX - imgSX)
    # print("firstY = ", firstSY - imgSY, "height = ", firstEY - imgSY)
    medicalImage = MedicalImageInfo.objects.get(imagePath=url)

    if model == 1:
        elasticDst = img[firstSY - imgSY:firstEY - imgSY, firstSX - imgSX:firstEX - imgSX]
        mkdir(settings.MEDIA_ROOT + username + '/elastic')
        medicalImage.elasticPath = settings.MEDIA_ROOT + username + '/elastic/' + "00_" + baseName
        cv2.imwrite(medicalImage.elasticPath, elasticDst)
    elif model == 2:
        originalDst = img[firstSY - imgSY:firstEY - imgSY, firstSX - imgSX:firstEX - imgSX]

        mkdir(settings.MEDIA_ROOT + username + '/original')
        medicalImage.originalPath = settings.MEDIA_ROOT + username + '/original/' + "01_" + baseName
        cv2.imwrite(medicalImage.originalPath, originalDst)
    elif model == 3:
        elasticDst = img[firstSY - imgSY:firstEY - imgSY, firstSX - imgSX:firstEX - imgSX]
        originalDst = img[secondSY - imgSY:secondEY - imgSY, secondSX - imgSX:secondEX - imgSX]
        mkdir(settings.MEDIA_ROOT + username + '/elastic')
        mkdir(settings.MEDIA_ROOT + username + '/original')
        medicalImage.elasticPath = settings.MEDIA_ROOT + username + '/elastic/'+"00_"+baseName
        medicalImage.originalPath = settings.MEDIA_ROOT + username + '/original/'+"01_"+baseName
        cv2.imwrite(medicalImage.elasticPath, elasticDst)
        cv2.imwrite(medicalImage.originalPath, originalDst)
    medicalImage.save()


# 读取与患者相关的信息
def loadFileInformation(filename):
    information = {}
    patient = {}
    study = {}
    series = {}
    instance = {}
    # Patient Tag
    ds = pydicom.dcmread(filename)
    print(ds)
    try:
        patient['PatientID'] = ds.PatientID  # 患者ID
    except AttributeError:
        patient['PatientID'] = 'unknow'

    try:
        patient['PatientName'] = ds.PatientName  # 患者姓名
    except AttributeError:
        patient['PatientName'] = 'unknow'
    try:
        patient['PatientBirthDate'] = ds.PatientBirthDate  # 患者出生日期
    except AttributeError:
        patient['PatientBirthDate'] = 'unknow'
    try:
        patient['PatientBirthTime'] = ds.PatientBirthTime  # 患者出生时间
    except AttributeError:
        patient['PatientBirthTime'] = 'unknow'
    try:
        patient['PatientSex'] = ds.PatientSex  # 患者性别
    except AttributeError:
        patient['PatientSex'] = 'unknow'
    try:
        patient['PatientWeight'] = ds.PatientWeight  # 患者体重
    except AttributeError:
        patient['PatientWeight'] = 'unknow'
    try:
        patient['PatientStatus'] = ds.PatientStatus  # 怀孕状态
    except AttributeError:
        patient['PatientStatus'] = 'unknow'

    information['patient'] = patient
    # Study Tag

    try:
        study['StudyID'] = ds.StudyID  # 检查ID
    except AttributeError:
        study['StudyID'] = 'unknow'
    try:
        study['AccessionNumber'] = ds.AccessionNumber  # 检查号
    except AttributeError:
        study['AccessionNumber'] = 'unknow'
    try:
        study['StudyInstanceUID'] = ds.StudyInstanceUID  # 检查实例号
    except AttributeError:
        study['StudyInstanceUID'] = 'unknow'
    try:
        study['StudyDate'] = ds.StudyDate  # 检查日期
    except AttributeError:
        study['StudyDate'] = 'unknow'
    try:
        study['StudyTime'] = ds.StudyTime  # 检查时间
    except AttributeError:
        study['StudyTime'] = 'unknow'
    try:
        study['ModalitiesinStudy'] = ds.ModalitiesinStudy  # 检查类型
    except AttributeError:
        study['ModalitiesinStudy'] = 'unknow'
    try:
        study['BodyPartExamined'] = ds.BodyPartExamined  # 检查的部位
    except AttributeError:
        study['BodyPartExamined'] = 'unknow'
    try:
        study['StudyDescription'] = ds.StudyDescription  # 检查的描述
    except AttributeError:
        study['StudyDescription'] = 'unknow'
    try:
        study['PatientAge'] = ds.PatientAge  # 真实年龄
    except AttributeError:
        study['PatientAge'] = 'unknow'

    information['study'] = study

    # Series Tag

    try:
        series['SeriesNumber'] = ds.SeriesNumber  #
    except AttributeError:
        series['SeriesNumber'] = 'unknow'
    try:
        series['SeriesInstanceUID'] = ds.SeriesInstanceUID  #
    except AttributeError:
        series['SeriesInstanceUID'] = 'unknow'
    try:
        series['Modality'] = ds.Modality  # 检查类型
    except AttributeError:
        series['Modality'] = 'unknow'
    try:
        series['SeriesDescription'] = ds.SeriesDescription  # 检查描述
    except AttributeError:
        series['SeriesDescription'] = 'unknow'
    try:
        series['SeriesDate'] = ds.SeriesDate  # 检查日期
    except AttributeError:
        series['SeriesDate'] = 'unknow'
    try:
        series['SeriesTime'] = ds.SeriesTime  # 检查时间
    except AttributeError:
        series['SeriesTime'] = 'unknow'

    information['series'] = series

    # instance Tag
    try:
        instance['SOPInstanceUID'] = ds.SOPInstanceUID  # SOP实例UID
    except AttributeError:
        instance['SOPInstanceUID'] = 'unknow'
    try:
        instance['Columns'] = ds.Columns  # 影像拍摄的日期
    except AttributeError:
        instance['Columns'] = 'unknow'
    try:
        instance['Rows'] = ds.Rows  # 影像拍摄的时间
    except AttributeError:
        instance['Rows'] = 'unknow'
    try:
        instance['InstanceNumber'] = ds.InstanceNumber  # 图像码
    except AttributeError:
        instance['InstanceNumber'] = 'unknow'
    try:
        instance['AcquisitionNumber'] = ds.AcquisitionNumber  # 影像拍摄的日期
    except AttributeError:
        instance['AcquisitionNumber'] = 'unknow'
    try:
        instance['PhotometricInterpretation'] = ds.PhotometricInterpretation  # 影像拍摄的时间
    except AttributeError:
        instance['PhotometricInterpretation'] = 'unknow'
    try:
        instance['BitsAllocated'] = ds.BitsAllocated  # 图像码
    except AttributeError:
        instance['BitsAllocated'] = 'unknow'
    try:
        instance['BitsStored'] = ds.BitsStored  # 影像拍摄的日期
    except AttributeError:
        instance['BitsStored'] = 'unknow'
    try:
        instance['PixelRepresentation'] = ds.PixelRepresentation  # 影像拍摄的时间
    except AttributeError:
        instance['PixelRepresentation'] = 'unknow'
    try:
        instance['SamplesPerPixel'] = ds.SamplesPerPixel  # 图像码
    except AttributeError:
        instance['SamplesPerPixel'] = 'unknow'
    try:
        instance['PixelSpacing'] = ds.PixelSpacing  # 影像拍摄的时间
    except AttributeError:
        instance['PixelSpacing'] = 'unknow'
    try:
        instance['HighBit'] = ds.HighBit  # 图像码
    except AttributeError:
        instance['HighBit'] = 'unknow'
    try:
        instance['RescaleSlope'] = ds.RescaleSlope  # 影像拍摄的日期
    except AttributeError:
        instance['RescaleSlope'] = 'unknow'
    try:
        instance['RescaleIntercept'] = ds.RescaleIntercept  # 影像拍摄的时间
    except AttributeError:
        instance['RescaleIntercept'] = 'unknow'
    try:
        instance['ImageOrientation'] = ds.ImageOrientationPatient  # 图像码
    except AttributeError:
        instance['ImageOrientation'] = 'unknow'
    try:
        instance['ImagePosition'] = ds.ImagePositionPatient  # 图像码
    except AttributeError:
        instance['ImagePosition'] = 'unknow'
    try:
        instance['FrameOfReferenceUID'] = ds.FrameOfReferenceUID  # 影像拍摄的日期
    except AttributeError:
        instance['FrameOfReferenceUID'] = 'unknow'
    try:
        instance['ImageType'] = ds.ImageType  # 影像拍摄的时间
    except AttributeError:
        instance['ImageType'] = 'unknow'

    information['instance'] = instance

    return information


if __name__ == "main":
    img = cv2.imread('', 1)
    cv2.imshow('img', img)
    cv2.waitKey(0)
