from django.urls import path
from .views import CourseListView,CourseDetailView,CommentsView,AddCommentView,CourseVideoView
from colleges.views import AddFavView
app_name = 'courses'

urlpatterns = [
    # 全部课程列表
    path('list/', CourseListView.as_view(), name='courses_list'),
    # 课程详情
    path('<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
    # 课程评论
    path('<int:course_id>/comment/', CommentsView.as_view(), name='course_comment'),
    path('<int:course_id>/<int:lesson_id>/<int:video_id>/', CourseVideoView.as_view(), name='course_video'),
    # 添加课程评论
    path('add_comment/', AddCommentView.as_view(), name='add_comment'),
    # 收藏课程
    path('add_fav/', AddFavView.as_view(), name='add_fav_course'),

]