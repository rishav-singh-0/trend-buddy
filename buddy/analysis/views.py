from django.shortcuts import render, HttpResponse
from django.views import View

class ChartView(View):

    def get(self, request, *args, **kwargs):
        # return HttpResponse("Hello World!")
        return render(request, 'home.html', {})