import numpy
import talib

# Momentum Analysis

def rsi(candle):
    rsi = talib.RIS(candle.close, timeperiod=14)

def macd(candle):
    macd, macdsignal, macdhist = talib.MACD(candle.close, fastperiod=12, slowperiod=26, signalperiod=9)
    

# Patterns

def morning_star(candle):
    integer = talib.CDLMORNINGSTAR(candle.open, candle.high, candle.low, candle.close, penetration=0)
    
def evening_star(candle):
    integer = talib.CDLEVENINGSTAR(candle.open, candle.high, candle.low, candle.close, penetration=0)
    
def engulfing(candle):
    integer = talib.CDLENGULFING(candle.open, candle.high, candle.low, candle.close)

def hammer(candle):
    integer = talib.CDLHAMMER(candle.open, candle.high, candle.low, candle.close)

def hanging_man(candle):
    integer = talib.CDLHANGINGMAN(candle.open, candle.high, candle.low, candle.close)

def inverted_hammer(candle):
    integer = talib.CDLINVERTEDHAMMER(candle.open, candle.high, candle.low, candle.close)

def ladder_bottom(candle):
    integer = talib.CDLLADDERBOTTOM(candle.open, candle.high, candle.low, candle.close)

def rickshaw_man(candle):
    integer = talib.CDLRICKSHAWMAN(candle.open, candle.high, candle.low, candle.close)

def shooting_star(candle):
    integer = talib.CDLSHOOTINGSTAR(candle.open, candle.high, candle.low, candle.close)

