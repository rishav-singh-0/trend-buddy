from django.shortcuts import render, HttpResponse
from django.views import View
import django_rq

from .bot import Bot

class BotView(View):
    
    def get(self, request, symbol, *args, **kwargs):
        bot = Bot(symbol)
        queue = django_rq.get_queue('day')
        queue.create_job(bot.start)
        return HttpResponse(f"Printing on console {symbol}")
        # return render(request, 'index.html', {'symbols': ''})
