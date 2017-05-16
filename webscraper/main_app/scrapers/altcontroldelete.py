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
    "Jan": '01',
    "Feb": '02',
    "Mar": '03',
    "Apr": '04',
    "May": '05',
    "Jun": '06',
    "Jul": '07',
    "Aug": '08',
    "Sep": '09',
    "Oct": '10',
    "Nov": '11',
    "Dec": '12'
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
		datetime_object = ""
	return datetime_object
	
def main_articles(pages):
	global ARTICLES
	for page in range(1, pages + 1):
		webpage = requests.get("http://www.altcontroldelete.pl/kategoria/index/" + str(page) +"/")
		soup = BeautifulSoup(webpage.content, 'lxml')
		
		print("Page: " + str(webpage.url))
		# start scraping
		altcontroldelete=soup.find_all('article')
		for i in altcontroldelete:
			if i.header is None:
				pass
			else:
				title = i.find(class_="article-header-3d").h1.a.text
				
				span = i.find(class_="article-header-3d").ul.li.span.text
				a, b = span.split("autor:")
				author = b.strip()
				
				link = i.find(class_="article-header-1d").a['href']
				date = i.find(class_="article-header-date").text.replace('\n', ' ')
				date = altcontroldelete_date2_python_date(date)
				text = i.find(class_="article-context").text
				
				ul = i.find(class_="article-header-3d").ul.text
				kat,tg = ul.split("Tagi:")
				tagi, ods = tg.split("Odsłony:")
				tags = tagi.strip()
				imageLink = i.find(class_="article-header-1d").a.img['src']
				
				one_article = {"title" : title, "date": date, "author" : author, "link":link,
				"tags":tags, "text":text, "imageLink": imageLink}
				
				ARTICLES.put(one_article)
				

def scrapshot(pages):
	global END
	main_articles(pages)
	END = True
	
if __name__ == "__main__":
	scrapshot(pages)