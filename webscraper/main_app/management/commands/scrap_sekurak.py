# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from main_app.models import *
from main_app.scrapers import sekurak
import threading

class Command(BaseCommand):
    help = 'Scrap sekurak.pl'

    def add_arguments(self, parser):
        parser.add_argument('pages', nargs=1, type=int, choices=range(1, 30), help='How many pages will be scraped')

    def handle(self, *args, **options):
        pages = options['pages'][0]

        # create new Source or find exist Source
        new_source = Sources(name="sekurak.pl")
        try:
            new_source.save()
        except IntegrityError:
            # Source exists, so find it
            new_source = Sources.objects.filter(Name="sekurak.pl")

        # run thread for scraper
        start = threading.Thread(target=sekurak.scrapshot, args=(pages,))
        start.start()

        # while queue has item or while END flag is set to False
        while not sekurak.ARTICLES.empty() or not sekurak.END:
            one_art = sekurak.ARTICLES.get()
            art = Articles(sourceID=new_source, title=one_art['title'], author="sekurak.pl", timestamp=one_art['date'],
                           tags=one_art['tags'], text=one_art['text'], link=one_art['link'],
                           imageLink=one_art['image_link'])
            try:
                art.save()
            except IntegrityError:
                pass  # TODO exception handler - entry exists
                # if 'UNIQUE constraint failed' in str(e):
                #    print("bee")

        start.join()  # make sure that thread finished