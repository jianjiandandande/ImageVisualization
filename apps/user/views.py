from django.shortcuts import render

# Create your views here.
import os
import SimpleITK
import pydicom
import numpy as np
import cv2
from tqdm import tqdm

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import HttpResponse
# Create your views here.

from .models import UserProfile, EmailVerifyRecord
from picture.models import Picture, DICOMInformation, MedicalImageInfo, DoctorSuggest
from .forms import LoginForm, RegisterForm, ForgetForm, ResetPwdForm
from utils.send_email import send_register_email
from utils.GetDICOMInformation import dicom_2png, loadFileInformation, storeDICOM, storeSrcImage, storeMR, Mr2Png


# 重写登录验证用户名和密码的功能
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username), )
            if user.check_password(password):
                return user
        except Exception as e:
            return None


##基于函数的登录功能的实现
# def user_login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, "index.html",{})
#         else:
#             return render(request, 'login.html', {"msg": "用户名或者密码错误"})
#     elif request.method == 'GET':
#         return render(request, 'login.html',{})
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html', {})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['username'] = user_name
                    print("username = ", user_name)
                    print("image = ", user.image)
                    return render(request, "index2.html", {"username": user_name, 'user': user})
                else:
                    return render(request, 'login.html', {"msg": "用户未激活"})
            else:
                return render(request, 'login.html', {"msg": "用户名或者密码错误"})
        else:
            return render(request, 'login.html', {"login_form": login_form})


class LogoutView(View):
    def get(self, request):
        request.session['username'] = None
        return render(request, "index2.html", )


class MineView(View):
    def get(self, request):
        return render(request, "mine.html", )


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get("email", "")
            pass_word = request.POST.get("password", "")
            user_profile = None
            try:
                user_profile = UserProfile.objects.get(email=email)
            except UserProfile.DoesNotExist:
                user_profile = None

            if user_profile is not None:
                return render(request, 'register.html', {"register_form": register_form, "msg": "该邮箱已被注册"})
            else:
                user_profile = UserProfile()
                user_profile.username = email
                user_profile.email = email
                user_profile.is_active = False
                user_profile.password = make_password(pass_word)  # 对密码进行加密
                user_profile.save()
                send_register_email(email, "register")  # 发送邮箱进行验证
                return render(request, "login.html")
        else:
            return render(request, 'register.html', {"register_form": register_form})


##激活用户
class ActiveUserView(View):
    def get(self, request, active_code):
        all_codes = EmailVerifyRecord.objects.filter(code=active_code)
        if all_codes:
            for code in all_codes:
                email = code.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


##忘记密码
class ForgetView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")  # 发送邮箱进行验证
            return render(request, "send_success.html", {})
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


##重置密码
class ResetView(View):
    def get(self, request, active_code):
        all_codes = EmailVerifyRecord.objects.filter(code=active_code)
        if all_codes:
            for code in all_codes:
                email = code.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


##修改密码
class ModifyPwdView(View):
    def post(self, request):
        reset_pwd_form = ResetPwdForm(request.POST)
        if reset_pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password=pwd1)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "reset_pwd_form": reset_pwd_form})


def get_file_extension(filename):
    arr = os.path.splitext(filename)
    return arr[len(arr) - 1]


##上传图片
class UploadView(View):
    def get(self, request):
        return render(request, 'upload_picture.html', {})

    def post(self, request):
        user_name = request.session.get("username")  # 获取用户名信息
        user = UserProfile()
        if user_name != None:
            user = UserProfile.objects.get(username=user_name)
        # 从请求当中　获取文件对象
        file = request.FILES.get('picture')

        if get_file_extension(file.name) == '.mha':
            filePath = storeMR(file, user_name)
            Mr2Png(filePath, user_name)
            picture = Picture()
            picture.name = file.name
            picture.user = user
            picture.url = user_name + '/PNG/' + file.name
            picture.desc = "MR"
            picture.username = user_name
            picture.save()
        else:
            filePath = storeDICOM(file, user_name)
            dicom_2png(filePath, user_name)
            information = loadFileInformation(filePath)
            for title, body in information.items():
                for key, value in body.items():
                    print(key, value)
            picture = Picture()
            picture.name = file.name
            picture.user = user
            picture.url = user_name + '/PNG/' + file.name
            picture.save()

            dicomInfo = DICOMInformation()
            dicomInfo.setInfo(information, user_name)
            dicomInfo.picture = picture
            dicomInfo.save()
        return HttpResponse('上传成功！')


