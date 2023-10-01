import codecs
import json
import pickle
import numpy as np
from scipy import sparse
from hazm import *


class TfidfModel:
    def __init__(self):
        self.doc_term_mat = sparse.load_npz("models/doc-term-tfidf.npz")
        with open(f'models/doc-term-tfidf-data.json', 'r', encoding="utf-8") as f:
            self.docs_data = json.loads(f.read())
        with open('models/tfidfvectorizer.pk', 'rb') as fin:
            self.tfidfvectorizer = pickle.load(fin)
        self.normalizer = Normalizer()
        stopwords = [self.normalizer.normalize(x.strip()) for x in
                     codecs.open('stopwords/stopwords.txt', 'r', 'utf-8').readlines()]
        custom_stop_words = [self.normalizer.normalize(x.strip()) for x in
                             codecs.open('stopwords/custom_stopwords.txt', 'r', 'utf-8').readlines()]
        self.total_stop_words = custom_stop_words + stopwords

    def print_similars(self, query, k=10):
        ls = self.get_query(query, k)
        for i, item in enumerate(ls):
            print(f'{i + 1}- title: {item[0]}')
            print(f'{i + 1}- link: {item[1]}')
            print('-------------------------')

    def get_query(self, query, k=10):
        query_tokens = [_ for _ in word_tokenize(self.normalizer.normalize(query)) if _ not in self.total_stop_words]
        emb = self.tfidfvectorizer.transform([' '.join(query_tokens)])
        docs = []
        for i, doc in enumerate(self.doc_term_mat):
            docs.append(
                {'title': self.docs_data[i]['title'], 'emb': doc[0].toarray()[0], 'link': self.docs_data[i]['link']})
        return self.nearest_neighbor(emb[0].toarray()[0], docs, k)

    def cosine_similarity(self, vector_1: np.ndarray, vector_2: np.ndarray) -> float:
        return np.dot(vector_1, vector_2) / (np.linalg.norm(vector_1) *
                                             np.linalg.norm(vector_2))

    def nearest_neighbor(self, v, doc_embs, k):
        data = {}
        for doc in doc_embs:
            data[doc['title']] = (self.cosine_similarity(v, doc['emb']), doc['link'])
        return [(k, v[1]) for k, v in sorted(data.items(), key=lambda item: item[1][0])][::-1][:k]
