from django.db import models

from datetime import datetime
# Create your models here.

from users.models import UserProfile
from courses.models import Course


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    comments = models.CharField(max_length=200, verbose_name="评论", default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    fav_id = models.IntegerField(default=0, verbose_name="数据id")
    fav_type = models.IntegerField(choices=((1, "课程"), (2, "讲师"), (3, "学院机构")), default=1, verbose_name="收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name


# class UserMessage(models.Model):
#     user = models.IntegerField(default=0, verbose_name="接受用户")
#     message = models.CharField(max_length=500, verbose_name="消息内容")
#     has_red = models.BooleanField(default=False, verbose_name="是否已读")
#     add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
#
#     class Meta:
#         verbose_name = "用户消息"
#         verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name
