#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re
from requests_html import HTMLSession
import pprint
import json

class Product(price, saving, title, savingText, categories):
    self.def __init__:
        1

def download_data(url):
    session = requests.get(url)
    pattern = r"<meta data-pagecontent-json='(.*?)'>"
    match=re.findall(pattern, session.text)
    json_data = json.loads(match[0])
    anchors = content["anchors"]
    return anchors
    

def product_pointers(data, pointers)
    # We need the title, the title, the original price, the new price, the saving text, the categories and the image 
    for main_cat in range(len(data["anchors"])):

        products = data[main_cat]["json"]["elements"]

        for product in products:

            product_obj = populate_product(product) 
            pointers[product_obj.title] = product_obj




def populate_product():

    obj = Product()

    for k,v in product.items():
        if k in ["title", "saving", "price", "savingText", "udoCat"]:
            print(v)







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
