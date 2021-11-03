from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint

class Symbol(models.Model):
    symbol = models.CharField(unique=True ,max_length=15)
    
    def __str__(self):
        return self.symbol
    
class Favourite(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    symbol_id = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='favourites')
    favourited_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['user_id','symbol_id'],  name="unique_symbol_favourites")
        ]
    
    def __str__(self):
        return f'{self.user_id.username} --> {self.symbol_id.symbol}'

class Candle(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='candles')
    time = models.IntegerField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    
    def __str__(self):
        return f'{self.symbol}_{self.time}'