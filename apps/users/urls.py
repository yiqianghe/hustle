from django.urls import path
from users.views import UserInfoView,UploadImageView,UpdatePwdView,UserFavView,UserLecturerCourseView,UploadVideoView,CreateCourseView,CreateLessonView
app_name = 'users'

urlpatterns = [
    # 获取/修改个人信息
    path('info/', UserInfoView.as_view(), name='user_info'),
    # 上传头像
    path('image/upload/', UploadImageView.as_view(), name='image_upload'),
    # 修改密码
    path('update/pwd/', UpdatePwdView.as_view(), name='update_pwd'),
    # 获取用户收藏
    path('fav/', UserFavView.as_view(), name='users_fav'),
    # 获取教师课程
    path('lecturer_course/', UserLecturerCourseView.as_view(), name='lecturer_course'),
    # 教师新建课程
    path('create/course/', CreateCourseView.as_view(), name='create_course'),
    # 教师新建章节
    path('create/lesson/', CreateLessonView.as_view(), name='create_lesson'),
    # 教师上传视频
    path('video/upload/', UploadVideoView.as_view(), name='video_upload'),
]