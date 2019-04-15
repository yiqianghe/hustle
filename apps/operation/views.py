from django.shortcuts import HttpResponse
from django.views.generic import View

from colleges.models import CollegeOrg, Teacher
from operation.models import UserFavorite
from courses.models import Course
from operation.models import CourseComments

# Create your views here.


class AddFavView(View):
    """用户收藏
    """

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
            if fav_type == 1:
                course = Course.objects.get(id=fav_id)
                course.fav_nums -= 1
                course.save()
            elif fav_type == 2:
                teacher = Teacher.objects.get(id=fav_id)
                teacher.fav_nums -= 1
                teacher.save()
            elif fav_type == 3:
                college = CollegeOrg.objects.get(id=fav_id)
                college.fav_nums -= 1
                college.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if fav_id > 0 and fav_type >0:
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums += 1
                    course.save()
                elif fav_type == 2:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums += 1
                    teacher.save()
                elif fav_type == 3:
                    college = CollegeOrg.objects.get(id=fav_id)
                    college.fav_nums += 1
                    college.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class AddCommentView(View):
    """添加评论
    """

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