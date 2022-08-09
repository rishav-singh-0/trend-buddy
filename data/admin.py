from django.contrib import admin
from .models import Exchange, Symbol, Favourite, Candle

admin.site.register(Exchange)
admin.site.register(Symbol)
admin.site.register(Candle)
admin.site.register(Favourite)