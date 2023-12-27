#!/usr/bin/env python

'''
By Kelvin Cheng.

Tools for scraping and parsing data from Macrotrends.
'''

################
##### TODOs
################
'''
- Add proper documentation for everything.
- Add feature to save DataFrames as CSVs.
- Add unit tests so we can automatically validate changes to the code.
- Add a guide to list the different types of data we can grab.
- Improve the error-handling for when a site doesn't exist or data is incomplete.
'''


################
##### IMPORTS
################
import os, re
import argparse

import requests
from bs4 import BeautifulSoup

import pandas as pd

################
##### CONSTANTS
################

# Example URLs:
#   https://www.macrotrends.net/stocks/charts/JPM/jpmorgan-chase/net-income
#
# Note: Using "JPM/jpm" works just the same as "JPM/jpmorgan-chase".
#       Looks like Macrotrends
#       designed their site to be nice to web scrapers like us. :)
MACROTRENDS_URL_TEMPLATE = 'https://www.macrotrends.net/stocks/charts/%s/%s'

ESSENTIAL_METRICS = [ 'net-income',
                      'revenue',
                      'total-share-holder-equity',
                      'free-cash-flow',
                      'cash-flow-from-operating-activities',
                      'eps-earnings-per-share-diluted'
]

THIS_DIR = os.path.dirname( __file__ )
ROOT_DIR = os.path.realpath( os.path.join( os.path.dirname( __file__ ), '../../..' ) )
FINANCIAL_INFO_DIR = ROOT_DIR + "/data/RawData/FinacialsFromMacrotrends"


################
##### FUNCTIONS
################

def getPageSource( ticker, metric ):
   '''
   Returns a string with the HTML corresponding to the Macrotrends page
   for the given ticker and metric.

   Params:
      ticker - ticker symbol of the comapny.
      metric - financial metric of interest, with dashes separating each word.

   Example:
      If ticker == "JPM" and metric == "net-income",
      then the function returns a string containing the HTML for
      https://www.macrotrends.net/stocks/charts/JPM/jpm/net-income
   '''
   tickerStr = "%s/%s" % ( ticker, ticker.lower() )
   url = MACROTRENDS_URL_TEMPLATE % ( tickerStr, metric )
   r = requests.get( url )
   data = r.text
   return data

def getAnnualData( ticker, metric ):
   '''
   Returns a dictionary where the key is the year and the value
   is the value of the metric for that year.

   Params:
      ticker - ticker symbol of the comapny.
      metric - financial metric of interest, with dashes separating each word.

   Example:
      >>> dataDict = MacrotrendsUtil.getAnnualData( 'JPM', 'net-income' )
      >>> for year in sorted( dataDict.keys() ):
      ...    year, dataDict[ year ]
      ... 
      (2005, 8470000000.0)
      (2006, 14440000000.0)
      (2007, 14924000000.0)
      etc.
   '''
   data = getPageSource( ticker, metric )
   soup = BeautifulSoup( data, 'html.parser' )

   # Find the table with the annual values.
   tables = soup.find_all( 'table' )
   annualDataTable = tables[ 0 ]
   tableRows = annualDataTable.find_all( 'tr' )

   # Some tables show values in Millions of US $
   tableHeader = annualDataTable.find( 'th' ).text
   multiplyByOneMillion = 'Millions of US $' in tableHeader

   # Go through each row of the table ( except the header row ),
   # and extract the year and the value.
   yearToValueMap = {}
   for row in tableRows[ 1: ]:
      cells = row.find_all( 'td' )
      year = int( cells[ 0 ].text )
      value = re.sub( "[^0-9-\.]", "", cells[ 1 ].text )

      # Sometimes the cell just contains "$", with no digits. In that case,
      # default to 0.
      value = float( value ) if value else 0

      if multiplyByOneMillion:
         value = value * 1000000
      yearToValueMap[ year ] = value

   return yearToValueMap

