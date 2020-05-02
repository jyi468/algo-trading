import backtrader as bt


class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # When init is called, the strategy already has a list of datas present in the platform
        # self.datas is a list of data feeds
        # self.datas[0] is the default data feed for trading operations and
        # keeping all strategy elements synched (system clock)
        # self.datas[0] is a reference to the close line
        # Keep a reference to the "close" line in the datas[0] dataseries
        self.dataclose = self.datas[0].close

    def next(self):
        # This method called on each bar of the system clock (self.datas[0])
        # True until things like indicators, which need some bars to start producing
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        if self.dataclose[0] < self.dataclose[-1]:
            # current close less than previous close
            if self.dataclose[-1] < self.dataclose[-2]:
                # previous close less than previous close
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                # Basically if price has fell for 3 sessions, we buy
                self.buy()
