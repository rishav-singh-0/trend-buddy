import numpy as np
import talib

class Statergy():
    def __init__(self):

        # converting list of candles into indevidual arrays
        self.opens, self.highs, self.lows, self.closes = np.array([]), np.array([]), np.array([]), np.array([])
        # closes = [ item.close for item in self.candles ]
        # self.closes = np.array(closes)
        for candle in self.candles:
            np.append(self.opens, candle.open)
            np.append(self.highs, candle.high)
            np.append(self.lows, candle.low)
            np.append(self.closes, candle.close)


    # Momentum Analysis
    def rsi(self, candles, timeperiod, overbought, oversold):
        '''
        RSI - Relative Strength Index

        Input:
            - candles: list of candles
            - timeperiod: timeperiod for RSI calculation
            - overbought and oversold: for RSI calculation
        
        Output:
            - Returns True if RSI is in oversold region 
            and False if RSI is in oversold region
        '''

        rsi_list = talib.RSI(self.closes, timeperiod=timeperiod)
        latest_rsi = rsi_list[-1]
        print(f"The current rsi is {latest_rsi}")

        if latest_rsi > overbought:
            print("Overbought! Sell! Sell! Sell!")
            return False
        elif latest_rsi < oversold:
            print("Oversold! Buy! Buy! Buy!")
            return True


    def macd(self, candles):
        '''
        MACD - Moving Averages Convergence Divergence

        Input:
            - candles: list of candles
            - fastperiod: timeperiod for RSI calculation
            - slowperiod
            - signalperiod
        
        Output:
            - Returns True if RSI is in oversold region 
            and False if RSI is in oversold region
        '''

        self.macd, self.macdsignal, self.macdhist = talib.MACD(self.closes, fastperiod=12, slowperiod=26, signalperiod=9)
        print('macdhist:\n',self.macdhist)
        if self.macdhist[-1] > 0:
            return True
        return False


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

