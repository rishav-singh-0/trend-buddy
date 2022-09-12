from django.urls import include, path

from .views import ExchangeView, CandleView, FileUploadAPIView, NSEPopulateView, SymbolView, FavouriteView, CryotoPopulateView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('exchange', ExchangeView, basename='exchange')
router.register('symbol', SymbolView, basename='symbol')
router.register('candle', CandleView, basename='candle')
router.register('favourite', FavouriteView, basename='fovourite')
router.register('file-upload', FileUploadAPIView, basename='order-upload')

urlpatterns = [
    path('', include(router.urls)), 
    path('populate/crypto/', CryotoPopulateView.as_view(), name='populate-crypto'),
    path('populate/nse/', NSEPopulateView.as_view(), name='populate-nse'),
]