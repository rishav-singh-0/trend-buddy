from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from data.models import Symbol, Candle
from analysis.statergy import Statergy

@login_required(login_url="/login/")
def dashboard_view(request):
    context = {'segment': 'index'}
    return render(request, 'home/index.html', context)

def analysis(request):
    favourite_symbols = []
    for favourite in request.user.favourites.all(): # likes is the related name used in models
        favourite_symbols.append(favourite.symbol_id)

    for symbol in favourite_symbols:
        candle = Candle.objects.filter()
        statergy = Statergy(candle)
        # rsi_value = statergy.rsi()
        # print(rsi_value)

    return render(request, 'home/index.html', {'segment': 'analysis', 'symbols': favourite_symbols})


@login_required(login_url="/login/")
def portfolio_view(request):
    context = {'segment': 'portfolio'}
    return render(request, 'home/portfolio.html', context)

@login_required(login_url="/login/")
def analysis_view(request):
    symbols = Symbol.objects.all()
    favourite_symbols = []

    for favourite in request.user.favourites.all(): # likes is the related name used in models
        favourite_symbols.append(favourite.symbol_id)
    context = {'segment': 'analysis', 'symbols': symbols, 'favourites': favourite_symbols}
    return render(request, 'home/analysis.html', context)

@login_required(login_url="/login/")
def analysis_symbol_view(request, symbol):
    symbol = Symbol.objects.get(symbol=symbol)
    if symbol.exchange.exchange == 'NSE':
        symbol.exchange.exchange = 'BSE'
    return render(request, 'home/analysis-symbol.html', {'symbol': symbol})


@login_required(login_url="/login/")
def populate_view(request):
    context = {'segment': 'populate'}
    return render(request, 'home/populate.html', context)

@login_required(login_url="/login/")
def tables_view(request):
    context = {'segment': 'tables'}
    return render(request, 'home/tables.html', context)

@login_required(login_url="/login/")
def billing_view(request):
    context = {'segment': 'billing'}
    return render(request, 'home/billing.html', context)

@login_required(login_url="/login/")
def notifications_view(request):
    context = {'segment': 'notifications'}
    return render(request, 'home/notifications.html', context)
