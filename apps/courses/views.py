from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q

from pure_pagination import Paginator,PageNotAnInteger

from .models import Course
from operation.models import CourseComments,UserFavorite

# Create your views here.


class CourseListView(View):
    """课程列表
    """

    @classmethod
    def get(cls, request):
        all_courses = Course.objects.all()
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords))
        courses_count = all_courses.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1


        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_courses, 5, request=request)

        all_courses = p.page(page)

        return render(request, 'courses.html', {
            'all_courses': all_courses,
            'courses_count': courses_count,
        })


class CourseDetailView(View):
    """课程详情
    """

    @classmethod
    def get(cls, request, course_id):
        course = Course.objects.get(id=int(course_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_id), fav_type=1):
                has_fav = True
        return render(request, 'course_detail.html',
                      {
                          'course': course,
                          'has_fav': has_fav,
                      })


class CourseVideoView(View):
    """课程视频
    """

    @classmethod
    def get(cls, request, course_id, lesson_id, video_id):
        course = Course.objects.get(id=int(course_id))
        current_lesson = course.lesson_set.get(id=int(lesson_id))
        current_video = current_lesson.video_set.get(id=int(video_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_id), fav_type=1):
                has_fav = True
        return render(request, 'course_detail.html',
                      {
                          'course': course,
                          'current_video': current_video,
                          'has_fav': has_fav,
                      })


class CommentsView(View):
    """课程评论
    """

    @classmethod
    def get(cls, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = CourseComments.objects.filter(course=course)
        return render(request, 'course_comment.html', {
            'course': course,
            'all_comments': all_comments,
        })



