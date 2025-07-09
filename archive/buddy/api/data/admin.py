from django.contrib import admin
from .models import Exchange, Symbol, Candle

admin.site.register(Exchange)
admin.site.register(Symbol)
admin.site.register(Candle)