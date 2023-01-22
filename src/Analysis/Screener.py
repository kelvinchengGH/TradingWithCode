#!/usr/bin/env python3

############
# Imports
############

import os
from functools import cached_property
import pandas as pd
import Stock


############
# Constants
############

ROOT_DIR = os.path.realpath( os.path.join( os.path.dirname( __file__ ), '../..' ) )


############
# Functions and Classes
############

class Screener( object ):
    def __init__( self ):
        csvDirPath = ROOT_DIR + '/data/RawData/DailyPriceCsvs/'
        csvs = os.listdir( csvDirPath )
        tickers = [ filename[:-4] for filename in csvs if filename.endswith( '.csv' ) ]
        self.stocks = [ Stock.Stock( t ) for t in sorted( tickers ) ]

    def getSectors( self ):
        sectors = set()
        for stock in self.stocks:
            try:
                sectors.add( stock.sector )
            except:
                pass
        return sorted( list( sectors ) )

    @property
    def df( self ):
        data = {
            'LongName' : [],
            'Sector' : [],
            'LastClosingPrice' : [],
            'AllTimeHigh' : [],
            'PctFrom52WkHigh' : [],
            'PctFromATH' : [],
            'DividendYield' : [],
            'ForwardPE' : [],
        }
        tickers = []
        for stock in self.stocks:
            try:
                longName = stock.longName
                sector = stock.sector
                lastClosingPrice = stock.lastClosingPrice
                allTimeHigh = stock.allTimeHigh
                pctFromAllTimeHigh = stock.pctFromAllTimeHigh
                pctFromFiftyTwoWeekHigh = stock.pctFromFiftyTwoWeekHigh
                dividendYield = stock.dividendYield
                forwardPE = stock.forwardPE
                data[ 'LongName' ].append( longName )
                data[ 'Sector' ].append( sector )                
                data[ 'LastClosingPrice' ].append( lastClosingPrice )
                data[ 'AllTimeHigh' ].append( allTimeHigh )
                data[ 'PctFromATH' ].append( pctFromAllTimeHigh )
                data[ 'PctFrom52WkHigh' ].append( pctFromFiftyTwoWeekHigh )
                data[ 'DividendYield' ].append( dividendYield )
                data[ 'ForwardPE' ].append( forwardPE )
                tickers.append( stock.ticker )
            except:
                print( "failed to create DataFrame row for %s" % stock.ticker )
                pass
        df = pd.DataFrame( data, index=tickers )
        df = df.round( 2 )
        return df
    

############
# main()
############
def main():
    screener = Screener()
    sectors = screener.getSectors()
    print( "*** Sectors of the market:" )
    for sector in sectors:
        print( sector )

    df = screener.df
    for sector in screener.getSectors():
        print( "*** %s ***" % sector )
        df1 = df[ (df.DividendYield >= 1.5) & (df.Sector == sector ) & (df. PctFrom52WkHigh <= -25 ) ]
        df1 = df1[ [ 'LongName', 'PctFrom52WkHigh', 'DividendYield', 'ForwardPE' ] ]
        print( df1.sort_values( by=['PctFrom52WkHigh'] ).to_string() )
        print( '\n\n' )

if __name__ == '__main__':
    main()
