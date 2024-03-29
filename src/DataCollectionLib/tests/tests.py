#!/usr/bin/env python

'''
Unit tests to make sure the code works properly.

TODOs:
- Learn how to implement unit tests professionally.
'''

import os, json
import yfinance as yf
import pandas as pd

from DataCollectionLib import MacrotrendsUtil, RawDataUtil



def testYfinance() -> None:
    ticker = 'AAPL'
    yfTicker = yf.Ticker( ticker )
    info = yfTicker.info

    currentPrice = info[ 'currentPrice' ]
    print( '%s Current Price: $%.2f\n' % ( ticker, currentPrice ) )

    dividendDf = yfTicker.dividends
    print( '%s Dividend History:' % ticker )
    print( dividendDf[-4:] )
    print()

    df = yfTicker.history( period='1wk' )
    print( '%s 1-Week Price History:' % ticker )
    print( df )
    print()


def testMacrotrendsUtil() -> None:
    ticker = 'AAPL'
    metric = 'net-income'
    _ = MacrotrendsUtil.getPageSource( ticker, metric )
    _ = MacrotrendsUtil.getAnnualData( ticker, metric )

    tickers = [ 'AAPL', 'GOOG' ]
    metrics = [ 'net-income', 'revenue' ]
    df = MacrotrendsUtil.getDataFrame( tickers, metrics )
    print( df.head() )


def testGetDailyPriceCsv() -> None:
    ticker = 'MSFT'
    csvFile = '%s.csv' % ticker
    RawDataUtil.getDailyPriceCsv( ticker, csvFile )
    df = pd.read_csv( csvFile )
    print( "Truncated %s Price History Read From CSV:" % ticker )
    print( df[-4:] )
    print()
    os.system( 'rm %s' % csvFile )


def testGetYahooFinanceInfoDict() -> None:
    ticker = 'MSFT'
    jsonFile = '%s.json' % ticker
    RawDataUtil.getYahooFinanceInfoDict( ticker, jsonFile )
    with open( jsonFile, 'r' ) as f:
        info = json.load( f )

    numKeys = 4
    truncatedInfo = { k: info[k] for k in list(info.keys())[:numKeys] }
    print( "Truncated %s Info Read From JSON:" % ticker )
    print( json.dumps( truncatedInfo, indent=4 ) )
    print()
    os.system( 'rm %s' % jsonFile )



def main() -> None:
    testList = [
        testYfinance,
        testGetDailyPriceCsv,
        testGetYahooFinanceInfoDict,

        # TODO: Uncomment this once I've got it working reliably and efficiently.
        # testMacrotrendsUtil
    ]

    failedTests = []
    for test in testList:
        testName = test.__name__
        print( '[TEST START] %s' % testName )
        try:
            test()
        except:
            print( "[TEST FAILED] %s got an exception" % testName )
            failedTests.append( testName )
        else:
            print( "[TEST PASSED] %s" % testName )
        print( '-' * 85 )

    if failedTests:
        print( "*** The following tests failed:" )
        for testName in failedTests:
            print( "   " + testName)
    else:
        print( "*** ALL TESTS PASSED!" )


if __name__ == '__main__':
    main()
