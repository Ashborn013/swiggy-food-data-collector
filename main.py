from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
import mysql.connector
import pickle

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='swag'
)
mycoursor = db.cursor()

try:
    with open('urls.pkl', 'rb') as f:
        urls = pickle.load(f)
except:
    print("Give me the pickle")
    exit()

for url in urls:
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    price_and_stuff = {}
    item__price_list = doc.find_all(class_="rupee")
    item__name_list = doc.find_all(class_="styles_itemNameText__3ZmZZ")
    for i in range(len(item__name_list)):
        item__name_list[i] = item__name_list[i].text
        item__price_list[i] = float(item__price_list[i].text)
    d = dict(zip(item__name_list, item__price_list))
    for i in d:
        quary = f'insert into foods values("{i}",{d[i]});'
        try:
            mycoursor.execute(quary)
        except:
            pass
    db.commit()
db.close()
