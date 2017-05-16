# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import threading  # for save time, it's half shorter than sequentially
from pytz import timezone  # python timezones
import queue

ARTICLES = queue.Queue()
END = False


def month2int(month):
    month = month.lower()
    months = {
        "sty": '01',
        "lut": '02',
        "mar": '03',
        "kwi": '04',
        "maj": '05',
        "cze": '06',
        "lip": '07',
        "sie": '08',
        "wrz": '09',
        "paź": '10',
        "lis": '11',
        "gru": '12'
    }
    return months.get(month)

def altcontroldelete_date2_python_date(date):
    date = date.split()
    day = date[1]
    month = month2int(date[0])
    year = date[2]
    together = day + " " + month + " " + year
    try:
        datetime_object = datetime.strptime(together, '%d %m %Y')
        datetime_object = datetime_object.replace(tzinfo=timezone('Europe/Warsaw'))
    except ValueError:
        raise
    return datetime_object

def main_articles(pages):
    global ARTICLES
    for page in range(1, pages + 1):
        webpage = requests.get("http://www.altcontroldelete.pl/kategoria/index/" + str(page) +"/")
        soup = BeautifulSoup(webpage.content, 'lxml')

        print("Page: " + str(webpage.url))
        # start scraping
        altcontroldelete = soup.find_all('article')
        for i in altcontroldelete:
            if i.header is None:
                pass
            else:
                try:
                    title = i.find(class_="article-header-3d").h1.a.text
                    link = i.find(class_="article-header-1d").a['href']
                    date = i.find(class_="article-header-date").text.replace('\n', ' ')
                    date = altcontroldelete_date2_python_date(date)
                    text = i.find(class_="article-context").text
                    ul = i.find(class_="article-header-3d").ul.text
                    kat, tg = ul.split("Tagi:")
                    tagi, ods = tg.split("Odsłony:")
                    tags = tagi.strip()
                except:
                    print("Error")
                    continue

                try:
                    span = i.find(class_="article-header-3d").ul.li.span.text
                    a, b = span.split("autor:")
                    author = b.strip()
                except:
                    author = "controlaltdelete"

                try:
                    image_link = i.find(class_="article-header-1d").a.img['src']
                except:
                    image_link = "http://img.altcontroldelete.pl/gfx/logo.png"

                one_article = {"title": title, "date": date, "author": author, "link":link,
                "tags":tags, "text":text, "image_link": image_link}

                ARTICLES.put(one_article)


def scrapshot(pages):
    global END
    main_articles(pages)
    END = True

if __name__ == "__main__":
    scrapshot(pages)