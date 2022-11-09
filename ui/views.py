from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect

from data.models import Symbol, Candle
from bot.models import Trade
from analysis.statergy import Statergy
from .forms import OrderForm
from data.populate import CsvTradePopulate
from django.contrib.auth.models import User
from pandas import read_csv
from io import StringIO
from datetime import datetime


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
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = OrderForm(request.POST, request.FILES, request.user)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data['order_csv']
            # print(data.read())
            trade_data = CsvTradePopulate(request.user)
            decoded_file = data.read().decode()
            io_string = StringIO(decoded_file)
            trade_data.csv_data = read_csv(io_string)
            trade_data.format_zerodha()
            trade_list = trade_data.save_trade()
        
            return HttpResponseRedirect('/portfolio/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = OrderForm()
        trade_list = Trade.objects.filter(user_id=request.user)
        for i in trade_list:
            i.order_execution_time = datetime.fromtimestamp(i.order_execution_time)
    context = {'segment': 'portfolio', 'form': form, 'trade_list':trade_list}
    return render(request, 'home/portfolio.html', context)

@login_required(login_url="/login/")
def screener_view(request):
    context = {'segment': 'screener'}
    return render(request, 'home/screener.html', context)

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
