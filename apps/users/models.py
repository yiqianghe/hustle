from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):

    nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="男")
    grade = models.CharField(max_length=100, default="")
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(max_length=100, upload_to="image/%Y/%m", default="image/default.png")


    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username