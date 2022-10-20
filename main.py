from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
import mysql.connector
import pickle
import threading
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

def fun(urls):
    for url in urls:
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        # price_and_stuff = {}
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
                quary=f"update table foods set price = {d[i]} where food_name = {i} "
        db.commit()
u1=urls[len(urls)//2:]
u2=urls[:len(urls)//2]

# print(u1,type(u2))
t1=threading.Thread(target=fun,args=(u1,))
t2=threading.Thread(target=fun,args=(u2,))
t1.start()
t2.start()
t1.join()
t2.join()
print("Adios")
db.close()
