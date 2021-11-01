from django.urls import path
from .views import CandleView, SymbolView

urlpatterns = [
    path('symbol', SymbolView.as_view(), name='symbol'),
    path('candle', CandleView.as_view(), name='candle'),
]