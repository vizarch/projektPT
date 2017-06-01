# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import threading
from pytz import timezone
import queue

ARTICLES = queue.Queue()
END = False

def niebezpiecznik_date2_python_date(date):
    a, b, c = date.split("\n")
    
    if "." in c:
        day, month, year = c.split(".")
    elif "/" in c:
        day, month, year = c.split("/")
    else:
        raise
    
    if len(month) == 1:
        month = str(0) + month
    if len(day) == 1:
        day = str(0) + day
    year = year[0:-1]

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
        webpage = requests.get("https://niebezpiecznik.pl/page/" + str(page) + "/")
        soup = BeautifulSoup(webpage.content, 'lxml')

        print("Page: " + str(webpage.url))

        niebezpiecznik = soup.find_all(class_="post")
        for i in niebezpiecznik:
            try:
                title = i.find(class_="title").h2.a.text
                link = i.find(class_="title").h2.a['href']
                date = i.find(class_="date").text
                date = niebezpiecznik_date2_python_date(date)
                text = i.find(class_="entry").p.text
                temp_tags = i.find(class_="postmeta").text
                a, tags = temp_tags.split("Tagi:")
                author = a.split()[1:3]
                try:
                    image_link = i.find(class_="entry").a.img['src']
                except:
                    image_link = "http://www.ipblog.pl/wp-content/uploads/2013/12/niebezpiecznik-logotyp-e1387270249671.png"
            except:
                print("Error:", link)
                continue

            if author[0] == "redakcja":
                author = "niebezpiecznik.pl"
            else:
                author = ' '.join(author)

            tags = [tag for tag in tags.split(",")]
            tags_list = []
            for tmp in tags:
                tmp = tmp.lower()
                tmp = tmp.replace("\n", "").replace("\xa0","")
                if tmp[0] == " ":
                    tmp = tmp[1:]
                if tmp[-1] == " ":
                    tmp = tmp[:-1]

                tags_list.append(tmp)

            one_article = {"title": title, "date": date, "author": author, "link": link,
                           "tags": tags_list, "text": text, "image_link": image_link}
            ARTICLES.put(one_article)

def test():
    while not ARTICLES.empty():
        i = ARTICLES.get()
        print(i['date'])

def scrapshot(pages):
    global END
    main_articles(pages)
    END = True

if __name__ == "__main__":
    scrapshot(pages)
