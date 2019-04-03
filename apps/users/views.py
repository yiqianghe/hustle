from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm,RegisterForm,UploadImageForm,ModifyPwdForm,UserInfoForm,UploadVideoForm,CreateCourseForm,CreateLessonForm
from django.contrib.auth.hashers import make_password
from colleges.models import CollegeOrg,Teacher
from courses.models import Course,Lesson,Video
from utils.login_utils import LoginRequiredMixin
import json
from django.urls import reverse
from operation.models import UserFavorite
# Create your views here.


class CustomBackend(ModelBackend):
    """设置username/email均可登陆
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as _e:
            return  None


class LogoutView(View):
    """用户登出
    """

    @classmethod
    def get(cls, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    """登陆
    """

    @classmethod
    def get(cls, request):
        all_courses = Course.objects.all()
        all_lecturers = Teacher.objects.all()
        all_colleges = CollegeOrg.objects.all()
        return render(request, "index.html", {
            'all_courses': all_courses,
            'all_lecturers': all_lecturers,
            'all_colleges': all_colleges,
        })

    @classmethod
    def post(cls, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            account = request.POST.get("account", "")
            password = request.POST.get("password", "")
            user = authenticate(username=account, password=password)  # 认证
            if user:
                login(request, user)
                return HttpResponse('{"status":"success", "msg":"登陆成功！！！"}', content_type='application/json')
            else:
                # return render(request, "index.html", {
                #     "msg": "账号或密码错误",
                #     'all_courses': all_courses,
                #     'all_lecturers': all_lecturers,
                #     'all_colleges': all_colleges,
                # })
                return HttpResponse('{"status":"fail", "msg":"账号或密码错误"}', content_type='application/json')
        else:
            # return render(request, "index.html", {
            #     "login_form": login_form,
            #     'all_courses': all_courses,
            #     'all_lecturers': all_lecturers,
            #     'all_colleges': all_colleges,
            # })
            return HttpResponse('{"status":"fail", "msg":"账号或密码错误"}', content_type='application/json')


class RegisterView(View):
    """注册
    """

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
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            account = request.POST.get("account", "")
            college = request.POST.get("college", "")
            is_lecturer = request.POST.get("is_lecturer", "")
            password = request.POST.get("password", "")
            if is_lecturer == 'Teacher':
                teacher = Teacher()
                teacher.college_org_id = int(college)
                teacher.name = account
                teacher.save()
                user_profile = UserProfile()
                user_profile.username = account
                user_profile.password = make_password(password)
                user_profile.is_active = 1
                user_profile.teacher = teacher
                user_profile.save()
            elif is_lecturer == 'Student':
                user_profile = UserProfile()
                user_profile.username = account
                user_profile.password = make_password(password)
                user_profile.is_active = 1
                user_profile.save()
            login(request, UserProfile.objects.get(username=account))
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            error_message = str(json.loads(register_form.errors.as_json()))
            error_content = '{{"status": "fail","msg":"{}"}}'.format(error_message)
            return HttpResponse(error_content, content_type='application/json')


class UserInfoView(LoginRequiredMixin, View):
        """用户个人信息
        """

        @classmethod
        def get(cls, request):
            return render(request, 'user_info.html', {})

        @classmethod
        def post(cls, request):
            user_info_form = UserInfoForm(request.POST, instance=request.user)
            if user_info_form.is_valid():
                user_info_form.save()
                return render(request, 'user_info.html', {})
            else:
                return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')



class UploadImageView(LoginRequiredMixin, View):
    """用户修改头像
    """

    @classmethod
    def post(cls, request):
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

    @classmethod
    def post(cls, request):
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
    """用户收藏
    """

    @classmethod
    def get(cls, request):
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


class UserLecturerCourseView(View):
    """教师用户:讲师课程页面
    """

    @classmethod
    def get(cls, request):
        teacher = Teacher.objects.get(userprofile=request.user)
        courses = Course.objects.filter(teacher=teacher)
        lessons = []
        for course in courses:
            lessons.extend(Lesson.objects.filter(course=course))
        return render(request, 'user_lecturer_course.html', {
            'courses': courses,
            'lessons': lessons,
        })


class UploadVideoView(LoginRequiredMixin, View):
    """教师用户上传视频
    """

    @classmethod
    def post(cls, request):
        video_form = UploadVideoForm(request.POST, request.FILES)
        if video_form.is_valid():
            lesson = video_form.cleaned_data['lesson']
            name = video_form.cleaned_data['name']
            video_file = video_form.cleaned_data['video_file']
            video = Video()
            video.lesson_id = int(lesson)
            video.name = name
            video.video_file = video_file
            video.save()

            teacher = Teacher.objects.get(userprofile=request.user)
            courses = Course.objects.filter(teacher=teacher)
            lessons = []
            for course in courses:
                lessons.extend(Lesson.objects.filter(course=course))
            return render(request, 'user_lecturer_course.html', {
                'courses': courses,
                'lessons': lessons,
            })
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class CreateCourseView(LoginRequiredMixin, View):
    """教师用户新建课程
    """

    @classmethod
    def post(cls, request):
        course_form = CreateCourseForm(request.POST, request.FILES)
        if course_form.is_valid():
            name = course_form.cleaned_data['name']
            image = course_form.cleaned_data['image']

            teacher = Teacher.objects.get(userprofile=request.user)
            course = Course()
            course.name = name
            course.image = image
            course.college_org = teacher.college_org
            course.teacher = teacher
            course.save()

            courses = Course.objects.filter(teacher=teacher)
            lessons = []
            for course in courses:
                lessons.extend(Lesson.objects.filter(course=course))
            return render(request, 'user_lecturer_course.html', {
                'courses': courses,
                'lessons': lessons,
            })
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class CreateLessonView(LoginRequiredMixin, View):
    """教师用户新建章节
    """

    @classmethod
    def post(cls, request):
        lesson_form = CreateLessonForm(request.POST)
        if lesson_form.is_valid():
            name = lesson_form.cleaned_data['name']
            course = lesson_form.cleaned_data['course']
            lesson = Lesson()
            lesson.name = name
            lesson.course_id = int(course)
            lesson.save()

            teacher = Teacher.objects.get(userprofile=request.user)
            courses = Course.objects.filter(teacher=teacher)
            lessons = []
            for course in courses:
                lessons.extend(Lesson.objects.filter(course=course))
            return render(request, 'user_lecturer_course.html', {
                'courses': courses,
                'lessons': lessons,
            })
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


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