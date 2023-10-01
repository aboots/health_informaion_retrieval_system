import json
import os

import requests
from bs4 import BeautifulSoup

DIRNAME = '../new-dataset'
os.makedirs(DIRNAME, exist_ok=True)
total_pages = 200
base_url = 'https://www.hidoctor.ir'
all_data = []

all_old_links = []
bad_patterns = ['\xa0\n\n\n\t\t\t\t\t\t\n\t\t\t\t\t\t', '\n', '', ' ', '\xa0\n', '\xa0']
for i in range(1, 6):
    with open(f'../old-dataset/hidoctor-{i}.json', 'r') as j:
        contents = json.loads(j.read())
        for cont in contents:
            all_old_links.append(cont['link'])

c2 = 0

for i in range(2, total_pages + 1):
    url = f"{base_url}/page/{i}/"
    f = requests.get(url)
    soup = BeautifulSoup(f.content, 'lxml')
    news_links = []
    for item in soup.findAll('a', {'class': 'readmore'}):
        news_links.append(item['href'])
    for link in news_links:
        if link in all_old_links:
            c2 += 1
            continue
        f = requests.get(link)
        data = {'link': link}
        soup = BeautifulSoup(f.content, 'lxml')
        data['title'] = soup.find('h1').text
        p_list = soup.find('div', {'class': 'post-content typography single-post-body clearfix progressive'}).findAll('p')
        data['paragraphs'] = [_.text for _ in p_list if ((_.text not in bad_patterns) and ('\xa0' not in _.text))]
        all_data.append(data)
    print(f'{i} page out of {total_pages} done.')
    print(f'len: {len(all_data)}')
    print(f'c2: {c2}')


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


c = 6
for gp in chunker(all_data, 500):
    with open(f"{DIRNAME}/hidoctor-{c}.json", "w", encoding="utf-8") as file:
        json.dump(gp, file, ensure_ascii=False)
    c += 1
