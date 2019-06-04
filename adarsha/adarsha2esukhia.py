import re
import shutil
import os
import requests
from bs4 import BeautifulSoup

base = 'https://adarsha.dharma-treasure.org/'
workBase = 'https://adarsha.dharma-treasure.org/kdbs/{name}'
apiBase = 'https://adarsha.dharma-treasure.org/api/kdbs/{name}/pbs?size=100&lastId={pbs}'

# [work, starting pbs]
work = ['degetengyur', 2308063]
# work = ['mipam', 1489993]
# work = ['jiangkangyur', 2561410]

outdir = f'adarsha/{work[0]}/'
if not os.path.exists(outdir):
    os.mkdir(outdir)


def item_generator(things):
    # because writelines() is such a tease
    for item in things:
        yield item
        yield '\n'

def writePage(page):
    lines = extractLines(page)
    formatedLines = formatLines(lines)

    fileName = "{:0>3d}".format(formatedLines.pop(0))

    with open(f'{outdir}{fileName}.txt', 'a+', encoding='utf-8') as file:
        file.writelines(item_generator(formatedLines))

def formatLines(lines):
    formatedLines = []

    volume = lines.pop(0)
    formatedLines.append(volume)

    page = lines.pop(0)
    side = lines.pop(0)
    formatedLines.append(f'[{page}{side}]')

    i = 1
    for line in lines:
        formatedLines.append(f'[{page}{side}.{i}]{line}')
        i += 1
    return formatedLines

def extractLines(page):
    # [volume, page, side, l1, ..., l7]
    lines = []
    volume = int(re.search('"pbId":"(\d+?)-', page).group(1))
    lines.append(volume)
    pageNum = int(re.search('"pbId":"\d+?-\d+?-(\d+?)[a-z]', page).group(1))
    lines.append(pageNum)
    side = re.search('"pbId":"\d+?-\d+?-\d+?([a-z])', page).group(1)
    lines.append(side)
    text = re.search('"text":"(.+?)"', page).group(1)
    text = re.sub('\s+', ' ', text)
    ls = list(filter(None, text.split('\\n')))
    lines += ls

    return lines

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
    # Empty file if already existing
    while testUrl(work, i):
        url = apiBase.format(name=work[0], pbs=i)
        response = requests.get(url)
        text = response.text.replace("},{", "},\n{")
        pages = text.splitlines()

        for page in pages:
            writePage(page)

        print(f'pbs: {i}')
        i += 100

if __name__ == '__main__':

    getwork()
    
    print('Done!')





    

    
    
