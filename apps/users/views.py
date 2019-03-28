from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm,RegisterForm
from django.contrib.auth.hashers import make_password
from colleges.models import CollegeOrg,Teacher
from courses.models import Course
# Create your views here.


class CustomBackend(ModelBackend):
    """设置username/email均可登陆"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as _e:
            return  None


class LoginView(View):
    """登陆"""

    @classmethod
    def get(cls, request):
        all_courses = Course.objects.all()[:4]
        all_lecturers = Teacher.objects.all()[:4]
        all_colleges = CollegeOrg.objects.all()[:4]
        return render(request, "index.html", {
            'all_courses': all_courses,
            'all_lecturers': all_lecturers,
            'all_colleges': all_colleges,
        })

    @classmethod
    def post(cls, request):
        all_courses = Course.objects.all()[:4]
        all_lecturers = Teacher.objects.all()[:4]
        all_colleges = CollegeOrg.objects.all()[:4]
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            account = request.POST.get("account", "")
            password = request.POST.get("password", "")
            user = authenticate(username=account, password=password)  # 认证
            if user:
                login(request, user)
                return render(request, "index.html", {
                    'all_courses': all_courses,
                    'all_lecturers': all_lecturers,
                    'all_colleges': all_colleges,
                })
            else:
                return render(request, "index.html", {
                    "msg": "账号或密码错误",
                    'all_courses': all_courses,
                    'all_lecturers': all_lecturers,
                    'all_colleges': all_colleges,
                })
        else:
            return render(request, "index.html", {
                "login_form": login_form,
                'all_courses': all_courses,
                'all_lecturers': all_lecturers,
                'all_colleges': all_colleges,
            })


class RegisterView(View):
    """注册"""

    @classmethod
    def get(cls, request):
        return render(request, "index.html", {})

    @classmethod
    def post(cls, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            account = request.POST.get("account", "")
            password = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = account
            user_profile.password = make_password(password)
            user_profile.is_active = 1
            user_profile.save()
            login(request, UserProfile.objects.get(username=account))
            return render(request, "index.html", {})
        else:
            return render(request, "index.html", {"register_form": register_form})


class UserInfoView(View):
    @classmethod
    def get(cls, request):
        return render(request, "user_info.html", {})