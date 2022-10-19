from re import L
from bs4 import BeautifulSoup
import requests
import pickle

url = 'https://www.swiggy.com/restaurants/geetha-canteen-kalingarayan-street-ram-nagar-coimbatore-61498'
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")
item__new_url = doc.find_all(class_="_3TjLz b-Hy9")
l_cits = []
for i in item__new_url:
    l_cits.append(f'https://www.swiggy.com/city/{i.text}')


shop_curls = []
for url in l_cits:
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    shop_class_url = doc.find_all(href=True,class_='_1j_Yo')
    for i in shop_class_url:
        # print(i)
        the_we_url=i['href']
        shop_curls.append(f"https://www.swiggy.com{the_we_url}")
        print(shop_curls[-1])
    
    if len(shop_curls) > 100:
        break

with open('url_list.pkl', 'wb') as f:
    pickle.dump(shop_curls, f)
# for i in shop_curls:
#     print(i)