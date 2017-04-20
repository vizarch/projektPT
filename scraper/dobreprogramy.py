# -*- coding: utf-8 -*-
from datetime import datetime, date, time
from bs4 import BeautifulSoup
import requests


def datefunc():
	count = 1

	chooseDateFrom = "01.04.2017" # data od w formacie DD.MM.RRRR
	chooseDateTo = "09.04.2017"   # data do w formacie DD.MM.RRRR

	cDFd, cDFm, cDFy = chooseDateFrom.split(".")  # dzien, miesiac, rok
	cDTd, cDTm, cDTy = chooseDateTo.split(".")


	cDateFrom = date(int(cDFy), int(cDFm), int(cDFd)) # konwersja na typ date
	cDateTo = date(int(cDTy), int(cDTm), int(cDTd))

	var = 1
	while var == 1 :
		b = "https://www.dobreprogramy.pl/Blog," + str(count) + ".html"
		page = requests.get(b)
		soup = BeautifulSoup(page.content, 'lxml')

		dobreprogramy=soup.find_all('article')
		for i in dobreprogramy:
			if i.header is None:
				pass
			else:
				datetim = i.find(class_="content-info").time.text  # data z artykulu
				dat, hour = datetim.split(" ")					# oddzielenie daty od godziny
				a,b,c = dat.split(".")
				d = date(int(c), int(b), int(a))

				if d > cDateTo:
					continue

				elif d <= cDateTo and d >= cDateFrom:

					print("------------------------------------------------")
					print("TYTUŁ: "+ i.header.h1.a.text)
					print("AUTOR: " + i.find(class_="content-info").find('a', rel='author').text)
					link = i.header.h1.a['href']
					print("LINK: " + link)
					print("DATA: " + datetim)
					print("TEKST: " + i.find(class_="entry-content").text)
					page1 = requests.get(link)
					soup1 = BeautifulSoup(page1.content, 'lxml')

					artykul = soup1.find(class_='tags font-heading-master')
					tagi = [i.text for i in artykul.find_all('a')]
					print("TAGI: " + ', ' .join(tagi))

				elif d < cDateFrom:
					var = 0

		count = count + 1  # przejscie do nastepnej strony

def tagfunc():
	page = requests.get("https://www.dobreprogramy.pl/Blog.html")
	soup = BeautifulSoup(page.content, 'lxml')

	dobreprogramy=soup.find_all('article')
	for i in dobreprogramy:
		if i.header is None:
			pass
		else:
			print("------------------------------------------------")
			print("TYTUŁ: "+ i.header.h1.a.text)
			print("AUTOR: " + i.find(class_="content-info").find('a', rel='author').text)
			link = i.header.h1.a['href']
			print("LINK: " + link)
			print("DATA: " + i.find(class_="content-info").time.text)
			print("TEKST: " + i.find(class_="entry-content").text)

			page1 = requests.get(link)
			soup1 = BeautifulSoup(page1.content, 'lxml')

			artykul = soup1.find(class_='tags font-heading-master')
			tagi = [i.text for i in artykul.find_all('a')]
			print("TAGI: " + ', ' .join(tagi))

datefunc()
#tagfunc()
