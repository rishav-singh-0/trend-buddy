from django.urls import path
from analysis.views import SymbolListView, AnalysisView

urlpatterns = [
    path('all-symbols/', SymbolListView.as_view(), name='all-symbols'),
    path('analysis/<symbol>', AnalysisView.as_view(), name='analysis'),
]