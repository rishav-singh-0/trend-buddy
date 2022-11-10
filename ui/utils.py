from data.populate import NSEPopulate
from bot.models import Holding, Trade

from datetime import datetime
from time import mktime

def make_data(df, holding, trades):
    
    data = []
    i = 0
    total_price = 0
    quantity = 0
    current_value = 0
    index = 0
    l = len(df)-1
    for i in trades:
        for j in range(index, len(df)):
            print(j, i.order_execution_time,df['Date '][l-j])
            if(i.order_execution_time>df['Date '][l-j]):
                print(index)
                index = j
                break

    for i, row in df.iterrows():
        date = datetime.fromtimestamp(row['Date '])
        print(i)
        print(row['Date '], trades[i].order_execution_time)
        if(row['Date ']==trades[i].order_execution_time):
            print(i, trades[i].price)
            i+=1
            if trades[i].trade_type=='BUY':
                total_price += trades[i].price * trades[i].quantity
                quantity+=i.quantity
            else:
                total_price -= trades[i].price * trades[i].quantity
                quantity-=i.quantity
            current_value = total_price / quantity        
        pnl = current_value - row['close ']

        data.append({
          'time': {
            'day': date.day,
            'month': date.month,
            'year': date.year,
          },
          'value': pnl,
        })
    return data

def calc_pnl(user):
    # calculate pnl and give data array
    holdings = Holding.objects.filter(user_id=user)
    trades = Trade.objects.filter(user_id=user)
    date_format = "%d-%m-%Y"
    candles = []
    for i in holdings:
        from_date = datetime.fromtimestamp(i.created_time).strftime(date_format)
        to_date = datetime.today().strftime(date_format)
        stock = NSEPopulate(i.symbol_id.symbol, from_date=from_date, to_date=to_date)
        stock.get_history_data()
        # stock.save_csv()
        new_candles = stock.save_candles()
        candles.append(stock.df)
        t = trades.filter(symbol_id=i.symbol_id).order_by('order_execution_time')
        data = make_data(stock.df, i, t)
        print(data)
        print(i.symbol_id,'\n\n')
        i.ltp = stock.df['close '][0]
        i.ltp_time = stock.df['Date '][0]
    holdings.update()
    # print(candles)
    


'''
{
  time: {
    day: 19,
    month: 10,
    year: 2018,
  },
  value: 180.095,
},
'''