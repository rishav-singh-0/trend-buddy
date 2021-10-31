from django.urls import path
from .views import SymbolView

urlpatterns = [
    path('symbol', SymbolView.as_view()),
]