from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import numpy as np

# Import the backtrader platform
import backtrader as bt
from portfolio.Optimizer import Optimizer


# Create a Strategy
class TradeStrategy(bt.Strategy):
    # Class variables for params
    params = (
        ('maperiod', 15),
        ('printlog', False),
        ('use_target_percent', False),
        ('should_train', True),
        ('should_test', True)
    )

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function fot this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" lines
        self.dataclose = [self.datas[i].close for i in range(len(self.datas))]

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        # TODO: Convert indicators to torch tensors - Can pass tensor value each iteration of learning
        # https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
        self.indicators = {}
        for i, data in enumerate(self.datas):
            self.indicators[data] = {}
            self.indicators[data]['sma'] = bt.indicators.MovingAverageSimple(data, period=self.params.maperiod)
            self.indicators[data]['rsi'] = bt.indicators.RSI(data)
        self.sma = [bt.indicators.MovingAverageSimple(self.datas[i], period=self.params.maperiod)
                    for i in range(len(self.datas))]
        self.optimizer = Optimizer()

        # Indicators for the plotting show
        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25).subplot = True
        # bt.indicators.StochasticSlow(self.datas[0])
        # bt.indicators.MACDHisto(self.datas[0])
        # rsi = bt.indicators.RSI(self.datas[0])
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # bt.indicators.ATR(self.datas[0]).plot = False


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

    def next(self):
        for i, data in enumerate(self.datas):
            self.optimizer.compute_portfolio(self.get_state(self.indicators[data]))
            self.order = self.order_target_percent()

    def get_state(self, indicators):
        state = np.stack([indicators[key][0] for key in indicators.keys()])
        return state

    def stop(self):
        """Strategy hook. Called when data has been exhausted and backtesting over"""
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)
