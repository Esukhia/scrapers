import urllib.request
from pathlib import Path
import re
import time
import datetime
from multiprocessing import freeze_support

from bs4 import BeautifulSoup
from pybo import PyBoChunk

from multithread import multi_thread_process


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


def cleanup():
    # create output dir if missing
    out_path = Path('output')
    if not out_path.is_dir():
        out_path.mkdir(exist_ok=True)

    # delete downloads from previous run
    for f in out_path.glob('*.txt'):
        f.unlink()


def download_one_text(url_base, index, uptime):
    start_time = time.time()
    out_path = Path('output')
    work = []
    page = 1
    title = ''
    while page:
        response = urllib.request.urlopen(url_base.format(work=index, page=page))

        content = get_content(response)

        if content:
            meta, text = separate_text(content)
            meta = ''.join(re.findall(r'\[Title:([^\]]+)\]', meta))  # only keep the Tibetan title as meta-data
            meta, has_bo = clean_non_bo(meta)
            text, _ = clean_non_bo(text)

            if not title and not has_bo:
                page = None
                continue

            if not title and meta:
                title = meta.replace('\n', '')[:80]  # filenames are limited

            # add the text found to pages
            if text:
                work.append(text)
            page += 1
        else:
            page = None

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


def main(url_base, min, max, uptime):
    # single threaded version
    for i in range(min, max):
        download_one_text(url_base, i, uptime)


if __name__ == '__main__':
    # cleanup()

    base = 'http://www.buddism.ru:4000/?index={work}&field={page}&ocrData=read&ln=rus'
    min = 1
    # max = 1828650
    max = 100
    thread_number = 10
    uptime = time.time()
    tasks = [(download_one_text, (base, i, uptime)) for i in range(min, max)]  # generate all the tasks

    freeze_support()
    multi_thread_process(thread_number, tasks)
