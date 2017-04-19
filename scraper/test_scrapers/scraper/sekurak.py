# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import threading  # na watkach wychodzi o polowe szybciej, sprawdzilem :)

# dwie listy, zawierajace slowniki z kluczami: title, date, link, tags, image, text
ART_1 = []  # artykulu ze strony glownej
ART_2 = []  # artykuly z zakladki 'w biegu'

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
    # zamiana zapisu czasu z sekuraka na zapis czasu dla python i bazy danych
    date = date.split()
    day = date[0]
    month = month2int(date[1])
    year = date[2][0:-1]  # usuwa ostatni znak czyli przecinek
    time_ = date[3]
    time_ = time_.split(":")
    hours = time_[0]
    minutes = time_[1]
    together = day + " " + month + " " + year + " " + hours + ":" + minutes
    try:
        datetime_object = datetime.strptime(together, '%d %m %Y %H:%M')
    except:
        datetime_object = "ERROR"
    return datetime_object


def main_articles():
    # init parameters
    global ART_1
    webpage = requests.get('https://sekurak.pl')
    soup = BeautifulSoup(webpage.text, 'lxml')

    # start scraping
    sekurak = soup.find_all('article')
    articles = []

    #  main page articles
    #print("main articles")
    for i in sekurak:
        #print(sekurak.index(i))  # for help
        title = i.find(class_="postTitle").text
        date = ' '.join(i.find('div',class_='meta').text.split()[0:4])
        date = sekurak_date2_python_date(date)
        link = i.find(class_="postTitle").a['href']

        tmp = requests.get(link)  # have to open page for scrap all tags
        soup2 = BeautifulSoup(tmp.text,'lxml')
        tags = ','.join([i.text for i in soup2.article.find_all('div',class_='meta')[1].find_all('a')])
        image_link = i.find('div',class_='entry excerpt').img['src']
        text = i.p.text
        one_article = {"title": title, "date": date, "link": link,"tags":tags, "image_link": image_link, "text":text}
        articles.append(one_article)
    ART_1 = articles

def w_biegu_articles():
    # init parameters
    global ART_2
    r = requests.get('https://sekurak.pl/wbiegu/')
    soup = BeautifulSoup(r.text,'lxml')

    # start scraping
    sekurak = soup.find_all('article')
    articles = []

    # w biegu
    #print("w biegu")
    for i in sekurak:
        #print(sekurak.index(i))
        title = i.find(class_="postTitle").text
        date = ' '.join(i.find('div', class_='meta').text.split()[0:4])
        date = sekurak_date2_python_date(date)
        link = i.find(class_="postTitle").a['href']

        tmp = requests.get(link)
        soup2 = BeautifulSoup(tmp.text,'lxml')
        tags = ','.join([i.text for i in soup2.article.find_all('div',class_='meta')[1].find_all('a')])
        image_link = ""  # w biegu nie maja obrazka
        text = i.p.text
        one_article = {"title": title, "date": date, "link": link,"tags":tags, "image_link": image_link, "text":text}
        articles.append(one_article)
    ART_2 = articles


def scrapshot():
    tmp1 = threading.Thread(target=main_articles)
    tmp1.start()
    tmp2 = threading.Thread(target=w_biegu_articles)
    tmp2.start()

    tmp1.join()
    tmp2.join()

    all_articles = ART_1 + ART_2
    return all_articles


if __name__ == "__main__":
    scrapshot()