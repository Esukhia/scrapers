import urllib.request
from multiprocessing.dummy import Pool as ThreadPool
import pickle
import random
from re import search

extentDict = {}
base = 'http://www.buddism.ru:4000/?index={work}&field={page}&ocrData=read&ln=rus'
work = 1
page = 1
works = [*range(650)]
# works = [*range(1828650)]
random.shuffle(works)

def getExtent(work):
    # gets work, returns extent
    url = base.format(work=work, page=page)
    response = urllib.request.urlopen(url)
    html = response.read()
    htmlStr = html.decode()
    pdata = search("\"gray\"><b>from (-?\d+)<", htmlStr)

    extent = pdata.group(1)
    extentDict[work] = extent
    print(work, extent)

    return pdata.group(1)


with ThreadPool(100) as pool:
    pool.map(getExtent, works)

with open('extent.pickle', 'wb') as fp:
    pickle.dump(extentDict, fp)

# with open ('extent.pickle', 'rb') as fp:
#     itemlist = pickle.load(fp)
