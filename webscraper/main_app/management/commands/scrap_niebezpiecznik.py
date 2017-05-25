# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from main_app.models import *
from main_app.scrapers import altcontroldelete
import threading

class Command(BaseCommand):
    help = 'Scrap niebezpiecznik.pl'

    def add_arguments(self, parser):
        parser.add_argument('pages', nargs=1, type=int, choices=range(1, 30), help='How many pages will be scraped')

    def handle(self, *args, **options):
        pages = options['pages'][0]

        # create new Source or find exist Source
        new_source = Sources(name="niebezpiecznik.pl")
        try:
            new_source.save()
        except IntegrityError:
            # Source exists, so find it
            new_source = Sources.objects.get(name="niebezpiecznik.pl")

        # run thread for scraper
        start = threading.Thread(target=niebezpiecznik.scrapshot, args=(pages,))
        start.start()

        # while queue has item or while END flag is set to False
        while not niebezpiecznik.ARTICLES.empty() or not niebezpiecznik.END:
            one_art = niebezpiecznik.ARTICLES.get()

            # if articles has no tags then skip
            if one_art['tags'] == "":
                continue

            # add Article
            art = Articles(sourceID=new_source, title=one_art['title'], author=one_art['author'], timestamp=one_art['date'],
                           tags=one_art['tags'], text=one_art['text'], link=one_art['link'],
                           imageLink=one_art['image_link'])
            try:
                art.save()
            except IntegrityError:
                continue  # skip this article

            # add Tags
            tags = one_art['tags'].split(",")
            for tmp_tag in tags:
                if tmp_tag[0] == " ":
                    tmp_tag = tmp_tag[1:]
                tag = Tags(name=str(tmp_tag))
                try:
                    tag.save()  # add tag if it's new
                except IntegrityError:
                    # because of unique constraint
                    # tag exists, so find it
                    tag = Tags.objects.get(name=str(tmp_tag))

                # connect Article to Tag
                mapping = ArticleTagMap(tagID=tag, articleID=art)
                mapping.save()

        start.join()  # make sure that thread finished