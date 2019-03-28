from django.shortcuts import render,HttpResponse
from django.views.generic import View
from .models import CollegeOrg, Teacher
from pure_pagination import Paginator,PageNotAnInteger
from courses.models import Course
from operation.models import UserFavorite
from django.db.models import Q
# Create your views here.


class CollegesView(View):
    """学院机构列表"""
    @classmethod
    def get(cls, request):
        all_colleges = CollegeOrg.objects.all()
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_colleges = all_colleges.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords))
        colleges_count = all_colleges.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1


        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_colleges, 5, request=request)

        colleges = p.page(page)

        return render(request, 'colleges.html', {
            'colleges': colleges,
            'colleges_count': colleges_count,
        })


class CollegeHomeView(View):
    """学院详情"""

    @classmethod
    def get(cls, request, college_id, get_type):
        college_org = CollegeOrg.objects.get(id=int(college_id))
        all_lecturers = college_org.teacher_set.all()
        all_courses = college_org.course_set.all()
        lecturers_counts = all_lecturers.count()
        courses_counts = all_courses.count()
        # 判断用户是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(college_id), fav_type=3):
                has_fav = True
        if get_type == 'lecturer':
            return render(request, 'college_detail.html', {
                'college_org': college_org,
                'college_id': college_id,
                'all_lecturers': all_lecturers,
                'lecturers_counts': lecturers_counts,
                'courses_counts': courses_counts,
                'has_fav': has_fav,
            })
        elif get_type == 'course':
            return render(request, 'college_detail.html', {
                'college_org': college_org,
                'college_id': college_id,
                'all_courses': all_courses,
                'lecturers_counts': lecturers_counts,
                'courses_counts': courses_counts,
            })


class CollegeCourseView(View):
    """学院课程详情"""

    @classmethod
    def get(cls, request, _college_id, _get_type, course_id):
        course = Course.objects.get(id=int(course_id))

        return render(request, 'course_detail.html',
                      {
                          'course': course,
                      })


class AddFavView(View):
    """用户收藏"""

    @classmethod
    def post(cls, request):
        fav_id = int(request.POST.get('fav_id', 0))
        fav_type = int(request.POST.get('fav_type', 0))

        if not request.user.is_authenticated:
            # 判断用户登陆状态
            return HttpResponse('{"status":"fail", "msg":"用户未登陆"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
        if exist_records:
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if fav_id > 0 and fav_type >0:
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class LecturerView(View):
    """讲师列表"""

    @classmethod
    def get(cls, request):
        all_lecturers = Teacher.objects.all()
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_lecturers = all_lecturers.filter(name__icontains=search_keywords)
        lecturers_count = all_lecturers.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1


        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_lecturers, 5, request=request)

        all_lecturers = p.page(page)
        return render(request, 'lecturers.html', {
            'all_lecturers': all_lecturers,
            'lecturers_count': lecturers_count,
        })


class LecturerDetailView(View):
    """讲师详情"""

    @classmethod
    def get(cls, request, lecturer_id):
        lecturer = Teacher.objects.get(id=int(lecturer_id))
        all_courses = lecturer.course_set.all()
        # 判断用户是否收藏课程
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(lecturer_id), fav_type=2):
                has_fav = True
        return render(request, 'lecturer_detail.html', {
            'lecturer': lecturer,
            'all_courses': all_courses,
            'has_fav': has_fav,})
