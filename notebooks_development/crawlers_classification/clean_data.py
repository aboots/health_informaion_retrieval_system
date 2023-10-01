import json
from collections import Counter

for i in range(1, 6):
    data = []
    with open(f'../old-dataset/namnak-{i}.json', 'r', encoding="utf-8") as j:
        contents = json.loads(j.read())
        for cont in contents:
            item = {'title': cont['title'], 'paragraphs': cont['paragraphs'], 'link': cont['link'],
                    'category': cont['categories'][1], "abstract": cont['abstract']}
            data.append(item)
    with open(f'../new-dataset-with-category/namnak-{i}.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def calc_categories_data():
    c = Counter()
    for i in range(1, 31):
        categories = {}
        with open(f'new-dataset-with-category/namnak-{i}.json', 'r', encoding="utf-8") as j:
            data = json.loads(j.read())
            for item in data:
                if item['category'] in categories:
                    categories[item['category']] += 1
                else:
                    categories[item['category']] = 1
        c.update(categories)
    return c
