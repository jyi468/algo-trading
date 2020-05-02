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
        # Keep a reference to the "close" line in the datas[0] data feed
        self.dataclose = self.datas[0].close

        # Keep track of pending orders
        self.order = None
        self.bar_executed = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # buy/sell order submitted/accepted to/by broker - nothing to do
            return

        # Check if order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

    def next(self):
        # This method called on each bar of the system clock (self.datas[0])
        # True until things like indicators, which need some bars to start producing
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending. If TRUE, we cannot send a 2nd one
        if self.order:
            return

        # Check if we're in the market
        # If we aren't, we can buy
        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close
                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than previous close
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    # Basically if price has fell for 3 sessions, we buy
                    self.buy()
        else:
            # Already in market, might sell
            if len(self) >= (self.bar_executed + 5):
                # SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
