# Django specific settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
# Ensure settings are read
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Your application specific imports
from django.db import IntegrityError
from data.models import *
from scraper import sekurak


def sekurak_scraper():
    sekurak_articles = sekurak.scrapshot()
    for one_art in sekurak_articles:
        art = Articles(Source="sekurak.pl", Title=one_art['title'], Author="sekurak.pl", Timestamp=one_art['date'],
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
