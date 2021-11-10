from django.urls import path
from .views import BotView

urlpatterns = [
    path('<symbol>/', BotView.as_view(), name='bot'),
]