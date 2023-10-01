from rest_framework.response import Response
from rest_framework.views import APIView

from informationretrieval.classification import naive_bayes_classifier, logistic_regression_classifier, \
    transformer_classifier
from informationretrieval.health_retrieval import *


class ClassificationView(APIView):

    def get(self, request, *args, **kwargs):
        method = self.request.query_params['method']
        model = self.get_model(method)
        query = self.request.query_params['query']
        return Response(model.predict(query))

    def get_model(self, method):
        if method == 'naive_bayes':
            return naive_bayes_classifier
        if method == 'logistic_regression':
            return logistic_regression_classifier
        if method == 'transformers':
            return transformer_classifier
        return fasttext_model
