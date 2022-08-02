#!/usr/bin/python3
import requests
#from bs4 import BeautifulSoup
import re
#from requests_html import HTMLSession
#import pprinti
from yattag import Doc
import json
from datetime import datetime as dt
from anytree import Node, NodeMixin, RenderTree
from anytree.search import findall_by_attr

class Product:
    '''Each discounted product becomes its own object'''

    def __init__(self):
        self.items = dict()
        self.title = str()
        self.saving = float()
        self.price = float()
        self.savingText = str()
        self.udoCat = list()
        self.image = str()
        self.percentage = float()
        self.min_purchase = int()

    def sanitise(self):
        self.title = self.items["title"].lower()
        self.saving = self.items["saving"]
        self.price = self.items["price"]
        self.savingText = self.items["savingText"]
        self.udoCat = self.items["udoCat"]
        self.image = "https:" + self.items["image"]["srcset"][-1][0]
        print(self.image)
        print(self.title)
        print(self.saving)
        print(self.price)
        print(self.savingText)

    def clean_title(self, string):
        string.lower()


    

def create_products(data, pointers):
    # We need the title, the title, the original price, the new price, the saving text, the categories and the image 
    for main_cat in data:

        products = main_cat["json"]["elements"]

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
        print(product)
        obj = Product()

        items = {"title": None,
                "saving": None,
                "price": None,
                "savingText": None,
                "udoCat": None,
                "image": None}
                    
        for datapoint, value in product.items():
            if datapoint in items.keys():
                items[datapoint] = value
                obj.items = items

        obj.sanitise()
        return obj

    except Exception as e:
        print(e)
        return None

def make_title(title, promotion):
    try:
        return "{} ({})".format(title, promotion)
    except:
        return title



def build_tree(pointers):

    coop = Node("Coop")

    for obj in pointers.values():
        edges = obj.udoCat
        HEAD = coop

        for edge in edges:
            # create edge if it doesn't exist yet
            # link product to the leaf
            
            if (answer := findall_by_attr(coop, edge)):
                HEAD = answer[0]

            else:
                temp = Node(edge, parent=HEAD, tag="branch")
                HEAD = temp
        
        product_title = make_title(obj.title, obj.savingText)
        __product = Node(product_title, parent=HEAD, tag="product")

    for pre, fill, node in RenderTree(coop):
        print("%s%s" % (pre, node.name))

    return coop


def read_html_file():
    with open("files/webpage.txt", encoding="utf-8") as f:
        text = f.read()
    return text


def is_monday():
    return True if dt.weekday(dt.now()) == 0 else False


def garbage_leaves():
    """Go through all nodes and delete all product leaf nodes."""
    ##for every node, if tag is product, then prune

def query_filter():

    with open("files/keywords.txt") as f:
        inpt = f.read()

    exprs_pattern = r'"(.*?)"'
    exprs = re.findall(exprs_pattern, inpt)
    re.sub(r'"(.*?)"', "", inpt)
    single_words = re.split(r"\t|\n| ", inpt)
    keywords = single_words + exprs
    keywords = [word for word in keywords if word != " "]

    selected_objects = list()
    ## based on keywords
    for title in pointers.keys():
        for word in keywords:
            if word in title:
                product = pointers[title]
                selected_objects.append(product)

    ## based on high discounts
    big_whales = list()

    ## based on categories
    basket_selection = list()

    return selected_objects, big_whales, basket_selection


def display_products(objects, filename, title):
    doc, tag, text = Doc().tagtext()
    with tag('html'):
            with tag('body'):
                with tag('h1', id = 'main'):
                    text(title)
                    with tag('h3'):
                        for obj in objects:
                            with tag('p'):
                                text(obj.title)
                            with tag('p'):
                                text(obj.savingText)
                            with tag('img', src=obj.image):
                                text("Image")

    with open('{}.html'.format(filename), 'w') as f:
        f.write(doc.getvalue())


def display_tree(selected_objects, tree):

    doc, tag, text = Doc().tagtext()
    tree_struct = ""
    for pre, fill, node in RenderTree(tree):
        tree_struct += "%s%s\n" % (pre, node.name)


    with tag('html'):
        with tag('body'):
            with tag('h1', id = 'main'):
                text("All categories and current discounts")
            with tag('span', style = "white-space: pre"):
                text(tree_struct)

    result = doc.getvalue()

    with open('tree.html', 'w') as f:
        f.write(doc.getvalue())
                

def strip(text):
    pattern = r"<meta data-pagecontent-json='(.*?)'>"
    match=re.findall(pattern, text)
    json_data = json.loads(match[0])
    anchors = json_data["anchors"]
    return anchors

def main_loop():
    if is_monday():
        garbage_leaves()

    offline = False
    if offline:
        lines = read_html_file()
        content = strip(lines)
    else:
        url = "https://www.coop.ch/en/promotions/weekly-special-offers/c/m_1011"
        session = requests.get(url)
        content = strip(session.text)
        print(content)

    product_pointers_empty = dict()
    product_pointers = create_products(content, product_pointers_empty)
    tree = build_tree(product_pointers)
    selected, whales, cats = query_filter()

    display_products(selected, filename="selection", title="Your wishlist")
    display_products(whales, filename="whales", title="$$$ Big discounts $$$")
    display_products(cats, filename="basket", title="Your baskets are offering...")
    display_tree(tree)


if __name__=="__main__":
    main_loop()
















