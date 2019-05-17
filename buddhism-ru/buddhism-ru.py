import urllib.request
from pathlib import Path
import re
import time
import datetime
from multiprocessing import freeze_support

from bs4 import BeautifulSoup
from pybo import PyBoChunk

from multithread import multi_thread_process
from multiprocessing import Pool


base = 'http://www.buddism.ru:4000/?index={work}&field={page}&ocrData=read&ln=rus'


class BoNonboChunk(PyBoChunk):
    def __init__(self, string):
        super().__init__(string, ignore_chars=['\n'])

    def chunk(self, indices=True, gen=False):
        return self.chunk_bo_chars()

    def get_cleaned_bo(self):
        chunks = self.chunk()
        chunks = self.get_chunked(chunks)
        has_bo = True if self.BO_MARKER in [a[0] for a in chunks] else False
        chunks = [b for a, b in chunks if a == self.BO_MARKER]
        return ''.join(chunks).strip(), has_bo


def separate_text(content):
    # TODO deal with [] at end of pages like: http://buddism.ru:4000/?index=8211&field=7&ocrData=read&ln=eng
    if ']' in content:
        idx = content.rfind(']')
        meta, text = content[:idx], content[idx + 1:]
    else:
        return '', content

    return meta, text


def clean_non_bo(string):
    chunk = BoNonboChunk(string)
    cleaned, has_bo = chunk.get_cleaned_bo()
    cleaned = cleaned.strip()
    return cleaned, has_bo


def get_content(response):
    html = BeautifulSoup(response.read(), 'lxml')

    # only keep the section containing text
    txt = html.find_all('textarea')
    txt = [a.text.strip() for a in txt]
    txt = ''.join([t for t in txt if t])
    return txt

def getExtent(work):
    # gets work, returns extent
    url = base.format(work=work, page=1)
    response = urllib.request.urlopen(url)
    html = response.read()
    htmlStr = html.decode()
    pdata = re.search("\"gray\"><b>from (-?\d+)<", htmlStr)
    extent = int(pdata.group(1))
    if extent > 1000 or extent < 1:
        extent = 0
    return extent

def cleanup():
    # create output dir if missing
    out_path = Path('output')
    if not out_path.is_dir():
        out_path.mkdir(exist_ok=True)

    # delete downloads from previous run
    for f in out_path.glob('*.txt'):
        f.unlink()


def download_one_text(index):
    start_time = time.time()
    out_path = Path('output')
    work = []
    extent = getExtent(index)
    print(index, extent)
    page = 1
    title = ''
    while page <= extent:

        dwnld_start = time.time()
        response = urllib.request.urlopen(base.format(work=index, page=page))

        content = get_content(response)
        dwnld_end = time.time()
        dwnld = str(dwnld_end - dwnld_start).split('.')[0]
        print(f'work: {index}, page: {page}, download time: {dwnld}')

        if content:
            meta, text = separate_text(content)
            print(page, 'text', text[:20])
            print(page, 'content', content[:20])
            meta = ''.join(re.findall(r'\[Title:([^\]]+)\]', meta))  # only keep the Tibetan title as meta-data
            meta, has_bo = clean_non_bo(meta)
            text, _ = clean_non_bo(text)

            # if not title and not has_bo:
            #     page = None
            #     continue

            if not title and meta:
                title = meta.replace('\n', '')[:80]  # filenames are limited

            # add the text found to pages
            # if text:
            work.append(content)
            page += 1
        else:
            # page = None
            break

    if work:
        out_file = out_path / f'{index}_{title}.txt'
        out_file.write_text(''.join(work), encoding='utf-8-sig')

    end_time = time.time()
    duration = str(datetime.timedelta(seconds=end_time - start_time))[:7]
    since_start = str(datetime.timedelta(seconds=end_time - uptime))[:7]
    if title:
        return f'elapsed: {since_start} — {duration} — "{title}"'
    else:
        return f'elapsed: {since_start}'


# Create a function called "chunks" with two arguments, l and n:
def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]


def main(min, max, batch_size):
    total_tasks = range(min, max)
    # Create a list that from the results of the function chunks:
    batches = list(chunks(total_tasks, batch_size))

    for batch in batches:
        tasks = [(download_one_text, (base, b, uptime)) for b in batch]
        freeze_support()
        multi_thread_process(threads, tasks)


if __name__ == '__main__':
    uptime = time.time()
    cleanup()

    batch_size = 100
    threads = batch_size
    min = 8149
    max = min + batch_size
    total = 8250

    while min < total:

        with Pool(processes=batch_size) as pool:
            pool.map(download_one_text, range(min, max))

        min = max+1
        max += batch_size
        print(min, max)

    # main(min, max, batch_size)




