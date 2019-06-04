import re
import shutil
import os

infile = 'adarsha/degetengyur.json'

outdir = 'adarsha/degetengyur/'
shutil.rmtree(outdir, ignore_errors=True)
os.mkdir(outdir)


with open(infile, 'r') as f:
    pages = f.readlines()

v = 1
vol = 1


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
    print(page[:15])
    pageNum = int(re.search('"pbId":"\d+?-\d+?-(\d+?)[a-z]', page).group(1))
    lines.append(pageNum)
    side = re.search('"pbId":"\d+?-\d+?-\d+?([a-z])', page).group(1)
    lines.append(side)
    text = re.search('"text":"(.+?)"', page).group(1)
    text = re.sub('\s+', ' ', text)
    ls = list(filter(None, text.split('\\n')))
    lines += ls

    return lines

def item_generator(things):
    # because writelines() is such a tease
    for item in things:
        yield item
        yield '\n'

for page in pages:
    lines = extractLines(page)
    formatedLines = formatLines(lines)

    fileName = "{:0>3d}".format(formatedLines.pop(0))

    with open(f'{outdir}{fileName}.txt', 'a+', encoding='utf-8') as file:
        file.writelines(item_generator(formatedLines))


    

    
    
