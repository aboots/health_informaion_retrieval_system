from django.urls import path

from informationretrieval import views_api

urlpatterns = [
    path('health/query_retrieval/', views_api.QueryRetrievalView.as_view()),
    path('health/classification/', views_api.ClassificationView.as_view()),
    path('health/clustering/', views_api.ClusteringView.as_view()),
    path('health/clustering_result/', views_api.ClusteringResultsView.as_view()),
    path('health/link_analyser/', views_api.LinkAnalyserView.as_view()),
]
