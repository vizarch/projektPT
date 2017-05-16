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
        "stycznia": '01',
        "lutego": '02',
        "marca": '03',
        "kwietnia": '04',
        "maja": '05',
        "czerwca": '06',
        "lipca": '07',
        "sierpnia": '08',
        "września": '09',
        "października": '10',
        "listopada": '11',
        "grudnia": '12'
    }
    return months.get(month)

def sekurak_date2_python_date(date):
    # change datetime from articles to database datetime format
    date = date.split()
    day = date[0]
    month = month2int(date[1])
    year = date[2][0:-1]  # remove the last sign - comma
    time_ = date[3]
    time_ = time_.split(":")
    hours = time_[0]
    minutes = time_[1]
    together = day + " " + month + " " + year + " " + hours + ":" + minutes
    try:
        datetime_object = datetime.strptime(together, '%d %m %Y %H:%M')
        datetime_object = datetime_object.replace(tzinfo=timezone('Europe/Warsaw'))
    except ValueError:
        raise
    return datetime_object


def main_articles(pages):
    global ARTICLES
    for page in range(1,pages+1):
        webpage = requests.get('https://sekurak.pl/page/'+str(page))
        soup = BeautifulSoup(webpage.text, 'lxml')

        # start scraping
        sekurak = soup.find_all('article')

        #  main page articles
        print("MAIN: " + str(webpage.url))
        for i in sekurak:
            try:
                title = i.find(class_="postTitle").text
                date = ' '.join(i.find('div', class_='meta').text.split()[0:4])
                date = sekurak_date2_python_date(date)
                link = i.find(class_="postTitle").a['href']

                tmp = requests.get(link)  # have to open page for scrap all tags
                soup2 = BeautifulSoup(tmp.text,'lxml')
                tags = ', '.join([i.text for i in soup2.article.find_all('div',class_='meta')[1].find_all('a')])
                text = i.p.text
            except:
                print("Error MAIN")
                continue
            try:
                image_link = i.find('div',class_='entry excerpt').img['src']
            except:
                image_link = "http://www.securitum.pl/logo_sekurak.png"

            one_article = {"title": title, "date": date, "link": link,"tags":tags, "image_link": image_link, "text":text}
            ARTICLES.put(one_article)

def w_biegu_articles(pages):
    global ARTICLES
    for page in range(1, pages+1):
        webpage = requests.get('https://sekurak.pl/wbiegu/page/'+str(page))
        soup = BeautifulSoup(webpage.text,'lxml')

        # start scraping
        sekurak = soup.find_all('article')

        # w biegu
        print("W BIEGU: " + str(webpage.url))
        for i in sekurak:
            try:
                title = i.find(class_="postTitle").text
                date = ' '.join(i.find('div', class_='meta').text.split()[0:4])
                date = sekurak_date2_python_date(date)
                link = i.find(class_="postTitle").a['href']

                tmp = requests.get(link)
                soup2 = BeautifulSoup(tmp.text,'lxml')
                tags = ','.join([i.text for i in soup2.article.find_all('div',class_='meta')[1].find_all('a')])
                text = i.p.text
            except:
                print("Error W BIEGU")
                continue
            
            image_link = "http://www.securitum.pl/logo_sekurak.png"  # w biegu nie maja obrazka
            one_article = {"title": title, "date": date, "link": link,"tags":tags, "image_link": image_link, "text":text}
            ARTICLES.put(one_article)


def scrapshot(pages):
    global END
    # pages = How many pages will be scraped
    tmp1 = threading.Thread(target=main_articles, args=(pages,))
    tmp1.start()
    tmp2 = threading.Thread(target=w_biegu_articles, args=(pages,))
    tmp2.start()

    tmp1.join()
    tmp2.join()

    END = True


if __name__ == "__main__":
    scrapshot(pages)