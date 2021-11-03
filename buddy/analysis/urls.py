from django.urls import path
from analysis.views import ChartView, SymbolListView, AnalysisView

urlpatterns = [
    path('all-symbols/', SymbolListView.as_view(), name='all-symbols'),
    path('chart/<symbol>', ChartView.as_view(), name='chart'),
    path('analysis', AnalysisView.as_view(), name='analysis'),
]