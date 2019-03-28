from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm,RegisterForm,UploadImageForm,ModifyPwdForm,UserInfoForm
from django.contrib.auth.hashers import make_password
from colleges.models import CollegeOrg,Teacher
from courses.models import Course
from utils.login_utils import LoginRequiredMixin
import json
from django.urls import reverse
from operation.models import UserFavorite
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


class LogoutView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


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


class UserInfoView(LoginRequiredMixin, View):
        """用户个人信息
        """

        def get(self, request):
            return render(request, 'user_info.html', {})

        def post(self, request):
            user_info_form = UserInfoForm(request.POST, instance=request.user)
            if user_info_form.is_valid():
                user_info_form.save()
                return render(request, 'user_info.html', {})
            else:
                return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')



class UploadImageView(LoginRequiredMixin, View):
    """用户修改头像
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            image_form.save()
            return render(request, 'user_info.html', {})
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    """个人中心修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password", "")
            pwd2 = request.POST.get("confirm_password", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class UserFavView(View):
    """
    用户收藏
    """
    def get(self, request):
        all_courses = []
        courses_list = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for course in courses_list:
            course_id = course.fav_id
            course = Course.objects.get(id=course_id)
            all_courses.append(course)

        all_lecturers = []
        lecturers_list = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for lecturer in lecturers_list:
            lecturer_id = lecturer.fav_id
            lecturer = Teacher.objects.get(id=lecturer_id)
            all_lecturers.append(lecturer)

        all_colleges = []
        colleges_list = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for college in colleges_list:
            college_id = college.fav_id
            college = CollegeOrg.objects.get(id=college_id)
            all_colleges.append(college)

        return render(request, "user_fav.html", {
            'all_courses': all_courses,
            'all_lecturers': all_lecturers,
            'all_colleges': all_colleges,
        })


def page_not_found(request):
    #全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    #全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 500
    return response