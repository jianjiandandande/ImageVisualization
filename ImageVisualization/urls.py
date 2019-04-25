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
    ModifyPwdView, UploadView, ShowPictureView, IndexView, ShowPictureDetailView, LogoutView, MineView, BaseSetting, \
    MineContent, ShowPictureDetailViewByPictureId, Welcome

from picture.views import GetCTPictureInfoView, UploadSrcPicture, UploadCoordinate, SendSuggest, SearchImage, \
    SendThyroidSuggest, SendSuggestByPictureId

app_name = 'ImageVisualization'

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name="index2.html"), name="index2"),
    path('index/', IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('mine/', MineView.as_view(), name="mine"),
    path('register/', RegisterView.as_view(), name="register"),
    path('captcha/', include('captcha.urls')),
    path('active/<active_code>/', ActiveUserView.as_view(), name="user_active"),
    path('forget/', ForgetView.as_view(), name="forget_psw"),
    path('reset/<active_code>/', ResetView.as_view(), name="reset_pwd"),
    path('modify_pwd/', ModifyPwdView.as_view(), name="modify_psw"),
    path('upload/', UploadView.as_view(), name="upload_picture"),
    path('show_picture/<image_class>/<page_index>', ShowPictureView.as_view(), name="show_picture"),
    path('show_picture_byId/<dicom_id>', ShowPictureDetailView.as_view(), name="show_detail_picture"),
    path('show_picture_byPictureId/<picture_id>', ShowPictureDetailViewByPictureId.as_view(), name="show_detail_picture_by_picture_id"),
    path('getCTPicture/', GetCTPictureInfoView.as_view(), name="get_ct_picture"),
    path('upload_src_picture/', UploadSrcPicture.as_view(), name="upload_src_picture"),
    path('upload_coordinate/', UploadCoordinate.as_view(), name="upload_coordinate"),
    path('send_suggest/<dicom_id>', SendSuggest.as_view(), name="send_suggest"),
    path('send_suggest_by_pictureId/<picture_id>', SendSuggestByPictureId.as_view(), name="send_suggest"),
    path('send_thyroid_suggest/<medicalImageInfoId>', SendThyroidSuggest.as_view(), name="send_thyroid_suggest"),
    path('search_image/', SearchImage.as_view(), name="search_image"),
    path('base_setting/', BaseSetting.as_view(), name="base_setting"),
    path('mine_content/', MineContent.as_view(), name="mine_content"),
    path('welcome/', Welcome.as_view(), name="mine_content"),
]
