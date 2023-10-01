import codecs
import json
import numpy as np
from hazm import *
import torch

from transformers import BigBirdModel, AutoTokenizer

from informationretrieval.health_retrieval.base_emb_model import BaseModel


class TransformerEmb(BaseModel):
    vector_title = 'vector'

    def __init__(self):
        self.model = BigBirdModel.from_pretrained('models/pretrained-transformer-model.model')
        self.tokenizer = AutoTokenizer.from_pretrained('models/pretrained-transformer-tokenizer')
        with open('models/transformers-link-docs-data.json', 'r', encoding="utf-8") as f:
            self.docs_links = json.loads(f.read())
        with open('models/transformer_vectors-new-mixed.json', 'r', encoding="utf-8") as f:
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
        encoded_query = self.model(**self.tokenizer(query, return_tensors='pt'))[0].detach().squeeze()
        encoded_query = torch.mean(encoded_query, dim=0).numpy()
        if query_expansion:
            encoded_query = self.rocchio(encoded_query, self.docs_embs)
        return self.nearest_neighbor(encoded_query, self.docs_embs, k)

    def cosine_similarity(self, vector_1: np.ndarray, vector_2: np.ndarray) -> float:
        return np.dot(vector_1, vector_2) / (np.linalg.norm(vector_1) *
                                             np.linalg.norm(vector_2))

    def nearest_neighbor(self, v, doc_embs, k):
        data = {}
        for doc in doc_embs:
            data[doc['title']] = (
                self.cosine_similarity(v, np.array(doc['vector'])), self.docs_links[str(doc['index'])])
        ls = [(k, v[1]) for k, v in sorted(data.items(), key=lambda item: item[1][0])][::-1][:(k * 3)]
        return self.get_top_k_unique(ls, k)


transformer_model = TransformerEmb()
