from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    # Cerebro engine created broker instance in background
    # instance already has cash to start with
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.broker.set_cash(100000.0)
    # run() loops over data
    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())