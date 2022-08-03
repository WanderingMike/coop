#!/usr/bin/python3
import requests
#from bs4 import BeautifulSoup
import re
#from requests_html import HTMLSession
from pprint import pprint
from yattag import Doc
import json
from datetime import datetime as dt
from anytree import Node, NodeMixin, RenderTree
from anytree.search import findall_by_attr, findall, find
from anytree.exporter.dictexporter import DictExporter
from anytree.importer import DictImporter


class Item(Node):

    def __init__(self):
        self.items = dict()
        self.saving = float()
        self.price = float()
        self.savingText = str()
        self.udoCat = list()
        self.image = str()
        self.percentage = float()
        self.min_purchase = int()
        self.tag = str()

    def sanitise(self):
        self.name = self.items["title"].lower()
        self.tag = "product"
        self.saving = self.items["saving"]
        self.price = self.items["price"]
        self.savingText = self.items["savingText"]
        if not self.savingText:
            self.savingText = "Special bonus at price %s" % (self.price)
        self.udoCat = self.items["udoCat"]
        self.image = "https:" + self.items["image"]["srcset"][-1][0]
        self.percentage, self.min_purchase = match_text(self.savingText)
        if not self.savingText:
            self.savingText = "Sale"
        print(self.name)
        print(self.percentage)
        print(self.min_purchase)
        print(self.saving)
        print(self.price)
        print(self.savingText)

    def clean_title(self, string):
        string.lower()


def match_text(text):
    if match:= re.findall(r"([0-9]) for ([0-9])", text):
        return int(match[0][1])/int(match[0][0]), 0

    elif match:= re.findall(r"([0-9]+)% (on|per|ab) ([0-9])*.?", text):
        return int(match[0][0])/100, int(match[0][2])

    elif match:= re.findall(r"([0-9]+)% ([0-9]) or more", text):
        return int(match[0][0])/100, int(match[0][1]) 

    elif match:= re.findall(r"([0-9]+)%", text):
        return int(match[0])/100, 0
    else:
        return 0.5, 0
 

def read_html_file():
    with open("files/webpage.txt", encoding="utf-8") as f:
        text = f.read()
    return text


def strip(text):
    pattern = r"<meta data-pagecontent-json='(.*?)'>"
    match=re.findall(pattern, text)
    json_data = json.loads(match[0])
    anchors = json_data["anchors"]
    return anchors


def populate_product(product):

    obj = Item()

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
    

def make_title(title, promotion):

    try:
        return "{} ({})".format(title, promotion)
    except:
        return title


def build_tree(products):
   
    ### Import skeleton
    if False:
        tree = Item()
        tree.name = "Coop"
        tree.tag = "branch"
    else:
        importer = DictImporter()
        with open("convert.json") as importf:
            raw_tree = json.load(importf)
        tree = importer.import_(raw_tree)

    ### Add current deals to tree
    for product in products:

        HEAD = tree

        try:
            node = populate_product(product) 
            if find(HEAD, lambda tmp: tmp.name == node.name):
                continue
            edges = node.udoCat
 
            for edge in edges:
            
                if (answer := findall_by_attr(HEAD, edge)):
                    HEAD = answer[0]

                else:
                    new_node = Item()
                    new_node.name = edge
                    new_node.tag = "branch"
                    new_node.parent = HEAD
                    HEAD = new_node
            
           # product_title = make_title(obj.title, obj.savingText)
            node.parent = HEAD


        except Exception as e:

            print("We get the following error for product", e)
            return None
    
    ### Print tree
    for pre, fill, node in RenderTree(tree):
        print("%s%s" % (pre, node.name))

    ### Export skeleton
    exporter = DictExporter(childiter=lambda children: [child for child in children if child.tag=="branch"])
    saved_tree = exporter.export(tree)

    with open('convert.json', 'w') as convert_file:
         convert_file.write(json.dumps(saved_tree))

    return tree


def extract_keys(filename):
    with open("files/{}".format(filename)) as f:
        inpt = f.read()

    exprs_pattern = r'"(.*?)"'
    exprs = re.findall(exprs_pattern, inpt)
    re.sub(r'"(.*?)"', "", inpt)
    single_words = re.split(r"\t|\n| ", inpt)
    keywords = single_words + exprs
    keywords = [word for word in keywords if word not in ["", " "]]

    return keywords


def check_ancestors(ancestors, baskets):
    for ancestor in ancestors:
        if ancestor.name in baskets:
            return True

    return False


def query_filter(tree):

    ## based on keywords
    keywords = extract_keys("keywords.txt")
    selected_objects = findall(tree, lambda node: any(keyword for keyword in keywords if keyword in node.name))

    ## based on high discounts
    big_whales = findall(tree, lambda node: node.tag == "product" and node.percentage > 0.3 and node.min_purchase < 2)

    ## based on categories
    basket_ids = extract_keys("baskets.txt")
    baskets = findall(tree, lambda node: node.tag == "product" and check_ancestors(node.ancestors, basket_ids))

    return selected_objects, big_whales, baskets


def display_products(objects, filename, title):
    doc, tag, text = Doc().tagtext()
    with tag('html'):
            with tag('body'):
                with tag('h1', id = 'main'):
                    text(title)
                    with tag('h3'):
                        for obj in objects:
                            with tag('p'):
                                text(obj.name)
                            with tag('p'):
                                text(obj.savingText)
                                try:
                                    text("\nCHF ", obj.price)
                                except:
                                    continue
                            try:
                                with tag('img', src=obj.image):
                                    continue
                            except:
                                continue
    with open('{}.html'.format(filename), 'w') as f:
        f.write(doc.getvalue())


def display_tree(tree):

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
                

def main_loop():
    #if is_monday():
    #    garbage_leaves()

    offline = False
    if offline:
        lines = read_html_file()
        content = strip(lines)
    else:
        url = "https://www.coop.ch/en/promotions/weekly-special-offers/c/m_1011"
        session = requests.get(url)
        content = strip(session.text)

    product_content=list()
    for category in content:
        product_content += category["json"]["elements"]
    tree = build_tree(product_content)
    selected, whales, cats = query_filter(tree)

    display_products(selected, filename="selection", title="Your wishlist")
    display_products(whales, filename="whales", title="$$$ Big discounts $$$")
    display_products(cats, filename="basket", title="Your baskets are offering...")
    display_tree(tree)


if __name__=="__main__":
    main_loop()







###########################################################
def is_monday():
    return True if dt.weekday(dt.now()) == 0 else False


def garbage_leaves():
    """Go through all nodes and delete all product leaf nodes."""
    ##for every node, if tag is product, then prune









