import numpy as np
import talib

class Statergy():
    def __init__(self, candles):

        # converting list of candles into indevidual arrays
        self.opens, self.highs, self.lows, self.closes = np.array([]), np.array([]), np.array([]), np.array([])
        for candle in candles:
            self.opens = np.append(self.opens, candle.open)
            self.highs = np.append(self.highs, candle.high)
            self.lows = np.append(self.lows, candle.low)
            self.closes = np.append(self.closes, candle.close)


    # Momentum Analysis
    def rsi(self, timeperiod=14, overbought=70, oversold=30):
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

        # Generating RSI for given ranges
        self.rsi_list = talib.RSI(self.closes, timeperiod=timeperiod)

        # Pridicting buy or sell call based on generated RSI
        latest_rsi = self.rsi_list[-1]
        print(f"The current rsi is {latest_rsi}")

        if latest_rsi > overbought:
            print("Overbought! Sell! Sell! Sell!")
            return False
        elif latest_rsi < oversold:
            print("Oversold! Buy! Buy! Buy!")
            return True


    def macd(self, fastperiod=12, slowperiod=26, signalperiod=9):
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

        self.macd_list, self.macdsignal, self.macdhist = talib.MACD(
            self.closes, 
            fastperiod=fastperiod, 
            slowperiod=slowperiod, 
            signalperiod=signalperiod
        )

        print('macdhist:\n',self.macdhist)
        if self.macdhist[-1] > 0:
            return True
        return False


    # Patterns
    def morning_star(self):
        integer = talib.CDLMORNINGSTAR(self.open, self.high, self.low, self.close, penetration=0)
        
    def evening_star(self):
        integer = talib.CDLEVENINGSTAR(self.open, self.high, self.low, self.close, penetration=0)
        
    def engulfing(self):
        integer = talib.CDLENGULFING(self.open, self.high, self.low, self.close)

    def hammer(self):
        integer = talib.CDLHAMMER(self.open, self.high, self.low, self.close)

    def hanging_man(self):
        integer = talib.CDLHANGINGMAN(self.open, self.high, self.low, self.close)

    def inverted_hammer(self):
        integer = talib.CDLINVERTEDHAMMER(self.open, self.high, self.low, self.close)

    def ladder_bottom(self):
        integer = talib.CDLLADDERBOTTOM(self.open, self.high, self.low, self.close)

    def rickshaw_man(self):
        integer = talib.CDLRICKSHAWMAN(self.open, self.high, self.low, self.close)

    def shooting_star(self):
        integer = talib.CDLSHOOTINGSTAR(self.open, self.high, self.low, self.close)

