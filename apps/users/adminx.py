import xadmin
from xadmin import views


class BaseSetting(object):

    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):

    site_title = "hustle"
    site_footer = 'hustle every day'
    menu_style = "accordion"


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)