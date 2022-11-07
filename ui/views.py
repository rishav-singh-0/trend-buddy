from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render

from data.models import Symbol, Candle
from analysis.statergy import Statergy

@login_required(login_url="/login/")
def dashboard_view(request):
    return render(request, 'home/index.html')

def analysis(request):
    favourite_symbols = []
    for favourite in request.user.favourites.all(): # likes is the related name used in models
        favourite_symbols.append(favourite.symbol_id)

    for symbol in favourite_symbols:
        candle = Candle.objects.filter()
        statergy = Statergy(candle)
        # rsi_value = statergy.rsi()
        # print(rsi_value)

    return render(request, 'home/index.html', {'symbols': favourite_symbols})


@login_required(login_url="/login/")
def portfolio_view(request):
    context = {'segment': 'portfolio'}

    html_template = loader.get_template('home/portfolio.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def analysis_view(request):
    symbols = Symbol.objects.all()
    favourite_symbols = []

    for favourite in request.user.favourites.all(): # likes is the related name used in models
        favourite_symbols.append(favourite.symbol_id)
    return render(request, 'home/analysis.html', {'symbols': symbols, 'favourites': favourite_symbols})

@login_required(login_url="/login/")
def analysis_symbol_view(request, symbol):
    symbol = Symbol.objects.get(symbol=symbol)
    if symbol.exchange.exchange == 'NSE':
        symbol.exchange.exchange = 'BSE'
    return render(request, 'home/analysis-symbol.html', {'symbol': symbol})


@login_required(login_url="/login/")
def populate_view(request):
    context = {'segment': 'populate'}

    html_template = loader.get_template('home/populate.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def tables_view(request):
    context = {'segment': 'tables'}

    html_template = loader.get_template('home/tables.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def billing_view(request):
    context = {'segment': 'billing'}

    html_template = loader.get_template('home/billing.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def notifications_view(request):
    context = {'segment': 'notifications'}

    html_template = loader.get_template('home/notifications.html')
    return HttpResponse(html_template.render(context, request))
