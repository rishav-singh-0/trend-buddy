from django.urls import path
from analysis.views import ChartView

urlpatterns = [
    path('chart/', ChartView.as_view(), name='chart')
]