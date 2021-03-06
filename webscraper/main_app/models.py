# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

# glowne tabele
class Sources(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "źródła"
        verbose_name = "źródło"

class Tags(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "tagi"
        verbose_name = "tag"

class Articles(models.Model):
    sourceID = models.ForeignKey(Sources, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    timestamp = models.DateField(null=True)
    tags = models.CharField(max_length=150)
    text = models.TextField()
    link = models.CharField(max_length=100, unique=True)
    imageLink = models.URLField(max_length=100)

    def __str__(self):
        return self.title

    def tags_list(self):
        return self.tags.split(",")

    class Meta:
        verbose_name_plural = "artykuły"
        verbose_name = "artykuł"

# tabele laczace
class ArticleTagMap(models.Model):
    tagID = models.ForeignKey(Tags, on_delete=models.CASCADE)
    articleID = models.ForeignKey(Articles, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "artykuły-tagi"
        verbose_name = "artykuł-tag"

# tabela dla profilu uzytkownika
class SearchProfiles(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    profileName = models.CharField(max_length=150)
    sources_list = models.TextField()
    tags_list = models.TextField()

    class Meta:
        verbose_name_plural = "profile wyszukiwania"
        verbose_name = "profil wyszukiwania"

