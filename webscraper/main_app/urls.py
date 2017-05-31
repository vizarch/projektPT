from django.conf.urls import url, include

from . import views

app_name = 'main_app'
urlpatterns = [
    url(r'^$', views.start_page, name='start_page'),
    url(r'^user_account/', include("user_account.urls", namespace="user_account")),
    url(r'^list/$', views.sources_and_tags, name='sources_and_tags'),
    url(r'^list/(?P<tag_id>[0-9]+)/$', views.sources_and_tags,name='sources_and_tags'),
    url(r'^search/$', views.search, name='search'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/del/(?P<profile_id>[0-9]+)/$', views.delete_profile, name='delete_profile'),
]