def dumpAnnualData( ticker, metric, useCurrencyFormat=False ):
   '''
   Dumps annual data for the given ticker and metric.
   This is helpful for me when I want to quickly copy/paste data
   into a spreadsheet.

   Params:
      ticker - ticker symbol of the comapny.
      metric - financial metric of interest, with dashes separating each word.
      useCurrencyFormat - Use currency format, e.g., "$420,666.69".
   
   Example:
      >>> MacrotrendsUtil.dumpAnnualData( 'GOOG', 'net-income' )
      2005	1465000000.00
      2006	3077000000.00
      2007	4204000000.00
      etc.
   '''
   yearToValueMap = getAnnualData( ticker, metric )
   for year in sorted( yearToValueMap.keys() ):
      value = yearToValueMap[ year ]
      if useCurrencyFormat:
         value = "${:,.2f}".format( value )
         print( "%d\t%s" % ( year, value ) )
      else:
         print( "%d\t%.2f" % ( year, value ) )
   
def getDataFrame( tickers, metrics ):
   '''
   Given a list of tickers and a list of metrics, create a DataFrame
   where each row contains the metrics for a given year and a given ticker.

   Params:
      tickers - list of strings.
      metrics - list of strings.

   Example:
      >>> tickers = [ 'GOOG', 'AMZN' ]
      >>> metrics = [ 'net-income', 'revenue' ]
      >>> MacrotrendsUtil.getDataFrame( tickers, metrics )
      >>> df.head()
         Year Ticker    net-income       revenue
      0  2005   GOOG  1.465000e+09  6.139000e+09
      1  2006   GOOG  3.077000e+09  1.060500e+10
      2  2007   GOOG  4.204000e+09  1.659400e+10
      3  2008   GOOG  4.227000e+09  2.179600e+10
      4  2009   GOOG  6.520000e+09  2.365100e+10
   '''
   tickerToAnnualDataMap = {}

   for ticker in tickers:
      yearToDataMap = {}

      for metric in metrics:
         try:
            yearToValueMap = getAnnualData( ticker, metric )
         except:
            # If we can't get data for a certain metric, just continue
            # and fill in what we can.
            print( "*** Failed to get %s for %s" % ( metric, ticker ) )
            continue
         for year, value in yearToValueMap.items():
            if year not in yearToDataMap:
               yearToDataMap[ year ] = {}
            yearToDataMap[ year ][ metric ] = value
      tickerToAnnualDataMap[ ticker ] = yearToDataMap

   columnNames = [ 'Year', 'Ticker' ] + metrics
   rowList = []

   for ticker in tickers:
      yearToDataMap = tickerToAnnualDataMap[ ticker ]
      for year in sorted( yearToDataMap.keys() ):
         row = [ year, ticker ]
         for metric in metrics:
            value = getattr( yearToDataMap[ year ], metric, 'NaN' )
            row.append( yearToDataMap[ year ][ metric ] )
         rowList.append( row )
   
   df = pd.DataFrame( rowList, columns=columnNames )
   return df



def getFinancialsCsv( ticker, dest='' ):
   print( "Getting Macrotrends financials info for %s" % ticker )
   try:
      df = getDataFrame( [ ticker ], ESSENTIAL_METRICS )
   except Exception as e:
      print( "[ERROR] Could not get Macrotrends financials info for %s" % ticker )
      print( e )
      return 1
   df = df.set_index( 'Year' )
   df = df.drop( [ 'Ticker' ], axis=1 )
   if not dest:
      dest = './%s.csv' % ticker
   df.to_csv( dest )
   return 0


#################
##### MAIN
#################
if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument( '-t', '--tickers', nargs='+', default=[],
                        help="List of ticker symbols separated by spaces." )
   parser.add_argument( '-c', dest='useCurrencyFormat',
                        action='store_true',
                        help="Print the values with dollar signs and commas." )
   args = parser.parse_args()

   for ticker in args.tickers:
      ticker = ticker.upper()
      for metric in ESSENTIAL_METRICS:
         metricWithDashesRemoved = metric.replace( '-', ' ' ).title()
         print( "*** %s Annual %s ***" % ( ticker,
                                          metricWithDashesRemoved ) )
         try:
            dumpAnnualData( ticker, metric,
                            useCurrencyFormat=args.useCurrencyFormat )
            print()            
         except Exception as e:
            print( "[ERROR] Failed to get data for %s %s: %s" % \
               ( ticker,
                 metricWithDashesRemoved,
                 str( e ) ) )
            continue
      print
