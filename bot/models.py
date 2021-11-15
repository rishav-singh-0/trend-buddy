from django.db import models
from django.contrib.auth.models import User
from data.models import Symbol


class Order(models.Model):
    CHOICE = (
        ('BUY', 'BUY'),
        ('SELL', 'SELL'),
    )

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    symbol_id = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='order')
    type = models.CharField(max_length=5, choices=CHOICE)
    amount = models.FloatField()
    price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id}_{self.symbol_id}@{self.date.strftime('%Y_%m_%d-%H_%M_%S')}"
