from django.urls import path
from ui.views import dashboard_view, portfolio_view, analysis_view, populate_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('portfolio/', portfolio_view, name='all-symbols'),
    path('analysis/', analysis_view, name='analysis'),
    path('symbols/<symbol>', analysis_view, name='analysis'),
    path('populate/', populate_view, name='populate'),
]