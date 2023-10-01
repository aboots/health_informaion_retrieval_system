import numpy as np


class BaseModel:
    vector_title = 'emb'

    def rocchio(self, v, doc_embs):
        nearest, furthest = self.k_nearest_furthest_neighbors(v, doc_embs, 10)
        nearest_mean = np.mean(nearest, axis=0)
        furthest_mean = np.mean(furthest, axis=0)
        return v + nearest_mean - furthest_mean

    def cosine_similarity(self, vector_1: np.ndarray, vector_2: np.ndarray) -> float:
        return np.dot(vector_1, vector_2) / (np.linalg.norm(vector_1) *
                                             np.linalg.norm(vector_2))

    def k_nearest_furthest_neighbors(self, v, doc_embs, k):
        data = {doc['title']: (self.cosine_similarity(v, doc[self.vector_title]), doc[self.vector_title]) for doc in
                doc_embs}
        sorted_ls = [v[1] for k, v in sorted(data.items(), key=lambda item: item[1][0])]
        return sorted_ls[::-1][:k], sorted_ls[:k]

    def get_top_k_unique(self, docs, k):
        final = []
        for item in docs:
            if item not in final:
                final.append(item)
                if len(final) == k:
                    return final
        return final
