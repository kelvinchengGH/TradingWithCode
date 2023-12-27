#!/usr/bin/python

'''
Unit tests to make sure the code works properly.

TODOs:
- Learn how to implement unit tests professionally.
'''

import tempfile, os
import MacrotrendsUtil
import RawDataUtil

def testMacrotrendsUtil() -> None:
    ticker = 'AAPL'
    metric = 'net-income'
    html = MacrotrendsUtil.getPageSource( ticker, metric )
    dataDict = MacrotrendsUtil.getAnnualData( ticker, metric )
    
    tickers = [ 'AAPL', 'GOOG' ]
    metrics = [ 'net-income', 'revenue' ]
    df = MacrotrendsUtil.getDataFrame( tickers, metrics )
    print( df.head() )
    

def testRawDataUtil() -> None:
    # Get CSV for ANET
    # Get JSON for ANET
    # Read dataframe for ANET
    ticker = 'ANET'
    csvFile = '%s.csv' % ticker
    jsonFile = '%s.json' % ticker
    RawDataUtil.getDailyPriceCsv( ticker, csvFile )
    RawDataUtil.getYahooFinanceInfoDict( ticker, jsonFile )
    os.system( 'rm %s %s' % ( csvFile, jsonFile ) )


def main() -> None:
    testList = [
        testRawDataUtil,
        testMacrotrendsUtil
    ]
    
    failedTests = []
    for test in testList:
        testName = test.__name__
        print( '*** Starting %s' % testName )
        try:
            test()
        except:
            print( "*** %s got an exception" % testName )
            failedTests.append( testName )
        else:
            print( "*** %s passed" % testName )
        print()

    if failedTests:
        print( "*** The following tests failed:" )
        for test in failedTests:
            print( "   " + test )
    else:
        print( "*** ALL TESTS PASSED!" )
   

if __name__ == '__main__':
    main()
