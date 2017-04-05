from bs4 import BeautifulSoup
import requests


r = requests.get('https://sekurak.pl')

soup = BeautifulSoup(r.text,'lxml')

sekurak=soup.find_all('article')
for i in sekurak:
	print("-------------------------------------------------------------------------------------------------------------")
	print("TYTUŁ: " + i.find(class_="postTitle").text)
	print("DATA: " + ' '.join(i.find('div',class_='meta').text.split()[0:4]))
	link = i.find(class_="postTitle").a['href']
	print("LINK: " + link)

	tmp = requests.get(link)
	soup2 = BeautifulSoup(tmp.text,'lxml')
	tags = [i.text for i in soup2.article.find_all('div',class_='meta')[1].find_all('a')]
	print("TAGS: " + ' '.join(tags))
	print("KATEGORIA: " + i.find('div',class_='meta').find('a',rel='tag').text)
	print("OBRAZEK: " + i.find('div',class_='entry excerpt').img['src'])
	print("TEKST:\n" + i.p.text)
	print("\n\n")