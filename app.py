import csv
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json
import csv
filecsv=open("node_udemy_courses.csv","w",encoding="utf-8")
file=open("node_udemy_courses.json","w",encoding="utf-8")
csv_columns=['book name','book image','book link','book price','book instock availability']
file.write('\n')
data={}
for page in range(4):
    url=f"http://books.toscrape.com/catalogue/page-{page}.html"
    source=requests.get(url)
    soup=BeautifulSoup(source.content,"html.parser")
    books=soup.find_all('article',{'class':'product_pod'})
    prices=soup.find_all('p',{'class':'price_color'})
    instock_availability=soup.find_all('p',{'class':'instock availability'})
    writer = csv.DictWriter(filecsv, fieldnames=csv_columns)
    writer.writeheader()
    # print(prices)
    for book,price,instock in zip(books,prices,instock_availability):
        print(price.text,"\n")
        book_link=f"http://books.toscrape.com/catalogue/{book.a['href']}"
        book_name=book.img['alt']
        book_price=str(price.text).strip()
        img=book.find('img',{'class':'thumbnail'})
        instockAvailability=str(instock.text).strip()
        writer.writerow({'book name':book_name,'book image':img.get('src'),'book link':book_link,'book price':book_price,'book instock availability':instockAvailability})
        data['book name']=book_name
        data['book image']=img.get('src')
        data['book link']=book_link
        data['book price']=book_price
        data['book instock availability']=instockAvailability
        json_data=json.dumps(data,ensure_ascii=False)
        file.write(f"\n\"{page}\":")
        file.write(json_data)
        file.write(",")
file.write("}")       
filecsv.close()
file.close()
