from django.urls import include, path

from .views import ExchangeView, CandleView, FileUploadAPIView, NSEPopulateView, SymbolView, FavouriteView, CryotoPopulateView
from rest_framework import routers

urlpatterns = [
    path('exchange/', ExchangeView.as_view(), name='exchange'),
    path('symbol/', SymbolView.as_view(), name='symbol'),
    path('candle/', CandleView.as_view(), name='candle'),
    path('favourite/', FavouriteView.as_view(), name='fovourite'),
    path('file-upload/', FileUploadAPIView.as_view(), name='order-upload'),
    path('populate/crypto/', CryotoPopulateView.as_view(), name='populate-crypto'),
    path('populate/nse/', NSEPopulateView.as_view(), name='populate-nse'),
]