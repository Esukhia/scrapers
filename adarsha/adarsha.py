import re
import requests
from bs4 import BeautifulSoup


# Set the URL you want to webscrape from
base = 'https://adarsha.dharma-treasure.org/'
workBase = 'https://adarsha.dharma-treasure.org/kdbs/{name}'
apiBase = 'https://adarsha.dharma-treasure.org/api/kdbs/{name}/pbs?size=100&lastId={pbs}'


# TODO TOC: ge the json between "sidebar":{"data": and `],"open":false}], ... "sidebarOff":true
# TODO Texts: loop throught the pbs to get work content in json
# TODO Volumes: parse text json and extract text and vol/line info

# [work, starting pbs]
# work = ['degetengyur', 2308063]
work = ['mipam', 1489993]
# work = ['jiangkangyur', 2561410]

def testUrl(work, pbs):
# check if url has text
    url = apiBase.format(name=work[0], pbs=pbs)
    response = requests.get(url)
    if response.text == '{"total":0,"data":[]}':
        print(response.text)
        status = False
    else:
        status = True
    return status


def getwork(work=work):
# put the work in a json
    i = work[1]
    outPath = 'adarsha/'+work[0]+'_text.json'
    # Empty file if already existing
    open(outPath, 'w')

    while testUrl(work, i):
        url = apiBase.format(name=work[0], pbs=i)
        response = requests.get(url)
        text = response.text.replace("},{", "},\n{")

        with open(outPath, "a+", encoding='utf-8') as f:
            f.write(text)
        print(f'pbs: {i}')
        f.close
        i += 100

def getTOC(work):
    pass

def getCatalog(rawCatalog):
    pass


def getRawCatalog():
# TODO Catalog: get all the names from the section "kdbs":[{"id":... on https://adarsha.dharma-treasure.org/kdbs/

# get general catalog
    text = requests.get(base).text
    catalogJson = re.search('"kdbs":(.+?),"kdbData":', text).group(1).replace("},{", "},\n{")
    with open('adarsha/'+'adharsha'+'_catalog.json', "w", encoding='utf-8') as f:
        f.write(catalogJson)
    return catalogJson



if __name__ == '__main__':
    getRawCatalog()




# word = """div class="name">
#                         Text_I_Want_To_Extract 
#                     </div>"""

# m = re.search('>(.+)<', word, flags=re.DOTALL)
# print (m.group(1).strip())