from django.urls import path
from .views import CandleView, NSEPopulateView, SymbolView, FavouriteView, CryotoPopulateView

urlpatterns = [
    path('symbol/', SymbolView.as_view(), name='symbol'),
    path('favourite/', FavouriteView.as_view(), name='favourite'),
    path('candle/<symbol>/', CandleView.as_view(), name='candle'),
    path('populate/crypto/', CryotoPopulateView.as_view(), name='populate'),
    path('populate/nse/', NSEPopulateView.as_view(), name='populate'),
]