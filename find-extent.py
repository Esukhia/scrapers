import urllib.request
from multiprocessing.dummy import Pool as ThreadPool
import pickle
import random
from re import search

# extentDict = {}
base = 'http://www.buddism.ru:4000/?index={work}&field={page}&ocrData=read&ln=rus'
work = 1
page = 1

min = 1
max = 1828660

works = [*range(min, max)]
# print(works)
# works = [*range(1828650)]
# random.shuffle(works) 

def getExtent(work):
    # gets work, returns extent
    url = base.format(work=work, page=page)
    response = urllib.request.urlopen(url)
    html = response.read()
    htmlStr = html.decode()
    pdata = search("\"gray\"><b>from (-?\d+)<", htmlStr)

    extent = pdata.group(1)
    extentDict = {}
    extentDict[work] = extent
    print(work, extent)

    return extentDict




i = min
batch = 100
while i < max:    
    with ThreadPool(batch) as pool:
        l = pool.map(getExtent, [*range(i, i+batch)])
        with open('extent.csv','a+') as f:
            for e in l:
                for x, y in e.items():
                    f.write("%s, %s\n" % (x, y))
    f.close()  
    i+=batch
    # f.write("}")
    

# with open('extent.pickle', 'wb') as fp:
#     pickle.dump(extentDict, fp)

# with open ('extent.pickle', 'rb') as fp:
#     itemlist = pickle.load(fp)
