# _*_ encoding: utf-8 _*_

__author__ = 'Vincent'
__date__ = '2019/3/4 20:41'

from random import Random
from user.models import EmailVerifyRecord
from django.core.mail import send_mail
from ImageVisualization.settings import EMAIL_FROM


#生成随机字符串
def random_str(randomLength = 8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomLength):
        str+=chars[random.randint(0,length)]
    return str

#发送邮箱进行激活提醒
def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""
    if send_type == "register":
        email_title = "Vincent空间激活链接"
        email_body = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)

    elif send_type == "forget":
        email_title = "Vincent空间重置链接"
        email_body = "请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}".format(code)

    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if send_status:
        pass