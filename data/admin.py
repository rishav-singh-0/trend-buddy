from django.contrib import admin
from .models import Symbol, Favourite, Candle

admin.site.register(Symbol)
admin.site.register(Candle)
admin.site.register(Favourite)