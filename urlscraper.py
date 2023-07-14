import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

baseurl = "https://www.amazon.in/"  

url = input("Enter the URL to scrape: ")
if url.startswith("http"):
    baseurl = url.split("/", 3)[2]
else:
    baseurl = url.split("/", 1)[0]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
productlinks = []
data = []

while url:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    productlist = soup.find_all("li")

    for product in productlist:
        link = product.find_all('a').get('href')
        productlinks.append(baseurl + link)

    next_link = soup.find('a', {'rel': 'next'})
    url = baseurl + next_link['href'] if next_link else None

for link in productlinks:
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    name = soup.find("h1").text.strip() if soup.find("h1") else None

    price_tag = soup.find("span", {"class": "price"})
    price = price_tag.text.strip() if price_tag else None

    rating_tag = soup.find("div", {"class": "rating"})
    rating_text = rating_tag.text.strip() if rating_tag else None
    rating_match = re.search(r'\d+(\.\d+)?', rating_text)
    rating = float(rating_match.group()) if rating_match else None

    about_tag = soup.find("div", {"class": "description"})
    about = about_tag.text.strip() if about_tag else None

    product_data = {"name": name, "price": price, "rating": rating, "about": about}
    data.append(product_data)

df = pd.DataFrame(data)
print(df)


