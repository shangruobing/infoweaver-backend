from django.db import models


class Notice(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    date = models.DateTimeField(blank=True, null=True)
    label = models.CharField(max_length=64, null=True)
    file_id = models.IntegerField(verbose_name="文件编号", unique=True, null=True)
    desc = models.CharField(max_length=64, null=True)
    region = models.CharField(max_length=64, null=True)

    class Meta:
        verbose_name = '通知文件表'


class UploadFile(models.Model):
    id = models.AutoField(primary_key=True)
    upload_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='上传时间')
    username = models.CharField(max_length=64, null=True)
    file_name = models.CharField(max_length=64, null=True)

    class Meta:
        verbose_name = '上传文件表'
