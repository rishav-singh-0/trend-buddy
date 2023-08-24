from django.db import models

class Exchange(models.Model):
    exchange = models.CharField(unique=True ,max_length=15)
    
    def __str__(self):
        return self.exchange

class Symbol(models.Model):
    symbol = models.CharField(unique=True ,max_length=15)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.symbol
    
class Candle(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='candles')
    time = models.IntegerField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.IntegerField()

    class Meta:
        unique_together = ["symbol", "time"]
    
    def __str__(self):
        return f'{self.symbol}_{self.time}'



# from django.contrib.auth.models import User
# from django.db.models import UniqueConstraint

# class Favourite(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
#     symbol_id = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='favourites')
#     favourited_on = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         constraints = [
#             UniqueConstraint(fields=['user_id','symbol_id'],  name="unique_symbol_favourites")
#         ]
    
#     def __str__(self):
#         return f'{self.user_id.username} --> {self.symbol_id.symbol}'

# class FundamentalData(models.Model):
#     symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='fundamental_data')
#     # Add fields for fundamental data (e.g., earnings, revenue, ratios)
    
#     def __str__(self):
#         return f'Fundamental data for {self.symbol}'

# class TechnicalData(models.Model):
#     symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='technical_data')
#     # Add fields for technical data (e.g., moving averages, RSI, MACD)
    
#     def __str__(self):
#         return f'Technical data for {self.symbol}'