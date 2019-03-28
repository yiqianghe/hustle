from django.urls import path
from users.views import UserInfoView,UploadImageView,UpdatePwdView,UserFavView

app_name = 'users'

urlpatterns = [
    # 个人信息
    path('', UserInfoView.as_view(), name='users_center'),
    # 头像上传
    path('image/upload/', UploadImageView.as_view(), name='image_upload'),
    # 修改密码
    path('update/pwd/', UpdatePwdView.as_view(), name='update_pwd'),
    # 用户收藏
    path('fav/', UserFavView.as_view(), name='users_fav'),
]