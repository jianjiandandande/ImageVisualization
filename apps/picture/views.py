from django.shortcuts import render
from django.views.generic.base import View
from .models import Picture, DICOMInformation
from user.models import UserProfile
from .models import DICOMInformation, MedicalImageInfo, MedicalHandleInfo
import json
from django.http import HttpResponse
from django.conf import settings

from utils.GetDICOMInformation import storeSrcImage, storeOriginalImage, storeElasticImage, cutPicture


# Create your views here.
##显示图片
class GetCTPictureInfoView(View):
    def get(self, request):

        user_name = request.session.get("username")  # 获取用户名信息
        print(user_name)
        informations = {}
        transactionId = 'CTStudy'
        informations['transactionId'] = transactionId
        studies = []
        dicomInfos = DICOMInformation.objects.all()
        print(len(dicomInfos))
        for dicomInfo in dicomInfos:
            if dicomInfo.modality == 'CT':
                studiesInfo = {}
                studiesInfo["studyInstanceUid"] = dicomInfo.studyInstanceUID
                studiesInfo["studyDescription"] = dicomInfo.studyDescription
                studiesInfo["studyDate"] = dicomInfo.studyDate
                studiesInfo["studyTime"] = dicomInfo.studyTime
                studiesInfo["patientName"] = dicomInfo.patientName
                studiesInfo["patientBirthData"] = dicomInfo.patientBirthDate
                studiesInfo["patientSex"] = dicomInfo.patientSex
                studiesInfo["patientId"] = dicomInfo.patientID
                seriesList = []
                seriesListInfo = {}
                seriesListInfo['seriesDescription'] = dicomInfo.seriesDescription
                seriesListInfo['seriesInstanceUid'] = dicomInfo.seriesInstanceUID
                seriesListInfo['seriesBodyPart'] = dicomInfo.bodyPartExamined
                seriesListInfo['seriesNumber'] = dicomInfo.seriesNumber
                seriesListInfo['seriesDate'] = dicomInfo.seriesDate
                seriesListInfo['seriesTime'] = dicomInfo.studyTime
                seriesListInfo['seriesModality'] = dicomInfo.modality
                instances = []
                instancesInfo = {}
                instancesInfo['columns'] = dicomInfo.columns
                instancesInfo['rows'] = dicomInfo.rows
                instancesInfo['instanceNumber'] = dicomInfo.instanceNumber
                instancesInfo['acquisitionNumber'] = dicomInfo.acquisitionNumber
                instancesInfo['photometricInterpretation'] = dicomInfo.photometricInterpretation
                instancesInfo['bitAllocated'] = dicomInfo.bitsAllocated
                instancesInfo['bitsStored'] = dicomInfo.bitsStored
                instancesInfo['pixelRepresentation'] = dicomInfo.pixelRepresentation
                instancesInfo['samplesPerPixel'] = dicomInfo.samplesPerPixel
                instancesInfo['pixelSpacing'] = dicomInfo.pixelSpacing
                instancesInfo['highBit'] = dicomInfo.highBit
                instancesInfo['rescaleSlope'] = dicomInfo.rescaleSlope
                instancesInfo['rescaleIntercept'] = dicomInfo.rescaleIntercept
                instancesInfo['imageOrientationPatient'] = dicomInfo.imageOrientation
                instancesInfo['imagePositionPatient'] = dicomInfo.imagePosition
                instancesInfo['frameOfReferenceUID'] = dicomInfo.frameOfReferenceUID
                instancesInfo['imageType'] = dicomInfo.imageType
                instancesInfo['sopInstanceUid'] = dicomInfo.sOPInstanceUID
                instancesInfo['url'] = 'dicomweb://' + (settings.ALLOWED_HOSTS[
                                                            0] + ':8000/static/uploadFile/15735657418@163.com/DICOM/' + dicomInfo.picture.name).replace(
                    '\\', '/')

                instances.insert(len(instances), instancesInfo)
                seriesListInfo['instances'] = instances

                seriesList.insert(len(seriesList), seriesListInfo)
                studiesInfo['seriesList'] = seriesList

                studies.insert(len(studies), studiesInfo)
                informations['studies'] = studies
            else:
                continue
        response = HttpResponse(json.dumps(informations), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        return response


class UploadSrcPicture(View):
    def get(self, request):
        return render(request, 'medicalHandle.html', {})

    def post(self, request):
        user_name = request.session.get("username")  # 获取用户名信息
        # 从请求当中　获取文件对象
        file = request.FILES.get('picture')
        srcPath, baseName = storeSrcImage(file, user_name)
        medicalImage = MedicalImageInfo()
        if MedicalImageInfo.objects.get(imagePath=srcPath) == None:
            medicalImage.imagePath = srcPath
            medicalImage.baseName = baseName
            medicalImage.save()
        print("srcPath = ", srcPath)
        return render(request, 'medicalHandle.html', {'url': srcPath})


class UploadCoordinate(View):
    def get(self, request):
        return HttpResponse("get")

    def post(self, request):
        if request.method == 'POST':
            user_name = request.session.get("username")  # 获取用户名信息
            imgSX = int(request.POST.get("imgSX"))
            imgSY = int(request.POST.get("imgSY"))
            imgEX = int(request.POST.get("imgEX"))
            imgEY = int(request.POST.get("imgEY"))
            firstSX = int(request.POST.get("firstSX"))
            firstSY = int(request.POST.get("firstSY"))
            firstEX = int(request.POST.get("firstEX"))
            firstEY = int(request.POST.get("firstEY"))
            secondSX = int(request.POST.get("secondSX"))
            secondSY = int(request.POST.get("secondSY"))
            secondEX = int(request.POST.get("secondEX"))
            secondEY = int(request.POST.get("secondEY"))
            url = request.POST.get("url", "")
            print("imgSX = ", imgSX)
            print("imgSY = ", imgSY)
            print("imgEX = ", imgEX)
            print("imgEY = ", imgEY)
            print("firstSX = ", firstSX)
            print("firstSY = ", firstSY)
            print("firstEX = ", firstEX)
            print("firstEY = ", firstEY)
            print("secondSX = ", secondSX)
            print("secondSY = ", secondSY)
            print("secondEX = ", secondEX)
            print("secondEY = ", secondEY)
            print("url = ", url)
            cutPicture(imgSX, imgSY, imgEX, imgEY,
                       firstSX, firstSY, firstEX, firstEY,
                       secondSX, secondSY, secondEX, secondEY,
                       url, user_name)

            return HttpResponse(url)


class USImage(View):
    def get(self, request):
        return render(request, 'usImage.html', )
    def post(self, request):
        return render(request, 'usImage.html', )

class CTImage(View):
    def get(self, request):
        return render(request, 'ctImage.html', )
    def post(self, request):
        return render(request, 'ctImage.html', )
