from django.conf.urls import url, include

from . import views

app_name = 'main_app'
urlpatterns = [
    url(r'^$', views.start_page, name='start_page'),
    url(r'^user_account/', include("user_account.urls", namespace="user_account")),
    url(r'^list/', views.sources_and_tags,name='sources_and_tags'),
    url(r'^board/', views.board,name='board'),
    url(r'^profile/', views.profile,name='profile'),
]