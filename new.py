import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def extract_data_from_page(soup):
    productlinks = []
    t={}
    data = []
    productlist = soup.find_all("li")

    for product in productlist:
        link = product.find("a").get('href')
        productlinks.append(link)

    for link in productlinks:
        f = requests.get(link,headers=headers).text
        hun=BeautifulSoup(f,'html.parser')

        try:
            price=hun.find("p",{"class":["product-action__price", "product-price"]}).text.replace('\n',"")
        except:
            price = None

        try:
            about=hun.find("div",{"class":["product-main__description", "product-description"]}).text.replace('\n',"")
        except:
            about=None

        try:
            rating = hun.find("div",{"class":["review-overview", "product-rating"]}).text.replace('\n',"")
            rating = re.findall(r'\d+\.?\d*', rating)[0]
        except:
            rating=None

        try:
            name=hun.find("h1",{"class":["product-main__name", "product-name"]}).text.replace('\n',"")
        except:
            name=None

        whisky = {"name":name,"price":price,"rating":rating,"about":about}

        data.append(whisky)
        print("Scraped",name)

    return data

def scrape_all_pages(base_url):
    page_number = 1
    all_data = []

    while True:
        url = f"{base_url}?page={page_number}"
        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            data = extract_data_from_page(soup)
            all_data.extend(data)
            page_number += 1
        else:
            break

    return all_data

base_url = input("Enter the URL to scrape: ")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
