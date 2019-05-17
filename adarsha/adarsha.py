# From:
# https://adarsha.dharma-treasure.org/api/kdbs/degetengyur/pbs?size=100&lastId=2308063
# To:
# https://adarsha.dharma-treasure.org/api/kdbs/degetengyur/pbs?size=100&lastId=2422561


# Import libraries
import requests
import time
from bs4 import BeautifulSoup

# Set the URL you want to webscrape from
base = 'https://adarsha.dharma-treasure.org/api/kdbs/{name}/pbs?size=100&lastId={pbs}'

# [collection, starting pbs, ending pbs]
# collection = ['degetengyur', 2308063, 2422561]
collection = ['mipam', 1489993, 1511471]
# collection = ['jiangkangyur', 2561410, 2629691]

# TODO Catalog: get all the names from the section "kdbs":[{"id":... on https://adarsha.dharma-treasure.org/kdbs/
# TODO TOC: ge the json between "sidebar":{"data": and `],"open":false}], ... "sidebarOff":true
# TODO Texts: loop throught the pbs to get collection content in json
# TODO Volumes: parse text json and extract text and vol/line info


# put the collection in a json
i = collection[1]
while i <= collection[2]:
    url = base.format(name=collection[0], pbs=i)
    # Connect to the URL
    response = requests.get(url)
    text = response.text.replace("},{", "},\n{")
    with open("adarsha/"+collection[0]+".json", "a+") as f:
        f.write(text)
    print(f'pbs: {i}')
    f.close
    i += 100


