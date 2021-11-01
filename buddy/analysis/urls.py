from django.urls import path
from analysis.views import ChartView

urlpatterns = [
    path('chart/<symbol>', ChartView.as_view(), name='chart')
]