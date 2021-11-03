from django.shortcuts import render
from django.views import View

from data.models import Symbol, Candle


class SymbolListView(View):

    def get(self, request, *args, **kwargs):

        symbols = Symbol.objects.all()
        favourite_symbol = []

        for favourite in request.user.favourites.all(): # likes is the related name used in models
            favourite_symbol.append(favourite.symbol_id)
        return render(request, 'analysis/all-symbols.html', {'symbols': symbols, 'favourites': favourite_symbol})


class AnalysisView(View):
    
    def get(self, request, symbol, *args, **kwargs):
        
        return render(request, 'analysis/analysis.html', {'symbol': symbol})