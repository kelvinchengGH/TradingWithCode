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


    columnTitleToCodeLineMap = {
        "LongName" : "stock.longName",
        "Sector" : "stock.sector",
        "DividendYield" : "stock.dividendYield",
        "AllTimeHigh" : "stock.allTimeHigh",
        "PctFrom52WkHigh" : "stock.pctFromNDayHigh( 252 )",
        "LastClosingPrice": "stock.lastClosingPrice",
        "DividendYield" : "stock.dividendYield",
        "ForwardPE" : "stock.forwardPE",
        "1DayPctReturn" : "stock.nDayReturn( 1 )",
        "5DayPctReturn" : "stock.nDayReturn( 5 )",
    }

    @property
    def df( self ):
        # Edit the columns list with the stuff you want to include.
        # Make sure columnTitleToCodeLineMap supports each column.
        columns = [ "LongName",
                    "Sector",
                    "LastClosingPrice",
                    "AllTimeHigh",
                    "1DayPctReturn",
                    "5DayPctReturn",
                    "PctFrom52WkHigh",
                    "DividendYield",
                    "ForwardPE",
        ]

        data = { c : [] for c in columns }
        tickers = []

        for stock in self.stocks:
            try:
                # First make sure we can collect all the values.
                values = []
                for column in columns:
                    value = eval( self.columnTitleToCodeLineMap[ column ] )
                    values.append( value )
                # Now insert the values into the dictionary.
                for i, v in enumerate( values ):
                    column = columns[ i ]
                    data[ column ].append( v )
                tickers.append( stock.ticker )
            except Exception as e:
                print( e )
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
