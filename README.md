# Projekt - Podstawy teleinformatyki
Webscrapper/Metawyszukiwarka

Wymagania:
- python 3.5
- Django 1.10.6

Instalacja Django:
- potrzebny jest menadżer pip
- pip install Django lub pip install Django==1.10.6 (jezeli chcemy wybrana wersje)
 (ale aktualnie najnowsza do 1.10.6 więc nie trzeba jej podawać)

Potem:
- wchodzimy do katalogu z projektem (poniżej robimy wszystko z użyciem python3.5)
- python manage.py runserver - serwer sie odpala na 127.0.0.1:8000
- czasami, po zmianach w bazie danych (models.py) bedzie trzeba zrobić: python manage.py migrate
- w przeglądarce pod adresem: 127.0.0.1:8000/admin jest panel admina
- login: admin, hasło: admin123
