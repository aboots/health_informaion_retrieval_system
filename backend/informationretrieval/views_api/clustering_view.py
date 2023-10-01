from rest_framework.response import Response
from rest_framework.views import APIView

from informationretrieval.clustering import kemans_clustering_model


class ClusteringView(APIView):

    def get(self, request, *args, **kwargs):
        query = self.request.query_params['query']
        k = 10 if 'k' not in self.request.query_params else int(self.request.query_params['k'])
        return Response(kemans_clustering_model.predict(query, k))


class ClusteringResultsView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(kemans_clustering_model.metrics)
