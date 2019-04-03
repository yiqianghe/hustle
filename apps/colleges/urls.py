from django.urls import path
from .views import CollegesView,CollegeHomeView,AddFavView,CollegeCourseView,LecturerDetailView

app_name = 'colleges'

urlpatterns = [
    path('list/', CollegesView.as_view(), name='colleges_list'),
    # 学院首页
    path('<int:college_id>/<str:get_type>/', CollegeHomeView.as_view(), name='college_detail'),
    # 学院课程
    path('<int:college_id>/<str:get_type>/<int:course_id>/', CollegeCourseView.as_view(), name='college_course'),
    # 学院讲师
    path('lecturer/<int:lecturer_id>/', LecturerDetailView.as_view(), name='college_lecturer'),
    # 收藏学院
    path('add_fav/', AddFavView.as_view(), name='add_fav'),
]