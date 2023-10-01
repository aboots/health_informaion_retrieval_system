import json
import os

import requests
from bs4 import BeautifulSoup

DIRNAME = '../new-dataset-with-category'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Content-Type': 'text/html',
}
os.makedirs(DIRNAME, exist_ok=True)
total_pages = 100
base_url = 'https://namnak.com'
all_data = []

all_old_links = []
for i in range(1, 6):
    with open(f'../old-dataset/namnak-{i}.json', 'r') as j:
        contents = json.loads(j.read())
        for cont in contents:
            all_old_links.append(cont['link'])

url = f"{base_url}/c5-بهداشت-و-سلامت"
f = requests.get(url, headers=headers)
soup = BeautifulSoup(f.content, 'lxml')
categories_dict = {}
for a in soup.find('div', {'class': 'Cc b'}).findAll('a'):
    categories_dict[a.text] = base_url + '/p{i}-' + a['href'][1:]

c2 = 0

for category, category_link in categories_dict.items():
    flag = False
    for i in range(1, total_pages + 1):
        url = category_link.format(i=i)
        f = requests.get(url, headers=headers)
        soup = BeautifulSoup(f.content, 'lxml')
        if len(soup.findAll('a', {'class': 'pno'})) == 1:
            flag = soup.find('a', {'class': 'pno'})['rel'][0] == 'prev'
        news_links = []
        for item in soup.findAll('div', {'class': 'j'}):
            news_links.append(base_url + item.find('a')['href'])
        for link in news_links:
            if link in all_old_links:
                c2 += 1
                continue
            f = requests.get(link, headers=headers)
            data = {'link': link}
            soup = BeautifulSoup(f.content, 'lxml')
            data['title'] = soup.find('h1').text
            data['category'] = category
            data['abstract'] = soup.find('div', {'class': 'E9'}).text
            p_list = soup.find('div', {'class': 'C3 c b i'}).findAll('p')
            data['paragraphs'] = [_.text for _ in p_list if _.text != '']
            if len(data['paragraphs']) < 2:
                continue
            all_data.append(data)
        print(f'{i} page of category {category} done.')
        print(f'len: {len(all_data)}')
        print(f'c2: {c2}')
        if flag:
            print(f'category {category} done.')
            break


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


c = 6
for gp in chunker(all_data, 250):
    with open(f"{DIRNAME}/namnak-{c}.json", "w", encoding="utf-8") as file:
        json.dump(gp, file, ensure_ascii=False)
    c += 1
