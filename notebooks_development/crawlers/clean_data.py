import json

for i in range(1, 8):
    data = []
    with open(f'../old-dataset/hidoctor-{i}.json', 'r', encoding="utf-8") as j:
        contents = json.loads(j.read())
        for cont in contents:
            item = {'title': cont['title'], 'text': ' '.join(cont['paragraphs']), 'link': cont['link']}
            data.append(item)
    with open(f'../dataset/hidoctor-p{i}.json', 'w', encoding="utf-8") as f:
        json.dump(data, f)

for i in range(1, 8):
    data = []
    with open(f'../old-dataset/namnak-{i}.json', 'r', encoding="utf-8") as j:
        contents = json.loads(j.read())
        for cont in contents:
            cont['paragraphs'].insert(0, cont['abstract'])
            item = {'title': cont['title'], 'text': ' '.join(cont['paragraphs']), 'link': cont['link']}
            data.append(item)
    with open(f'../dataset/namnak-p{i}.json', 'w', encoding="utf-8") as f:
        json.dump(data, f)
