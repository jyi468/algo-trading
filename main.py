from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime
import os.path  # Manage paths
import sys  # Find out the script name (in argv[0
import backtrader as bt
from feeds.OandaCSVData import OandaCSVData
from trading.TradeStrategy import TradeStrategy

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    # Cerebro engine created broker instance in background

    # Add strategy - Optimize for different moving averages
    cerebro.optstrategy(
        TradeStrategy,
        maperiod=range(10, 31)
    )

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, 'datas/orcl-1995-2014.txt')

    # Create a Data Feed - Composed of different lines
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2000, 1, 1),
        # Do not pass values after this date
        todate=datetime.datetime(2000, 12, 31),
        reverse=False)

    # Add Data Feed to Cerebro
    cerebro.adddata(data)

    datalist = [
        ('datas/CAD_CHF-2005-2017-D1.csv', 'CADCHF'),
        ('datas/EUR_USD-2005-2017-D1.csv', 'EURUSD'),
        ('datas/GBP_AUD-2005-2017-D1.csv', 'GBPAUD'),
    ]

    # Add multiple data feeds
    for i in range(len(datalist)):
        data = OandaCSVData(dataname=datalist[i][0])
        cerebro.adddata(data, name=datalist[i][1])

    # Set cash
    cerebro.broker.setcash(1000.0)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # Set commission to 0.1%. Divide by 100 to remove %
    cerebro.broker.setcommission(commission=0.001)

    # instance already has cash to start with
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # run() loops over data
    cerebro.run(maxcpus=1)

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # cerebro.plot()