# -*- coding: utf-8 -*-
from datetime import datetime, date, time
from bs4 import BeautifulSoup
import requests

				
def tagfunc():
	count = 1 
	var = 1
	page = requests.get("http://pclab.pl/news-1.html")
	soup = BeautifulSoup(page.content, 'lxml')

	pclab=soup.find_all(class_="element")
	for i in pclab:
		print("------------------------------------------------")
		print("LINK: http://pclab.pl" + i.find(class_="title").a['href'])
		print("TITLE" + i.find(class_="title").a.text)
		print("DATA: " + i.find(class_="info").text)
		print("TEXT: " + i.find(class_="text").p.text)
		print("TAGS : " + i.find(class_="tags")	.text)
		print("IMAGE: http://pclab.pl" + i.find(class_="text").a.img['src'])
		
tagfunc()

