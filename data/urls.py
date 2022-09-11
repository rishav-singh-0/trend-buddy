from django.urls import include, path

from data.models import Exchange
from .views import ExchangeView, CandleView, NSEPopulateView, SymbolView, FavouriteView, CryotoPopulateView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('exchange', ExchangeView, 'exchange')
router.register('symbol', SymbolView, 'symbol')
router.register('candle', CandleView, 'candle')
router.register('favourite', FavouriteView, 'fovourite')

urlpatterns = [
    path('', include(router.urls)), 
    path('populate/crypto/', CryotoPopulateView.as_view(), name='populate-crypto'),
    path('populate/nse/', NSEPopulateView.as_view(), name='populate-nse'),
]