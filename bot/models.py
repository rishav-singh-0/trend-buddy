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
    order_execution_time = models.IntegerField()

    def __str__(self):
        return f"{self.user_id}_{self.trade_type}_{self.symbol_id}@{self.order_execution_time}"


class Holding(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='holding')
    symbol_id = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='holding')
    quantity = models.FloatField()
    buying_price = models.FloatField()
    ltp = models.FloatField(null=True)
    ltp_time = models.IntegerField(null=True)
    created_time = models.IntegerField()

    @property
    def percentage_gain(self):
        return round(100 * (self.ltp - self.buying_price) / self.buying_price, 2)

    @property
    def invested_price(self):
        return round(self.quantity * self.buying_price, 2)

    class Meta:
        unique_together = ["user_id", "symbol_id"]

    def __str__(self):
        return f"{self.user_id}_{self.symbol_id}_{self.quantity}@{self.buying_price}"