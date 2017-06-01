# coding=utf-8
from django.contrib import admin
from .models import *

class SourcesAdmin(admin.ModelAdmin):
    model = Sources
    list_display = ('id','name')


class TagsAdmin(admin.ModelAdmin):
    model = Tags
    list_display = ('id', 'name')


class ArticlesAdmin(admin.ModelAdmin):
    model = Articles
    list_display = ('id', 'sourceID','title','author','timestamp','tags','text','link','imageLink')


class ArticleTagMapAdmin(admin.ModelAdmin):
    model = ArticleTagMap
    list_displat = ('id','tagID','articleID')

class SearchProfilesAdmin(admin.ModelAdmin):
    model = SearchProfiles
    list_display = ('id', 'userID', 'profileName','sources_list', 'tags_list')


admin.site.register(Sources, SourcesAdmin)
admin.site.register(SearchProfiles, SearchProfilesAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Articles,ArticlesAdmin)
admin.site.register(ArticleTagMap, ArticleTagMapAdmin)

