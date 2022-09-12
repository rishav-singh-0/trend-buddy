from django.db import models
from django.contrib.auth.models import User
from data.models import Symbol


class Trade(models.Model):
    CHOICE = (
        ('BUY', 'BUY'),
        ('SELL', 'SELL'),
    )

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trade')
    symbol_id = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='trade')
    trade_type = models.CharField(max_length=5, choices=CHOICE)
    quantity = models.FloatField()
    price = models.FloatField()
    order_execution_time = models.DateField()

    def __str__(self):
        return f"{self.user_id}_{self.symbol_id}@{self.order_execution_time.strftime('%Y_%m_%d-%H_%M_%S')}"
