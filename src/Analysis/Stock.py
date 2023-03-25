#!/usr/bin/env python3

############
# Imports
############

import os, datetime, json
import pandas as pd
import yfinance as yf
from functools import cached_property

############
# Constants
############

ROOT_DIR = os.path.realpath( os.path.join( os.path.dirname( __file__ ), '../..' ) )


############
# Stock
############

class Stock( object ):
    def __init__( self, ticker ):
        self.ticker = ticker
        self.yfTicker = yf.Ticker( ticker )
        self.csvFile = ''

    @property
    def history( self ):
        # Returns the yfTicker's history method
        return self.yfTicker.history

    @cached_property
    def maxHistoryDf( self ):
        filePath = ROOT_DIR + '/data/ProcessedData/DailyClosingPriceCsvs/%s.csv' % self.ticker
        df = pd.read_csv( filePath, index_col='Date', parse_dates=True,
                          na_values=[ 'nan' ] )
        return df
        # return self.history( period='max' )

    @cached_property
    def info( self ):
        # Returns the yfTicker's info dict
        # TODO:
        #    1. Check if the JSON exists and is up-to-date.
        #    2. If the JSON does not exist or is out of date, update it.
        filePath = ROOT_DIR + '/data/RawData/YahooFinanceInfo/%s.json' % self.ticker
        with open( filePath, 'r' ) as f:
            d = json.load( f )
        return d
        # return self.yfTicker.info

    @cached_property
    def financialsDf( self ):
        filePath = ROOT_DIR + '/data/RawData/FinacialsFromMacrotrends/%s.csv' % self.ticker
        df = pd.read_csv( filePath, index_col='Year', na_values=[ 'NaN' ] )
        return df

    ##### Basic Attributes #####
    @property
    def longName( self ):
        return self.info[ 'longName' ]

    @property
    def forwardPE( self ):
        '''
        "forwardPE" is the metric that yfinance would provide, but
        since we can't access it now, we just return an estimate of the PE ratio
        using the most recent full year's EPS.
        '''
        try:
            df = self.financialsDf
            mostRecentYearsEarnings = df.iloc[ -1 ][ 'eps-earnings-per-share-diluted' ]
            if mostRecentYearsEarnings <= 0:
                return 'NaN'
            return round( self.lastClosingPrice / mostRecentYearsEarnings, 2 )
        except:
            return 'NaN'
        # return self.info[ 'forwardPE' ]

    @cached_property
    def dividends( self ):
        '''
        Return a Pandas Dataframe with the past dividends.
        >>> s = Stock.Stock( 'AAPL' )
        >>> s.dividends
                                 Date  Dividends
        0   1987-05-11 00:00:00-04:00   0.000536
        1   1987-08-10 00:00:00-04:00   0.000536
        2   1987-11-17 00:00:00-05:00   0.000714
        3   1988-02-12 00:00:00-05:00   0.000714
        4   1988-05-16 00:00:00-04:00   0.000714
        ..                        ...        ...
        73  2022-02-04 00:00:00-05:00   0.220000
        74  2022-05-06 00:00:00-04:00   0.230000
        75  2022-08-05 00:00:00-04:00   0.230000
        76  2022-11-04 00:00:00-04:00   0.230000
        77  2023-02-10 00:00:00-05:00   0.230000

        [78 rows x 2 columns]
        '''
        filePath = ROOT_DIR + '/data/RawData/Dividends/%s.csv' % self.ticker
        df = pd.read_csv( filePath )
        return df

    @property
    def oneYearDividendTotal( self ):
        '''
        The sum of the dividends paid out in the last year.
        '''
        df = self.dividends.copy()
        df.Date = df.Date.apply( lambda x: x[:10])
        df[ 'Date' ] = pd.to_datetime(df['Date'])
        oneYearAgo = datetime.datetime.now() - datetime.timedelta(365)
        oneYearDividendTotal = df[ df[ 'Date' ] >= oneYearAgo ].Dividends.sum()
        return oneYearDividendTotal

    @property
    def dividendYield( self ):
        # Need to manually compute the dividendYield because
        # yfinance's "info" feature is blocked.
        # res = self.info[ 'dividendYield' ]
        # return res * 100 if res else 0
        return 100.0 * self.oneYearDividendTotal / self.lastClosingPrice

    @property
    def shortPercentOfFloat( self ):
        return self.info[ 'shortPercentOfFloat' ]

    @property
    def sector( self ):
        return self.info[ 'sector' ]
    
    ##### Basic Price Metrics #####
    @property
    def allTimeHigh( self ):
        return self.maxHistoryDf[ 'Close' ].max()

    @property
    def allTimeLow( self ):
        return self.maxHistoryDf[ 'Close' ].min()

    @property
    def lastClosingPrice( self ):
        return self.maxHistoryDf[ 'Close' ][-1]

    @property
    def pctFromAllTimeHigh( self ):
        return 100 * ( self.lastClosingPrice - self.allTimeHigh ) / self.allTimeHigh
    
    ##### Intermediate Price Metrics #####
    def nDayHigh( self, n ):
        idx = -1 * n
        return self.maxHistoryDf[ 'Close' ].iloc[ idx: ].max()

    def nDayLow( self, n ):
        idx = -1 * n
        return self.maxHistoryDf[ 'Close' ].iloc[ idx: ].min()

    def pctFromNDayHigh( self, n ):
        high = self.nDayHigh( n )
        return 100 * ( self.lastClosingPrice - high ) / high

    def pctFromNDayLow( self, n ):
        low = self.nDayLow( n )
        return 100 * ( self.lastClosingPrice - low ) / low

    def nDayReturn( self, n ):
        idx = -1 * ( n + 1 )
        oldPrice = self.maxHistoryDf[ 'Close' ].iloc[ idx ]
        return 100 * ( self.lastClosingPrice - oldPrice ) / oldPrice

    def nYearReturn( self, n ):
        # TODO: Fill me in
        return 0

    @property
    def ytdReturn( self ):
        # TODO: Fill me in
        return 0

############
# main()
############
def main():
    data = {
        'LastClosingPrice' : [],
        'AllTimeHigh' : [],
        'PctFromATH' : [],
        'DividendYield' : [],
        'ForwardPE' : [],
    }
    tickers = [ "ANET", "AMZN", "BAC", "INTC", "JPM", "TSLA" ]
    for ticker in tickers:
        stock = Stock( ticker )
        data[ 'LastClosingPrice' ].append( stock.lastClosingPrice )
        data[ 'AllTimeHigh' ].append( stock.allTimeHigh )
        data[ 'PctFromATH' ].append( stock.pctFromAllTimeHigh )
        data[ 'DividendYield' ].append( stock.dividendYield )
        data[ 'ForwardPE' ].append( stock.forwardPE )

    df = pd.DataFrame( data, index=tickers )
    print( df.round( 2 ) )


if __name__ == '__main__':
    main()
