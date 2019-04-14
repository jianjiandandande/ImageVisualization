"""ImageVisualization URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.views.generic import TemplateView
import xadmin

from user.views import LoginView, RegisterView, ActiveUserView, ForgetView, ResetView, \
    ModifyPwdView, UploadView, ShowPictureView,IndexView

from picture.views import GetCTPictureInfoView, UploadSrcPicture, UploadCoordinate, USImage, CTImage

app_name = 'ImageVisualization'

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name="index2.html"), name="index2"),
    path('index/', IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('captcha/', include('captcha.urls')),
    path('active/<active_code>/', ActiveUserView.as_view(), name="user_active"),
    path('forget/', ForgetView.as_view(), name="forget_psw"),
    path('reset/<active_code>/', ResetView.as_view(), name="reset_pwd"),
    path('modify_pwd/', ModifyPwdView.as_view(), name="modify_psw"),
    path('upload/', UploadView.as_view(), name="upload_picture"),
    path('show_picture/<image_class>', ShowPictureView.as_view(), name="show_picture"),
    path('getCTPicture/', GetCTPictureInfoView.as_view(), name="get_ct_picture"),
    path('upload_src_picture/', UploadSrcPicture.as_view(), name="upload_src_picture"),
    path('upload_coordinate/', UploadCoordinate.as_view(), name="upload_coordinate"),
    # path('USImage/', USImage.as_view(), name="usImage"),
    # path('CTImage/', CTImage.as_view(), name="ctImage"),
]
