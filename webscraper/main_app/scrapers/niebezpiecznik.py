from bs4 import BeautifulSoup
import  requests
from datetime import  datetime
import  threading
from  pytz import  timezone
import  queue

ARTICLES = queue.Queue()
END = False

def niebezpiecznik_date2_python_date(date):
    a, b, c = date.split("\n")
    day, month, year = c.split(".")
    together = day + " " + month + " " + year
    try:
        datetime_object = date.strptime(together, '%d %m %Y')
        datetime_object = datetime_object.replace(tzinfo=timezone('Europe/Warsaw'))
    except ValueError:
        raise
    return  datetime_object

def main_articles(pages):
    global ARTICLES
    for page in range(1, pages + 1):
        webpage = requests.get("https://sekurak.pl/page/" + str(page) + "/")
        soup = BeautifulSoup(webpage.content, 'lxml')

        print("Page: " + str(webpage.url))

        niebezpiecznik = soup.find_all(class_="post")
        for i in niebezpiecznik:
            try:
                title = i.find(class_="title").h2.a.text
                link = i.find(class_="title").h2.a['href']
                date = i.find(class_="date").text
                date = niebezpiecznik_date2_python_date(date)
                text = i.find(class_="entry").p.text
                tempTags = i.find(class_="postmeta").text
                a, tags = tempTags.split("Tagi:")
                b, author = a.split("Autor:")
                image_link = i.find(class_="entry").a.img['src']
            except:
                print("Error")
                continue

            one_article = {"title": title, "date" : "??????", "author": author, "link": link,
                           "tags": tags, "text": text, "image_link": image_link}
            ARTICLES.put(one_article)

def scrapshot(pages):
    global END
    main_articles(pages)
    END = True

if __name__ == "__main__":
    scrapshot(pages)
