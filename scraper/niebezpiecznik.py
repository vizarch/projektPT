# -*- coding: utf-8 -*-
from datetime import datetime, date, time
from bs4 import BeautifulSoup
import requests

				
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
		date = i.find(class_="date").text
		a, b, c = date.split("\n")
		hours, minutes = b.split(":")
		day, month, year = c.split(".")
		print("DATE: " + "hour: " + hours + " minutes: " + minutes + " day: " + day + " month: " + month + " year: " + year)
		postmeta = i.find(class_="postmeta").text
		a, tagi = postmeta.split("Tagi:")
		b, autor = a.split("Autor:")
		autor = autor.replace('|', '')
		print("TAGI: " + tagi)
		print("AUTHOR: " + autor)
		print("TEXT: " + i.find(class_="entry").p.text)
tagfunc()

