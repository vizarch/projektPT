# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from pytz import timezone  # python timezones
import queue

ARTICLES = queue.Queue()
END = False

def dobreprogramy_date2_python_date(date):
    date = date.split(".")  # [24, 04, 2017 1:27]
    day = date[0]
    month = date[1]
    date = date[2].split(" ")  # # [2017, 1:27]
    year = date[0]
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
        webpage = requests.get("https://www.dobreprogramy.pl/Blog,"+str(page)+".html")
        soup = BeautifulSoup(webpage.text, 'lxml')

        print("Page: " + str(webpage.url))
        # start scraping
        dobreprogramy = soup.find_all('article')
        for i in dobreprogramy:
            if i.header is None:
                continue
            else:
                try:
                    title = i.header.h1.a.text
                    link = i.header.h1.a['href']
                    date = i.find(class_="content-info").time.text
                    date = dobreprogramy_date2_python_date(date)
                    text = i.find(class_="entry-content").text
                    page1 = requests.get(link)  # have to open page for scrap all tags
                    soup1 = BeautifulSoup(page1.content, 'lxml')

                    artykul = soup1.find(class_='tags font-heading-master')
                    tags = [i.text for i in artykul.find_all('a')]
                except:
                    print("Error")
                    continue
                
                try:
                    author = i.find(class_="content-info").find('a', rel='author').text
                    page2 = requests.get("https://www.dobreprogramy.pl/"+author)
                    soup2 = BeautifulSoup(page2.content, 'lxml')
                    image = soup2.find_all("img", alt="avatar")
                    imagelink = image[0].attrs['src']
                except IndexError:
                    # I don't know why sometimes scraper can't find this img
                    imagelink = "https://static.dpcdn.pl/res/default.jpg"
                    if author is None:
                        author = "dobreprogramy"

                tags_list = []
                for tmp in tags:
                    tmp = tmp.lower()
                    tmp = tmp.replace("\n", "")
                    if tmp[0] == " ":
                        tmp = tmp[1:]
                    if tmp[-1] == " ":
                        tmp = tmp[:-1]

                    tags_list.append(tmp)

                one_article = {"title": title, "date": date, "author": author, "link": link,
                               "tags": tags_list, "text": text, "imageLink": imagelink}
                ARTICLES.put(one_article)

def test():
    while not ARTICLES.empty():
        i = ARTICLES.get()
        print(i['tags'])

def scrapshot(pages):
    global END
    main_articles(pages)
    END = True

if __name__ == "__main__":
    scrapshot(pages)
