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
	page = requests.get("https://niebezpiecznik.pl/page/2/")
	soup = BeautifulSoup(page.content, 'lxml')

	niebezpiecznik=soup.find_all(class_="post")
	for i in niebezpiecznik:
		print("------------------------------------------------")
		print("DATA: " + i.find(class_="date").text)
		print("TITLE: " + i.find(class_="title").h2.a.text)
		print("LINK: " + i.find(class_="title").h2.a['href'])
		print("IMAGE: " + i.find(class_="entry").a.img['src'])
		print("DATE: " + i.find(class_="date").text)
		postmeta = i.find(class_="postmeta").text
		a, tagi = postmeta.split("Tagi:")
		b, autor = a.split("Autor:")
		autor = autor.replace('|', '')
		print("TAGI: " + tagi)
		print("AUTHOR: " + autor)
		print("TEXT: " + i.find(class_="entry").p.text)
tagfunc()
#data()
def abc():
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