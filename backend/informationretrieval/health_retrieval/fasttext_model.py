import codecs
import json
import numpy as np
from hazm import *
from gensim.models.fasttext import FastText

from informationretrieval.health_retrieval.base_emb_model import BaseModel


class FastTextEmb(BaseModel):
    def __init__(self):
        self.ft_model = FastText.load('models/_fasttext.model')
        with open(f'models/fasttext_docs_embedding.json', 'r', encoding="utf-8") as f:
            self.docs_embs = json.loads(f.read())
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

    def get_query(self, query, k=10, query_expansion=True):
        query_tokens = [_ for _ in word_tokenize(self.normalizer.normalize(query)) if _ not in self.total_stop_words]
        emb = np.zeros(self.ft_model.wv.vector_size)
        for token in query_tokens:
            emb += self.ft_model.wv[token]
        emb /= len(query_tokens)
        if query_expansion:
            emb = self.rocchio(emb, self.docs_embs)
        return self.nearest_neighbor(emb, self.docs_embs, k)

    def nearest_neighbor(self, v, doc_embs, k):
        data = {}
        for doc in doc_embs:
            data[doc['title']] = (self.cosine_similarity(v, doc['emb']), doc['link'])
        ls = [(k, v[1]) for k, v in sorted(data.items(), key=lambda item: item[1][0])][::-1][:(3 * k)]
        return self.get_top_k_unique(ls, k)

    def get_text_embeding(self, text):
        tokens = [_ for _ in word_tokenize(self.normalizer.normalize(text)) if _ not in self.total_stop_words]
        emb = np.zeros(self.ft_model.wv.vector_size)
        for token in tokens:
            emb += self.ft_model.wv[token]
        emb /= len(tokens)
        return emb


fasttext_model = FastTextEmb()
