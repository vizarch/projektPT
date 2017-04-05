from bs4 import BeautifulSoup
import requests

page = requests.get("https://www.dobreprogramy.pl/Blog.html")
soup = BeautifulSoup(page.content, 'lxml')

dobreprogramy=soup.find_all('article')
for i in dobreprogramy:
	if i.header is None:
		pass
	else:
		print("------------------------------------------------")
		print("TYTU£: "+ i.header.h1.a.text)
		print("AUTOR: " + i.find(class_="content-info").find('a', rel='author').text)
		link = i.header.h1.a['href']
		print("LINK: " + link)
		print("DATA: " + i.find(class_="content-info").time.text)
		print("TEKST: " + i.find(class_="entry-content").text)
		
		
		