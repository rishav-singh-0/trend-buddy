from django.contrib import admin
from .models import Symbol, Candle

admin.site.register(Symbol)
admin.site.register(Candle)