import urllib.request
import pickle
from re import search

base = 'http://www.buddism.ru:4000/?index={work}&field={page}&ocrData=read&ln=rus'
work = 1
page = 1

extentDict = {}

def getExtent(work):
    # gets work, returns extent
    url = base.format(work=work, page=page)
    response = urllib.request.urlopen(url)
    html = response.read()
    htmlStr = html.decode()
    pdata = search("\"gray\"><b>from (-?\d+)<", htmlStr)
    return pdata.group(1)

while work < 50:
    extent = getExtent(work)
    extentDict[work] = extent
    print(work, extent)
    work += 1

with open('extent.pickle', 'wb') as fp:
    pickle.dump(extentDict, fp)


# with open ('extent.pickle', 'rb') as fp:
#     itemlist = pickle.load(fp)

