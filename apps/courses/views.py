from django.shortcuts import render,HttpResponse
from django.views.generic import View
from .models import Course
from pure_pagination import Paginator,PageNotAnInteger
from operation.models import CourseComments,UserFavorite
from django.db.models import Q
# Create your views here.


class CourseListView(View):
    """课程列表"""

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
    """课程详情"""

    @classmethod
    def get(cls, request, course_id):
        course = Course.objects.get(id=int(course_id))
        first_lesson = course.lesson_set.all()[0]
        current_video = first_lesson.video_set.all()[0]
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_id), fav_type=1):
                has_fav = True
        return render(request, 'course_detail.html',
                      {
                          'course': course,
                          'first_video': current_video,
                          'has_fav': has_fav,
                      })


class CourseVideoView(View):
    """课程视频"""

    @classmethod
    def get(cls, request, course_id, lesson_id, video_id):
        course = Course.objects.get(id=int(course_id))
        current_lesson = course.lesson_set.get(id=int(lesson_id))
        current_video = current_lesson.video_set.get(id=int(video_id))
        return render(request, 'course_detail.html',
                      {
                          'course': course,
                          'current_video': current_video,
                      })


class CommentsView(View):
    """课程评论"""

    @classmethod
    def get(cls, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = CourseComments.objects.filter(course=course)
        return render(request, 'course_comment.html', {
            'course': course,
            'all_comments': all_comments,
        })


class AddCommentView(View):
    """添加评论"""

    @classmethod
    def post(cls, request):

        if not request.user.is_authenticated:
            # 判断用户登陆状态
            return HttpResponse('{"status":"fail", "msg":"用户未登陆"}', content_type='application/json')

        course_id = int(request.POST.get('course_id', 0))
        comments = request.POST.get('comments', '')
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=course_id)
            course_comments.user = request.user
            course_comments.course = course
            course_comments.comments = comments
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')

