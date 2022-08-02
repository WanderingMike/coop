#!/usr/bin/python3
import requests
#from bs4 import BeautifulSoup
import re
#from requests_html import HTMLSession
#import pprint
import json
from datetime import datetime as dt
from anytree import Node, NodeMixin, RenderTree

class MyClass(NodeMixin): # Add Node feature ...
    def __init__(self, name, length, width, tag, parent=None):
        super(MyClass, self).__init__()
        self.name = name
        self.length = length
        self.width = width
        self.parent = parent
        self.tag = tag

class Product:
    '''Each discounted product becomes its own object'''

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


def strip(text):
    pattern = r"<meta data-pagecontent-json='(.*?)'>"
    match=re.findall(pattern, text)
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

        return pointers


def populate_product(product):
    
    try:

        obj = Product()

        for datapoint, value in product.items():
            if datapoint in ["title", "saving", "price", "savingText", "udoCat"]:
                exec("""obj.%s ="%s" """ % (datapoint, value))

        print(obj.udoCat)
        obj.sanitise()
        return obj

    except:
        return None



def build_tree(pointers):

    for obj in pointers:
        edges = obj.udoCat

        for edge in edges:
            # create edge if it doesn't exist yet
            # link product to the leaf
            print("Hello")


def read_html_file():
    with open("files/webpage.txt", encoding="utf-8") as f:
        text = f.read()
    return text


def is_monday():
    return True if dt.weekday(dt.now()) == 0 else False


def garbage_leaves():
    """Go through all nodes and delete all product leaf nodes."""
    ##for every node, if tag is product, then prune


if __name__=="__main__":
    input()
    if is_monday():
        print("yes")
        garbage_leaves()

    offline = True
    if offline:
        lines = read_html_file()
        content = strip(lines)
    else:
        url = "https://www.coop.ch/en/promotions/weekly-special-offers/c/m_1011"
        session = requests.get(url)
        content = strip(session.text)

    product_pointers_empty = dict()
    product_pointers = create_products(content, product_pointers_empty)
    build_tree(product_pointers)


















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
