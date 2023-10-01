from rest_framework.response import Response
from rest_framework.views import APIView

from informationretrieval.utils import link_analyser_categories_data


class LinkAnalyserView(APIView):

    def get(self, request, *args, **kwargs):
        return Response(link_analyser_categories_data)