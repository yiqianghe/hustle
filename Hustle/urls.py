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
# from django.contrib import admin
from django.urls import path, re_path
import xadmin
from users.views import LoginView, RegisterView,LogoutView
from colleges.views import LecturerView,LecturerDetailView
from courses.views import CourseDetailView
from django.views.static import serve
from Hustle.settings import MEDIA_ROOT,STATIC_ROOT
from django.urls import include


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # 首页
    path('', LoginView.as_view(), name="index"),
    # 登陆
    path('login/', LoginView.as_view(), name='login'),
    # 注销
    path('logout/', LogoutView.as_view(), name='logout'),
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
    # 课程详情
    path('lecturer/course/<int:course_id>', CourseDetailView.as_view(), name='teacher_course'),
    # 配置上传文件访问函数
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    # 配置静态文件访问函数
    re_path('static/(?P<path>.*)',  serve, {"document_root":STATIC_ROOT}),
    # 配置用户
    path('users/', include(('users.urls', 'users'), namespace='users')),

    # 用户操作
    path('operate/add_fav/', include(('operation.urls', 'operation'), namespace='operation'))
]

#全局404页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'