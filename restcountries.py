import requests
import json
import os
from bs4 import BeautifulSoup as bs


class RestCountries():
    
    def get_info(self, country):
        url = f'https://restcountries.com/v3.1/name/{country}'
        file_path = f'{country}.txt'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                res = json.load(f)
        else:
            res = requests.get(url)
            res = res.json()
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(res, f, ensure_ascii=False, indent = 4)
        res = f"""
'Country': {res[0]['name']['official']},
'Capital': {res[0]['capital'][0]},
'Flag':    {res[0]['flags']['png']}
"""
        print(res)
    
    def __call__(self, country):
        return self.get_info(country)



class EbayGoods():
    def get_info(self, url):
        r = requests.get(url)
        soup = bs(r.text, 'html.parser')

        contents = soup.find_all('div', class_='right-summary-panel-container vi-mast__col-right')
        name = contents[0].find('span', class_='ux-textspans ux-textspans--BOLD').text
        price = contents[0].find('div', class_='x-price-primary').text
        photo = soup.find('div', attrs={'data-idx': 0})
        photo = photo.find('img')['src']
        seller = soup.find('div', class_='d-stores-info-categories__container__info__section')
        seller = seller.find('span', class_='ux-textspans ux-textspans--BOLD').text
        contents = soup.find_all('div', class_='ux-labels-values__values-content')
        delivery_price = contents[0].find_all('span')[0].text
        
        res = f"""
Name: {name},
Photo: {photo},
Link: {url},
Price: {price},
Seller: {seller}
Delivery: {delivery_price}
"""
        print(res)

    def __call__(self, url):
        return self.get_info(url)


r = RestCountries()
r('Ukraine')
        
goods = EbayGoods()
goods('https://www.ebay.com/itm/403962915270')


