import codecs
import json
import time
from elasticsearch import Elasticsearch
from subprocess import Popen

from hazm import Normalizer, word_tokenize

from informationretrieval.health_retrieval import fasttext_model


class ElasticSearch:
    def __init__(self, host='http://localhost:9200', elasticsearch_path=None):
        self.normalizer = Normalizer()
        stopwords = [self.normalizer.normalize(x.strip()) for x in
                     codecs.open('stopwords/stopwords.txt', 'r', 'utf-8').readlines()]
        custom_stop_words = [self.normalizer.normalize(x.strip()) for x in
                             codecs.open('stopwords/custom_stopwords.txt', 'r', 'utf-8').readlines()]
        self.total_stop_words = custom_stop_words + stopwords
        self.hosts = [host]
        self.index = 'health'
        if elasticsearch_path:
            self.__start_elasticsearch_server(elasticsearch_path)
        self.client = Elasticsearch(hosts=self.hosts)

    def delete_index(self):
        print("deleting the '{}' index.".format(self.index))
        res = self.client.indices.delete(index=self.index, ignore=[400, 404])
        print("Response for deleting from server: {}".format(res))

    def insert_data_and_create_index(self, folder_path):
        data = []
        for i in range(1, 8):
            with open(f'{folder_path}/namnak-p{i}.json', 'r', encoding="utf-8") as f:
                data.extend(json.loads(f.read()))
            with open(f'{folder_path}/hidoctor-p{i}.json', 'r', encoding="utf-8") as f:
                data.extend(json.loads(f.read()))
        data = {(_['title'], _['link'], _['text']) for _ in data}
        data = [{'title': _[0], 'link': _[1], "text": _[2]} for _ in data]
        print("Creating Index and Adding Data...")
        if self.client.indices.exists(index=self.index):
            self.delete_index()
        print("creating the '{}' index.".format(self.index))
        res = self.client.indices.create(index=self.index)
        print("Response for creating index from server: {}".format(res))
        print("bulk index the data")
        indexed_data = self.prepare_indexed_data(data)
        res = self.client.bulk(index=self.index, body=indexed_data, refresh=True)
        print("Errors: {}, Num of records indexed: {}".format(res["errors"], len(res["items"])))

    def __start_elasticsearch_server(self, elasticsearch_path):
        print("Starting Elasticsearch Server...")
        Popen(elasticsearch_path)
        time.sleep(30)

    def prepare_indexed_data(self, data):
        es_data = []
        for idx, record in enumerate(data):
            meta_dict = {
                "index": {
                    "_index": self.index,
                    "_id": idx
                }
            }
            es_data.append(meta_dict)
            es_data.append(record)
        return es_data

    def get_query(self, query, k=10, query_expansion=True):
        query_tokens = [_ for _ in word_tokenize(self.normalizer.normalize(query)) if _ not in self.total_stop_words]
        response = self.search_client(query, k)
        if query_expansion or len(response) < k:
            final_query = " ".join(self.expansion_query(query_tokens))
            response = self.search_client(final_query, k)
        result = []
        for item in response:
            result.append((item['_source']['title'], item['_source']['link']))
        return result

    def search_client(self, query, k):
        body = {
            "size": k,
            "query": {
                "multi_match": {
                    "query": query,
                    "type": "most_fields",
                    "fields": [
                        "title^2",
                        "text"
                    ]
                }
            }
        }
        return self.client.search(index=self.index, body=body)['hits']['hits']

    def expansion_query(self, tokens):
        final_tokens = tokens.copy()
        for token in tokens:
            similar_words = fasttext_model.ft_model.wv.most_similar(token)
            for word in similar_words:
                if 0.85 < word[1] < 0.98:
                    final_tokens.append(word[0])
        return final_tokens


# local_mode
elastic_model = ElasticSearch(elasticsearch_path="C:\\elasticsearch\\elasticsearch-7.3.2\\bin\\elasticsearch.bat")
# elastic_model.insert_data_and_create_index('dataset')
