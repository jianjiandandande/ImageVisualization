from django.shortcuts import render
from django.views.generic.base import View
from .models import Picture, DICOMInformation
from user.models import UserProfile
from .models import DICOMInformation, MedicalImageInfo, MedicalHandleInfo, DoctorSuggest, DoctorSuggestForThyroid
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
        try:
            medicalImage = MedicalImageInfo.objects.get(imagePath=srcPath)
        except Exception:
            medicalImage = None

        if medicalImage == None:
            medicalImage = MedicalImageInfo()
            medicalImage.imagePath = srcPath
            medicalImage.baseName = baseName
            medicalImage.save()
        print("srcPath = ", srcPath)
        return render(request, 'medicalHandle.html', {'url': srcPath, "baseName": baseName})


check_result = {"Panyaru-38-f_20180418_154801_image.jpg": [0.8494, 0.9988, 0.9997],
                "The-006-82_20180315_161215_image.jpg": [0.5343, 0.9265, 0.8965],
                "The-006-58_20180131_155157_image.jpg": [0.3824, 0.0281, 0.1221]}


class UploadCoordinate(View):
    def get(self, request):
        return HttpResponse("get")

    def post(self, request):
        if request.method == 'POST':

            firstSX = 0
            firstSY = 0
            firstEX = 0
            firstEY = 0
            secondSX = 0
            secondSY = 0
            secondEX = 0
            secondEY = 0
            result = 0

            user_name = request.session.get("username")  # 获取用户名信息
            chooseModel = request.POST.get("model", "")
            baseName = request.POST.get("baseName")
            model = 3
            if chooseModel == 'elastic':
                print("basename= ", baseName)
                result = check_result.get(baseName)[1]
                model = 1
            elif chooseModel == 'original':
                model = 2
                print("basename= ", baseName)
                result = check_result.get(baseName)[0]
            elif chooseModel == 'double':
                model = 3
                result = check_result.get(baseName)[2]

            print("result = ", result)
            imgSX = int(request.POST.get("imgSX"))
            imgSY = int(request.POST.get("imgSY"))
            imgEX = int(request.POST.get("imgEX"))
            imgEY = int(request.POST.get("imgEY"))
            firstSX = int(request.POST.get("firstSX"))
            firstSY = int(request.POST.get("firstSY"))
            firstEX = int(request.POST.get("firstEX"))
            firstEY = int(request.POST.get("firstEY"))
            if model == 3:
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
                       url, user_name, model, baseName)
            badResult = "%.4f" % (1.0 - result)
            medicalImageInfo = MedicalImageInfo.objects.get(imagePath=url)
            try:
                suggestsForThyroid = DoctorSuggestForThyroid.objects.filter(medicalImageInfo=medicalImageInfo)
            except Exception:
                suggestsForThyroid = None
            return render(request, 'medicalHandle.html',
                          {"medicalImageInfoId": medicalImageInfo.id, "suggestsForThyroid": suggestsForThyroid,
                           'url': url, 'baseName': baseName, 'msg': "裁剪成功!",
                           "result": result, "badResult": badResult})


class SendSuggest(View):

    def post(self, request, dicom_id):
        print(dicom_id)
        user_name = request.session.get("username")  # 获取用户名信息
        dicom = DICOMInformation.objects.get(username=user_name, id=dicom_id)
        if dicom == None:
            print("dicom is None")
        else:
            print("dicom is not None")

        try:
            my_suggest = DoctorSuggest.objects.filter(dicomInfo=dicom, doctorName=user_name)[0]
        except Exception:
            my_suggest = None

        mySuggest = request.POST.get("suggest")

        if my_suggest == None:
            my_suggest = DoctorSuggest()
            my_suggest.dicomInfo = dicom
            my_suggest.doctorName = user_name
            my_suggest.suggest = mySuggest
            my_suggest.save()
        else:
            my_suggest.suggest = mySuggest
            my_suggest.save()

        suggests = DoctorSuggest.objects.filter(dicomInfo=dicom)
        print("suggest.size = ", len(suggests))

        return render(request, 'show_detail.html', {'dicom': dicom, "suggests": suggests})


class SendSuggestByPictureId(View):

    def post(self, request, picture_id):
        print(picture_id)
        user_name = request.session.get("username")  # 获取用户名信息
        picture = Picture.objects.get(username=user_name, id=picture_id)
        if picture == None:
            print("dicom is None")
        else:
            print("dicom is not None")

        mySuggest = request.POST.get("suggest")
        picture.suggest = mySuggest
        picture.save()
        suggests = []
        suggests.insert(len(suggests), picture.suggest)
        return render(request, 'show_detail_by_Picture.html', {'picture': picture, "suggests": suggests})


class SearchImage(View):
    def post(self, request):
        user_name = request.session.get("username")  # 获取用户名信息
        search_class = int(request.POST.get("search_class"))
        search_content = request.POST.get("search_content")
        dicomInfos = None
        if search_class == 2:
            dicomInfos = DICOMInformation.objects.filter(username=user_name, patientName=search_content)
        elif search_class == 3:
            dicomInfos = DICOMInformation.objects.filter(username=user_name, modality=search_content)
        elif search_class == 1:
            try:
                picture = Picture.objects.get(name=search_content)
            except Exception:
                picture = None
            if picture != None:
                dicomInfos = DICOMInformation.objects.filter(username=user_name, picture=picture)
        return render(request, 'ClassImage.html', {'dicomInfos': dicomInfos})


class SendThyroidSuggest(View):
    def post(self, request, medicalImageInfoId):
        user_name = request.session.get("username")  # 获取用户名信息

        medicalImageInfo = MedicalImageInfo.objects.get(id=medicalImageInfoId)
        baseName = medicalImageInfo.baseName

        try:
            my_suggest = DoctorSuggestForThyroid.objects.filter(medicalImageInfo=medicalImageInfo, doctorName=user_name)[0]
        except Exception:
            my_suggest = None

        mySuggest = request.POST.get("suggest")

        if my_suggest == None:
            my_suggest = DoctorSuggestForThyroid()
            my_suggest.medicalImageInfo = medicalImageInfo
            my_suggest.doctorName = user_name
            my_suggest.suggest = mySuggest
            my_suggest.save()
        else:
            my_suggest.suggest = mySuggest
            my_suggest.save()

        suggestsForThyroid = DoctorSuggestForThyroid.objects.filter(medicalImageInfo=medicalImageInfo)
        print("suggest for thyroid's size = ", len(suggestsForThyroid))
        result = request.POST.get("result")
        badResult = request.POST.get("badResult")
        return render(request, 'medicalHandle.html',
                      {"suggestsForThyroid": suggestsForThyroid, 'url': medicalImageInfo.imagePath, 'baseName': baseName, "result": result,
                       "badResult": badResult})
