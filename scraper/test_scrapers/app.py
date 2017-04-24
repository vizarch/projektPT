# Django specific settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
# Ensure settings are read
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Your application specific imports
from django.db import IntegrityError
from data.models import *
from scraper import sekurak, dobreprogramy


def dobreprogramy_scraper():
    # dodanie nowego zrodla do bazy danych
    new_source = Sources(Name="dobreprogramy.pl")
    try:
        new_source.save()
    except IntegrityError as e:
        # zrodlo istnieje, wiec je wyszukaj
        new_source = Sources.objects.filter(Name="dobreprogramy.pl")

    dobreprogramy_articles = dobreprogramy.scrapshot()
    for one_art in dobreprogramy_articles:
        art = Articles(SourceID=new_source, Title=one_art['title'], author="author", Timestamp=one_art['date'],
                       Tags=one_art['tags'], Text=one_art['text'], Link=one_art['link'])
        try:
            art.save()
        except IntegrityError as e:
            pass  # TODO obsluga bledow UNIQUE - tzn. juz taki artykul jest
            #if 'UNIQUE constraint failed' in str(e):
            #    print("bee")


def sekurak_scraper():
    # dodanie nowego zrodla do bazy danych
    new_source = Sources(Name="sekurak.pl")
    try:
        new_source.save()
    except IntegrityError as e:
        # zrodlo istnieje, wiec je wyszukaj
        new_source = Sources.objects.filter(Name="sekurak.pl")

    sekurak_articles = sekurak.scrapshot()
    for one_art in sekurak_articles:
        art = Articles(SourceID=new_source, Title=one_art['title'], Author="sekurak.pl", Timestamp=one_art['date'],
                       Tags=one_art['tags'], Text=one_art['text'], Link=one_art['link'], ImageLink=one_art['image_link'])
        try:
            art.save()
        except IntegrityError as e:
            pass  # TODO obsluga bledow UNIQUE - tzn. juz taki artykul jest
            #if 'UNIQUE constraint failed' in str(e):
            #    print("bee")


def check():
    a = Articles.objects.all()
    print("---------------  CHECK   ---------------")
    for i in a:
        print(i.Title)


sekurak_scraper()
check()
