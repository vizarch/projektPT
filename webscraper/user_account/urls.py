from django.conf.urls import url

from . import views

app_name = 'user_account'
urlpatterns = [
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^register/$', views.register_view, name='register_view'),
    url(r'^activate/(?P<activation_code>\w+)/$',views.activate,name='activate'),
    url(r'^$', views.user_profile, name='user_profile'),
    url(r'^change_password/$', views.change_password, name='change_password')
]

# pierwszy argument (regular expression r'') to adres widoczny dla uzytkownika
# jest niezalezny od name'a :)