##显示图片
class ShowPictureView(View):
    def get(self, request, image_class, page_index):
        print('image_class', image_class)
        print('page_index', page_index)

        page_count = 8
        show_datas = []
        showS = (int(page_index) - 1) * page_count
        showE = int(page_index) * page_count - 1
        if image_class == 'MR':
            user_name = request.session.get("username")  # 获取用户名信息
            pictures = Picture.objects.filter(desc='MR', username=user_name)
            count = len(pictures)
            if count / page_count == 0:
                total_page = int(count / page_count)
            else:
                total_page = int(count / page_count) + 1
            total_pages = []
            for i in range(total_page):
                total_pages.insert(len(total_pages), i + 1)

            if count >= showE:
                for i in range(showS, showE + 1):
                    show_datas.insert(len(show_datas), pictures[i])
            elif (count >= showS) and (count < showE):
                for i in range(showS, count):
                    show_datas.insert(len(show_datas), pictures[i])
            elif count < showS:
                show_datas = None

            return render(request, 'ClassImage.html',
                          {'image_class': image_class, 'current_page': page_index, 'total_page': total_page,
                           'pictures': show_datas, 'total_pages': total_pages})
        else:
            user_name = request.session.get("username")  # 获取用户名信息
            print(user_name)
            dicomInfos = DICOMInformation.objects.filter(username=user_name, modality=image_class)
            count = len(dicomInfos)
            print('count = ', count)
            if count / page_count == 0:
                total_page = int(count / page_count)
            else:
                total_page = int(count / page_count) + 1
            total_pages = []
            for i in range(total_page):
                total_pages.insert(len(total_pages), i + 1)

            if count > showE:
                for i in range(showS, showE + 1):
                    show_datas.insert(len(show_datas), dicomInfos[i])
            elif (count >= showS) and (count <= showE):
                for i in range(showS, count):
                    show_datas.insert(len(show_datas), dicomInfos[i])
            elif count < showS:
                show_datas = None
            return render(request, 'ClassImage.html',
                          {'image_class': image_class, 'current_page': page_index, 'total_page': total_page,
                           'dicomInfos': show_datas, 'total_pages': total_pages})


##显示图片的详细信息
class ShowPictureDetailView(View):
    def get(self, request, dicom_id):
        print(dicom_id)
        user_name = request.session.get("username")  # 获取用户名信息
        dicom = DICOMInformation.objects.get(username=user_name, id=dicom_id)
        if dicom == None:
            print("dicom is None")
        else:
            print("dicom is not None")
        suggests = DoctorSuggest.objects.filter(dicomInfo=dicom)
        print("suggest.size = ", len(suggests))
        return render(request, 'show_detail.html', {'dicom': dicom, "suggests": suggests})


##显示图片的详细信息
class ShowPictureDetailViewByPictureId(View):
    def get(self, request, picture_id):
        print(picture_id)
        user_name = request.session.get("username")  # 获取用户名信息
        picture = Picture.objects.get(username=user_name, id=picture_id)
        if picture == None:
            print("picture is None")
        else:
            print("picture is not None")
        suggests = []
        suggests.insert(len(suggests), picture.suggest)
        print("suggest.size = ", len(suggests))
        return render(request, 'show_detail_by_Picture.html', {'picture': picture, "suggests": suggests})


class BaseSetting(View):
    def get(self, request):
        user_name = request.session.get("username")  # 获取用户名信息
        user = UserProfile.objects.get(username=user_name)
        return render(request, 'baseSetting.html', {'user': user})


class MineContent(View):
    def get(self, request):
        user_name = request.session.get("username")  # 获取用户名信息
        user = UserProfile.objects.get(username=user_name)
        return render(request, 'mineContent.html', {'user': user})


class Welcome(View):
    def get(self, request):
        return render(request, 'welcome.html', )
