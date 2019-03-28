from django.db import models
from datetime import datetime
from colleges.models import CollegeOrg,Teacher
# Create your models here.


class Course(models.Model):
    college_org = models.ForeignKey(CollegeOrg, on_delete=models.CASCADE, verbose_name="学院机构", null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="讲师", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    degree = models.CharField(verbose_name="难度", choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name="学习时长（分钟数）")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson(self):
        # 课程章节
        return self.lesson_set.all()

    def get_lesson_count(self):
        # 课程章节数
        return self.lesson_set.all().count()

    def get_learn_users(self):
        # 课程学习人数
        return self.usercourse_set.all()[:5]


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_video(self):
        # 章节视频
        return self.video_set.all()

    def get_video_count(self):
        # 章节视频数
        return self.video_set.all().count()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="章节")
    name = models.CharField(max_length=100, verbose_name="视频名")
    url = models.CharField(max_length=300, verbose_name="视频地址", default="")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name