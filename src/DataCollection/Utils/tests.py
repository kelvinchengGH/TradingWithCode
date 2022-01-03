#!/usr/bin/python

'''
Unit tests to make sure the code works properly.

TODOs:
- Learn how to implement unit tests professionally.
'''

import MacrotrendsUtil

def testMacrotrendsUtil():
    ticker = 'AAPL'
    metric = 'net-income'
    html = MacrotrendsUtil.getPageSource( ticker, metric )
    dataDict = MacrotrendsUtil.getAnnualData( ticker, metric )

    tickers = [ 'AAPL', 'GOOG' ]
    metrics = [ 'net-income', 'revenue' ]
    df = MacrotrendsUtil.getDataFrame( tickers, metrics )
    print df.head()

if __name__ == '__main__':
    testMacrotrendsUtil()
    print '*** ALL UNIT TESTS PASSED ***'
