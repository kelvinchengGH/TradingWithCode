#!/usr/bin/env python3

############
# Imports
############

from typing import Callable

import os, datetime, json
from functools import cached_property

import pandas as pd
from pandas import DataFrame
import yfinance as yf


from UtilLib.Util import absolutePathLocator


############
# Stock
############

class LiveStatus:
    """
    Provides the latest data directly from Yahoo! Finance
    """
    def __init__( self, yfTicker: yf.Ticker ) -> None:
        self.yfTicker = yfTicker

    @cached_property
    def info( self ) -> dict:
        return self.yfTicker.info

    @cached_property
    def fastInfo( self ) -> dict:
        return dict(self.yfTicker.fast_info)

    @cached_property
    def maxHistoryDf( self ) -> DataFrame:
        return self.yfTicker.history( period='max' )


class History:
    """
    Contains historical data read from local files.

    This can be helpful if you're offline or if the Yahoo! Finance API
    behavior changes unexpectedly.
    """
    def __init__( self, ticker: str ) -> None:
        self.ticker = ticker

    @cached_property
    def info( self ) -> dict:
        relativeFilePath = 'data/RawData/YahooFinanceInfo/%s.json' % self.ticker
        filePath = absolutePathLocator( relativeFilePath )
        with open( filePath, 'r' ) as f:
            d = json.load( f )
        return d

    @cached_property
    def fastInfo( self ) -> dict:
        relativeFilePath = 'data/RawData/YahooFinanceFastInfo/%s.json' % self.ticker
        filePath = absolutePathLocator( relativeFilePath )
        with open( filePath, 'r' ) as f:
            d = json.load( f )
            return d

    @cached_property
    def maxHistoryDf( self ) -> DataFrame:
        relativeFilePath = 'data/ProcessedData/DailyClosingPriceCsvs/%s.csv' % self.ticker
        filePath = absolutePathLocator( relativeFilePath )
        df = pd.read_csv( filePath, index_col='Date', parse_dates=True,
                          na_values=[ 'nan' ] )
        return df

class Stock:
    def __init__( self, ticker: str, useLiveStatus: bool = False ) -> None:
        """
        useLiveStatus specifies if you want to fetch the latest data 
        using Yahoo! Finance.
           - I make it False by default because fetching the latest data 
             this way can be slow.
        """
        self.ticker = ticker
        self.yfTicker = yf.Ticker( ticker )

        self.useLiveStatus = useLiveStatus
        self.liveStatus = LiveStatus( self.yfTicker )
        self.history = History( ticker )

    @cached_property
    def info( self ) -> dict:
        if not self.useLiveStatus:
            return self.history.info
        try:
            return self.liveStatus.info
        except Exception as e:
            return self.history.info

    @cached_property
    def fastInfo( self ) -> dict:
        if not self.useLiveStatus:
            return self.history.fastInfo
        try:
            return self.liveStatus.fastInfo
        except Exception as e:
            return self.history.fastInfo

    @cached_property
    def maxHistoryDf( self ) -> DataFrame:
        if not self.useLiveStatus:
            return self.history.maxHistoryDf
        try:
            return self.liveStatus.maxHistoryDf
        except Exception as e:
            return self.history.maxHistoryDf

    @cached_property
    def financialsDf( self ) -> DataFrame:
        relativeFilePath = 'data/RawData/FinacialsFromMacrotrends/%s.csv' % self.ticker
        filePath = absolutePathLocator( relativeFilePath )
        df = pd.read_csv( filePath, index_col='Year', na_values=[ 'NaN' ] )
        return df

    ##### Basic Attributes #####
    @property
    def longName( self ) -> str:
        return self.info[ 'longName' ]

    @property
    def shares( self ) -> int:
        ''' Shares Outstanding '''
        return self.fastInfo[ 'shares' ]

    @property
    def marketCap( self ) -> float:
        return self.fastInfo[ 'marketCap' ]

    @property
    def forwardPE( self ) -> float:
        '''
        "forwardPE" is the metric that yfinance would provide, but
        since we can't access it now, we just return an estimate of the PE ratio
        using the most recent full year's EPS.
        '''
        try:
            df = self.financialsDf
            mostRecentYearsEarnings = df.iloc[ -1 ][ 'eps-earnings-per-share-diluted' ]
            if mostRecentYearsEarnings <= 0:
                return -1
            return self.lastClosingPrice / mostRecentYearsEarnings
        except:
            return -1

    @cached_property
    def dividends( self ) -> DataFrame:
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
        relativeFilePath = 'data/RawData/Dividends/%s.csv' % self.ticker
        filePath = absolutePathLocator( relativeFilePath )
        df = pd.read_csv( filePath )
        return df

    @property
    def oneYearDividendTotal( self ) -> float:
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
    def dividendYield( self ) -> float:
        # Need to manually compute the dividendYield because
        # yfinance's "info" feature is blocked.
        # res = self.info[ 'dividendYield' ]
        # return res * 100 if res else 0
        return 100.0 * self.oneYearDividendTotal / self.lastClosingPrice

    @property
    def shortPercentOfFloat( self ) -> float:
        return self.info[ 'shortPercentOfFloat' ]

    @property
    def sector( self ) -> str:
        return self.info[ 'sector' ]
    
    ##### Basic Price Metrics #####
    @property
    def allTimeHigh( self ) -> float:
        return self.maxHistoryDf[ 'Close' ].max()

    @property
    def allTimeLow( self ) -> float:
        return self.maxHistoryDf[ 'Close' ].min()

    @property
    def lastClosingPrice( self ) -> float:
        return self.maxHistoryDf[ 'Close' ].iloc[-1]

    @property
    def pctFromAllTimeHigh( self ) -> float:
        return 100 * ( self.lastClosingPrice - self.allTimeHigh ) / self.allTimeHigh
    
    ##### Intermediate Price Metrics #####
    def nDayHigh( self, n: int ) -> float:
        idx = -1 * n
        return self.maxHistoryDf[ 'Close' ].iloc[ idx: ].max()

    def nDayLow( self, n: int ) -> float:
        idx = -1 * n
        return self.maxHistoryDf[ 'Close' ].iloc[ idx: ].min()

    def pctFromNDayHigh( self, n: int ) -> float:
        high = self.nDayHigh( n )
        return 100 * ( self.lastClosingPrice - high ) / high

    def pctFromNDayLow( self, n: int ) -> float:
        low = self.nDayLow( n )
        return 100 * ( self.lastClosingPrice - low ) / low

    def nDayReturn( self, n: int ) -> float:
        idx = -1 * ( n + 1 )
        oldPrice = self.maxHistoryDf[ 'Close' ].iloc[ idx ]
        return 100 * ( self.lastClosingPrice - oldPrice ) / oldPrice

    def nYearReturn( self, n: int ) -> float:
        # TODO: Fill me in
        return 0

    @property
    def ytdReturn( self ) -> float:
        # TODO: Fill me in
        return 0

############
# main()
############
def main() -> None:
    data: dict[str, list] = {
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
