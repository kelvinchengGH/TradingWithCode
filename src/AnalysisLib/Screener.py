#!/usr/bin/env python

############
# Imports
############

from typing import Optional
import os
from functools import cached_property

import pandas as pd
from pandas import DataFrame

from AnalysisLib import Stock
from UtilLib.Util import absolutePathLocator


############
# Functions and Classes
############

class Screener:
    def __init__( self, tickers: Optional[list[str]] = None, useLiveStatus: bool = False ) -> None:
        if tickers is None:
            relativeCsvDirPath = 'data/RawData/DailyPriceCsvs/'
            csvDirPath = absolutePathLocator( relativeCsvDirPath )
            csvs = os.listdir( csvDirPath )
            tickers = [ filename[:-4] for filename in csvs if filename.endswith( '.csv' ) ]
        self.stocks = [ Stock.Stock( t, useLiveStatus ) for t in sorted( tickers ) ]

    def getSectors( self ) -> list[str]:
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
        "AllTimeHigh" : "stock.allTimeHigh",
        "PctFrom52WkHigh" : "stock.pctFromNDayHigh( 252 )",
        "LastClosingPrice": "stock.lastClosingPrice",
        "DividendYield" : "stock.dividendYield * 100.0",
        "ForwardPE" : "stock.forwardPE",
        "1DayPctReturn" : "stock.nDayReturn( 1 )",
        "5DayPctReturn" : "stock.nDayReturn( 5 )",
        "MarketCap" : "'%.2e' % stock.marketCap",
        "ShortPercentOfFloat" : "stock.shortPercentOfFloat * 100.0"
    }

    @cached_property
    def df( self ) -> DataFrame:
        # Edit the columns list with the stuff you want to include.
        # Make sure columnTitleToCodeLineMap supports each column.
        columns = [ "LongName",
                    "Sector",
                    "MarketCap",
                    "LastClosingPrice",
                    "AllTimeHigh",
                    "1DayPctReturn",
                    "5DayPctReturn",
                    "PctFrom52WkHigh",
                    "DividendYield",
                    "ForwardPE",
        ]

        data: dict[str, list] = { c : [] for c in columns }
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
def main() -> None:
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
