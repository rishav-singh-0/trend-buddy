from django.urls import path
from .views import BotView

urlpatterns = [
    path('', BotView.as_view(), name='dashboard'),
]