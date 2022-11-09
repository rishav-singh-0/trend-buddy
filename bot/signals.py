from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Holding, Trade


@receiver(post_save, sender=Trade, dispatch_uid="update_stock_count")
@receiver(post_delete, sender=Trade, dispatch_uid="update_stock_count")
def update_holding(sender, instance, **kwargs):
    symbol = instance.symbol_id
    user = instance.user_id
    trades = Trade.objects.only('quantity','trade_type','price').filter(user_id=user,symbol_id=symbol)
    quantity = 0
    price = 0
    for i in trades:
        if i.trade_type=='BUY':
            quantity+=i.quantity
            price+=i.quantity*i.price
        else:
            quantity-=i.quantity
            price-=i.quantity*i.price
    if(quantity!=0):
        price = price / quantity
    else:
        Holding.objects.filter(user_id=user, symbol_id=symbol).delete()
        return
    holding, created = Holding.objects.update_or_create(
        user_id = user,
        symbol_id = symbol,
        defaults={
            'quantity':quantity,
            'buying_price':price,
            'ltp':price,
            'ltp_time':0
        },
    )
    # print(holding, created)

    