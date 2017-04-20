from django.db import models


# glowne tabele
class User(models.Model):
    name = models.CharField(max_length=255)

class Sources(models.Model):
    Name = models.CharField(max_length=50, unique=True)

class Articles(models.Model):
    SourceID = models.ForeignKey(Sources, on_delete=models.CASCADE, null=True)
    Title = models.CharField(max_length=100)
    Author = models.CharField(max_length=50)
    Timestamp = models.DateTimeField()
    Tags = models.CharField(max_length=150)  # animal, nature, forest
    Text = models.TextField()
    Link = models.CharField(max_length=100, unique=True)
    ImageLink = models.URLField(max_length=100)

class Tags(models.Model):
    Name = models.CharField(max_length=50)

# tabele laczace
class ArticleTagMap(models.Model):
    TagID = models.ForeignKey(Tags, on_delete=models.CASCADE)
    ArticleID = models.ForeignKey(Articles, on_delete=models.CASCADE)

class SourceProfile(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    SourceID = models.ForeignKey(Sources, on_delete=models.CASCADE)

class TagsProfile(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    TagID = models.ForeignKey(Tags, on_delete=models.CASCADE)
