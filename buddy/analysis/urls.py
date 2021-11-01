from django.urls import path
from analysis.views import ChartView, SymbolListView

urlpatterns = [
    path('chart/', SymbolListView.as_view(), name='chart'),
    path('chart/<symbol>', ChartView.as_view(), name='chart'),
]