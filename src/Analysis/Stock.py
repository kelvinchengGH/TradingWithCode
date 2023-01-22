#!/usr/bin/env python3

############
# Imports
############

import os, json
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


    ##### Basic Attributes #####
    @property
    def longName( self ):
        return self.info[ 'longName' ]

    @property
    def forwardPE( self ):
        return self.info[ 'forwardPE' ]

    @property
    def dividendYield( self ):
        res = self.info[ 'dividendYield' ]
        return res * 100 if res else 0

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
    def fiftyTwoWeekHigh( self ):
        return self.info[ 'fiftyTwoWeekHigh' ]

    @property
    def lastClosingPrice( self ):
        return self.maxHistoryDf[ 'Close' ][-1]

    @property
    def pctFromAllTimeHigh( self ):
        return 100 * ( self.lastClosingPrice - self.allTimeHigh ) / self.allTimeHigh
    
    @property
    def pctFromFiftyTwoWeekHigh( self ):
        return 100 * ( self.lastClosingPrice - self.fiftyTwoWeekHigh ) / self.fiftyTwoWeekHigh

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
