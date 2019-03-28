from django.db import models
from datetime import datetime

# Create your models here.


class CollegeOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name="学院名称")
    desc= models.TextField(verbose_name="学院描述")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(upload_to="college_org/%Y/%m", verbose_name="学院logo")
    address = models.CharField(max_length=150, verbose_name="学院地址")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "学院机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_teacher_counts(self):
        return self.teacher_set.all().count()

    def get_course_counts(self):
        return self.course_set.all().count()

class Teacher(models.Model):
    college_org = models.ForeignKey(CollegeOrg, on_delete=models.CASCADE, verbose_name="所属学院")
    name = models.CharField(max_length=50, verbose_name="讲师名称")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    address = models.CharField(max_length=150, verbose_name="办公地址")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="讲师封面", default='')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "讲师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_counts(self):
        return self.course_set.all().count()