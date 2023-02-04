#!/usr/bin/env python

import os
import pandas as pd

THIS_DIR = os.path.dirname( __file__ )
ROOT_DIR = os.path.realpath( os.path.join( THIS_DIR, '../../..' ) )
RAW_CSV_DIR = ROOT_DIR + '/data/RawData/DailyPriceCsvs'

def createCondensedCsv( ticker ):
    rawCsvPath = RAW_CSV_DIR + '/%s.csv' % ticker
    df = pd.read_csv( rawCsvPath )
    df = df[ [ 'Date', 'Close' ] ]
    df[ 'Date' ] = df[ 'Date' ].apply( lambda dateStr: dateStr[:10] )
    df[ 'Close' ] = df[ 'Close' ].apply( lambda price: "%.2f" % price )
    newCsvPath = THIS_DIR +  '/%s.csv' % ticker
    df.to_csv( newCsvPath, index=False )

def populate():
    csvList = os.listdir( RAW_CSV_DIR )
    tickers = [ filename[:-4] for filename in csvList if filename.endswith( '.csv' ) ]
    for ticker in tickers:
        createCondensedCsv( ticker )
    



if __name__ == '__main__':
    populate()
