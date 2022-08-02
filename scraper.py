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
        self.items = dict()
        self.title = str()
        self.saving = float()
        self.price = float()
        self.savingText = str()
        self.udoCat = list()

    def sanitise(self):
        self.title = self.items["title"]
        self.saving = self.items["saving"]
        self.price = self.items["price"]
        self.savingText = self.items["savingText"]
        self.udoCat = self.items["udoCat"]

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
            except Exception as e:
                print(e, ", missing this value")

        return pointers


def populate_product(product):

    try:

        obj = Product()

        items = {"title": None,
                "saving": None,
                "price": None,
                "savingText": None,
                "udoCat": None}
                    
        for datapoint, value in product.items():
            if datapoint in items.keys():
                print(datapoint, value)
                items[datapoint] = value
                obj.items = items


        obj.sanitise()
        return obj

    except Exception as e:
        print(e)
        return None



def build_tree(pointers):

    coop = Node("Coop")

    for obj in pointers.values():
        edges = obj.udoCat
        print(edges)
        root = coop

        for edge in edges:
            # create edge if it doesn't exist yet
            # link product to the leaf
            print(root)
            if edge not in root.children:
                temp = Node(edge, parent=root, tag="branch")
                root = temp
            else findall_by_attr(edge

    for pre, fill, node in RenderTree(coop):
        print("%s%s" % (pre, node.name))


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
