#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re
from requests_html import HTMLSession
import pprint
import json

class Product:
    def __init__(self):
        self.title = str()
        self.saving = float()
        self.price = float()
        self.savingText = str()
        self.udoCat = list()

    def sanitise(self):
        print("sanitising")
        self.title = self.title
        print(self.saving)
        print(self.price)
        self.saving = float(self.saving)
        self.price = float(self.price)

    def clean_title(self, string):
        string.lower()

def download_data(url):
    session = requests.get(url)
    pattern = r"<meta data-pagecontent-json='(.*?)'>"
    match=re.findall(pattern, session.text)
    json_data = json.loads(match[0])
    anchors = json_data["anchors"]
    return anchors
    

def create_products(data, pointers):
    # We need the title, the title, the original price, the new price, the saving text, the categories and the image 
    for main_cat in range(len(data)):

        products = data[main_cat]["json"]["elements"]

        for product in products:

            try:
                product_obj = populate_product(product) 
                print(product_obj.title)
                pointers[product_obj.title] = product_obj
            except:
                print("missing this value")




def populate_product(product):
    
    try:
        obj = Product()

        for datapoint, value in product.items():
            if datapoint in ["title", "saving", "price", "savingText", "udoCat"]:
                exec("""obj.%s ="%s" """ % (datapoint, value))

        print(obj.title)
    except:
        print("missing {}".format(value))

    obj.sanitise()
    return obj
    






if __name__=="__main__":
    URL_coop = "https://www.coop.ch/en/promotions/weekly-special-offers/c/m_1011"
    content = download_data(URL_coop)
    product_pointers = dict()
    create_products(content, product_pointers)

















#session = HTMLSession()
#r = session.get(URL)
#r.html.render()
#print(r.text)
#with open('readme.txt', 'w') as f:
#    f.write(r.text)
#print(r.html.search('cmsTeaserRow'))

#r.html.search("Watermelon")

#page = requests.get(URL)
#soup = BeautifulSoup(page.content, "html.parser")

#
#job_elements = soup.find_all("div", class_="product-carousel__stage")
#print(job_elements)
#
### delete <script> and <template> content
#pattern_script = r"(<script>.*?</script>)"
#pattern_template = r"<template>(.*?)</template>"
#
##match=re.findall(pattern_script, soup)
