from django.shortcuts import render, HttpResponse
from django.views import View

from .jobs import Bot

class BotView(View):
    
    def get(self, request, *args, **kwargs):
        bot = Bot('BTCUSDT')
        bot.start()
        return HttpResponse("Printing on console")
        # return render(request, 'index.html', {'symbols': ''})

