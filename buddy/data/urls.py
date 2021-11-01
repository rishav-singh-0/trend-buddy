from django.urls import path
from .views import CandleView, SymbolView, PopulateView

urlpatterns = [
    path('symbol/', SymbolView.as_view(), name='symbol'),
    path('candle/<symbol>', CandleView.as_view(), name='candle'),
    path('populate/', PopulateView.as_view(), name='populate'),
]