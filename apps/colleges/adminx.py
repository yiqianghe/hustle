import xadmin

from .models import CollegeOrg,Teacher


class CollegeOrgAdmin(object):

    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'add_time']


class TeacherAdmin(object):

    list_display = ['college_org', 'name', 'work_years', 'address', 'points', 'click_nums', 'image', 'fav_nums', 'add_time']
    search_fields = ['college_org', 'name', 'work_years', 'address', 'points', 'click_nums', 'image', 'fav_nums']
    list_filter = ['college_org', 'name', 'work_years', 'address', 'points', 'click_nums', 'image', 'fav_nums', 'add_time']


xadmin.site.register(CollegeOrg, CollegeOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)