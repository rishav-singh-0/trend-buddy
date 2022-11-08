from django.urls import path
from ui.views import dashboard_view, portfolio_view, analysis_view, analysis_symbol_view, populate_view, screener_view
from ui.views import tables_view, billing_view, notifications_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('portfolio/', portfolio_view, name='all-symbols'),
    path('analysis/', analysis_view, name='analysis'),
    path('analysis/<symbol>', analysis_symbol_view, name='analysis-symbol'),
    path('populate/', populate_view, name='populate'),
    path('screener/', screener_view, name='screener'),
    path('tables/', tables_view),
    path('billing/', billing_view),
    path('notifications/', notifications_view),
]