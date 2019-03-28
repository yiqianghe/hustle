"""Hustle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
import xadmin
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView,UserInfoView
from colleges.views import LecturerView,LecturerDetailView,AddFavView
from courses.views import CourseDetailView
from django.views.static import serve
from Hustle.settings import MEDIA_ROOT
from django.urls import include


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # 首页
    path('', LoginView.as_view(), name="index"),
    # 登陆
    path('login/', LoginView.as_view(), name='login'),
    # 注册
    path('register/', RegisterView.as_view(), name='register'),

    # 学院机构
    path('colleges/', include(('colleges.urls', 'colleges'), namespace='colleges')),
    # 课程
    path('courses/', include(('courses.urls', 'courses'), namespace='courses')),
    # 讲师
    path('lecturer/list/', LecturerView.as_view(), name='teacher'),
    # 讲师详情
    path('lecturer/<int:lecturer_id>/', LecturerDetailView.as_view(), name='teacher_detail'),
    # 收藏讲师
    path('add_fav/', AddFavView.as_view(), name='add_fav_lecturer'),
    # 课程详情
    path('lecturer/course/<int:course_id>', CourseDetailView.as_view(), name='teacher_course'),
    # 配置上传文件访问函数
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    path('user/', UserInfoView.as_view(), name='user'),
]
