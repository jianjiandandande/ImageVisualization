# Generated by Django 2.1.7 on 2019-04-10 11:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picture', '0002_auto_20190408_0956'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalHandleInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handleMode', models.CharField(choices=[('elastic', '弹性图像'), ('original', '原始图像'), ('double', '两种方式')], default='original', max_length=10)),
                ('benignResult', models.FloatField(default=0.0, verbose_name='良性结果值')),
                ('malignantResult', models.FloatField(default=0.0, verbose_name='恶性结果值')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '医学处理结果信息',
                'verbose_name_plural': '医学处理结果信息',
            },
        ),
        migrations.CreateModel(
            name='MedicalImageInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagePath', models.CharField(default='', max_length=200, verbose_name='图片上传地址')),
                ('originalPath', models.CharField(default='', max_length=200, verbose_name='原始处理图片的地址')),
                ('elasticPath', models.CharField(default='', max_length=200, verbose_name='弹性方式图片的地址')),
            ],
            options={
                'verbose_name': '医学影像信息',
                'verbose_name_plural': '医学影像信息',
            },
        ),
        migrations.AlterField(
            model_name='picture',
            name='name',
            field=models.CharField(max_length=500, verbose_name='图片名'),
        ),
        migrations.AddField(
            model_name='medicalhandleinfo',
            name='medicalImageInfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='picture.MedicalImageInfo', verbose_name='医学影像信息'),
        ),
    ]
