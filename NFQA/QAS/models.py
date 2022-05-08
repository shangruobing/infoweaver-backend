from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, AbstractBaseUser


class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('0', 'Administrator'),
        ('1', 'Student'),
        ('2', 'Teacher')
    ]
    id = models.AutoField(primary_key=True, verbose_name="用户ID")
    name = models.CharField(max_length=30, verbose_name='姓名', default='')
    username = models.CharField(max_length=10, verbose_name='用户名', unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=0)
    password = models.CharField(max_length=256, verbose_name='密码')
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='最后登录时间')
    objects = UserManager()
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = '用户'

    def __str__(self):
        return self.name


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
