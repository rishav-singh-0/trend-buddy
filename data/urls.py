from django.urls import path
from .views import CandleView, SymbolView, FavouriteView, PopulateView

urlpatterns = [
    path('symbol/', SymbolView.as_view(), name='symbol'),
    path('favourite/', FavouriteView.as_view(), name='favourite'),
    path('candle/<symbol>/', CandleView.as_view(), name='candle'),
    path('populate/', PopulateView.as_view(), name='populate'),
]