from django.db import models

class Symbol(models.Model):
    symbol = models.CharField(unique=True ,max_length=15)
    
    def __str__(self):
        return self.symbol

class Candle(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    time = models.IntegerField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    
    def __str__(self):
        return f'{self.symbol}_{self.time}'