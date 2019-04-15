from django.urls import path
from .views import AddFavView,AddCommentView

app_name = 'operation'

urlpatterns = [

    # 用户收藏学院
    path('add_fav/', AddFavView.as_view(), name='add_fav'),
    # 添加课程评论
    path('add_comment/', AddCommentView.as_view(), name='add_comment'),
]