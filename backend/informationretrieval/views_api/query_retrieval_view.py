from rest_framework.response import Response
from rest_framework.views import APIView
from informationretrieval.health_retrieval import *


class QueryRetrievalView(APIView):

    def get(self, request, *args, **kwargs):
        method = self.request.query_params['method']
        model = self.get_model(method)
        query = self.request.query_params['query']
        query_expansion = self.request.query_params['query_expansion']
        query_expansion = True if query_expansion == 'true' else False
        k = 10 if 'k' not in self.request.query_params else int(self.request.query_params['k'])
        ls = model.get_query(query, k, query_expansion)
        final_ls = []
        for item in ls:
            final_ls.append({'title': item[0], 'url': item[1]})
        return Response(final_ls)

    def get_model(self, method):
        if method == 'fasttext':
            return fasttext_model
        if method == 'boolean':
            return boolean_model
        if method == 'transformers':
            return transformer_model
        if method == 'tfidf':
            return tfidf_model
        if method == 'elastic':
            return elastic_model
        return fasttext_model
