from django.urls import path
from analysis.views import DashboardView, SymbolListView, AnalysisView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('all-symbols/', SymbolListView.as_view(), name='all-symbols'),
    path('analysis/<symbol>', AnalysisView.as_view(), name='analysis'),
]