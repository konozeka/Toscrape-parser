import requests
from bs4 import BeautifulSoup
import csv
#Адрес страницы
URL = "http://books.toscrape.com/"
#Заголовки, чтобы сайт не подумал на бота
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"} 
# 1. Делаем запрос и получаем HTML
response = requests.get(URL, headers=HEADERS)
response.encoding = 'utf-8'
# 2. Парсим HTML
soup = BeautifulSoup(response.text, "html.parser")
# 3. Ищем все карточки книг
books = soup.find_all("article", class_="product_pod")

data = []

for book in books:
    #Название книги (в атрибуте title у ссылки)
    title = book.find("h3").find("a")["title"]
    # Цена (в теге с классом price_color)
    price = book.find("p", class_ = "price_color").text.strip()
    # Наличие (в теге с классом instock availability)
    stock = book.find("p", class_ = "instock availability").text.strip()
    data.append({
        "title" : title,
        "price" : price,
        "stock" : stock
    })

#Сохраняем в csv
with open("books.csv", "w", newline = "", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "stock"])
    writer.writeheader()
    writer.writerows(data)

print(f"Готово! Собрано {len(data)} книг. Файл: books.csv")