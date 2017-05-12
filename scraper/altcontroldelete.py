# -*- coding: utf-8 -*-
from datetime import datetime, date, time
from bs4 import BeautifulSoup
import requests



def data():
	span = 'cze\n09\n2014'
	print( span.replace('\n', ' '))
				
def tagfunc():
	count = 1 
	var = 1
	page = requests.get("http://www.altcontroldelete.pl/kategoria/index/21/")
	soup = BeautifulSoup(page.content, 'lxml')

	altcontroldelete=soup.find_all('article')
	for i in altcontroldelete:
		if i.header is None:
			pass
		else:
			print("------------------------------------------------")
			span = i.find(class_="article-header-3d").ul.li.span.text
			a, b = span.split("autor:")
			
			print("Autor: "+ b.strip())
			print("TYTUŁ: "+ i.find(class_="article-header-3d").h1.a.text)
			x = i.find(class_="article-header-3d").ul.text
			a,b = x.split("Tagi:")
			c,d = b.split("Odsłony:")
			print("TAGI: "+ c.strip())
			print("DATA: " + i.find(class_="article-header-date").text.replace('\n', ' '))
			print("Tekst: " + i.find(class_="article-context").text)
			print("Link: " + i.find(class_="article-header-1d").a['href'])
			print("Obrazek: " + i.find(class_="article-header-1d").a.img['src'])
			


tagfunc()
#data()
