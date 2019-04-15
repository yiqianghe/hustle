from django.urls import path
from .views import CourseListView,CourseDetailView,CommentsView,CourseVideoView

app_name = 'courses'

urlpatterns = [
    # 全部课程列表
    path('list/', CourseListView.as_view(), name='courses_list'),
    # 课程详情
    path('<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
    # 课程评论
    path('<int:course_id>/comment/', CommentsView.as_view(), name='course_comment'),
    # 课程小节视频
    path('<int:course_id>/<int:lesson_id>/<int:video_id>/', CourseVideoView.as_view(), name='course_video'),
]