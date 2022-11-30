import os, json
import pandas as pd
import yfinance as yf
from Utils import cachedproperty


ROOT_DIR = os.path.realpath( os.path.join( os.path.dirname( __file__ ), '../..' ) )
print ROOT_DIR

class Stock( object ):
    def __init__( self, ticker ):
        self.ticker = ticker
        self.yfTicker = yf.Ticker( ticker )
        self.csvFile = ''

    @property
    def history( self ):
        # Returns the yfTicker's history method
        return self.yfTicker.history

    @cachedproperty
    def maxHistoryDf( self ):
        filePath = ROOT_DIR + '/data/RawData/DailyPriceCsvs/%s.csv' % self.ticker
        df = pd.read_csv( filePath, index_col='Date', parse_dates=True,
                          na_values=[ 'nan' ] )
        return df
        # return self.history( period='max' )
    
    @cachedproperty
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


    @property
    def forwardPE( self ):
        return self.info[ 'forwardPE' ]

    @property
    def dividendYield( self ):
        return self.info[ 'dividendYield' ]

    @property
    def pctFromAllTimeHigh( self ):
        df = self.maxHistoryDf
        lastClosingPrice = df[ 'Close' ][-1]
        allTimeHigh = df[ 'Close' ].max()
        pctChange = ( lastClosingPrice - allTimeHigh ) / allTimeHigh
        return pctChange
    
    @property
    def shortPercentOfFloat( self ):
        return self.info[ 'shortPercentOfFloat' ]
