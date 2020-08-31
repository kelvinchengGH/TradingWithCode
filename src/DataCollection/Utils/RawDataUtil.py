#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
#
# Utilities to collect raw data from the Internet
#
#
#
#

import pandas_datareader as web
import datetime
import subprocess

def getTickerList( tickerListPath ):
   ''' Read list of ticker symbols from text file.

   Keyword arguments:
   stockListPath -- Path to the list of tickers
   '''
   with open( tickerListPath, 'r' ) as f:
      tickers = f.readlines()
   tickers = [ t.strip() for t in tickers ]
   return tickers
   

def getDailyPriceCsv( ticker, dest='' ):
   ''' Get daily price info for a stock in csv format.
   
   Keyword arguments:
   ticker -- The ticker symbol
   dest   -- Path to the created CSV file
   '''

   start = datetime.datetime( 1900, 1, 1 )
   end = datetime.datetime.today()

   # Fetch Yahoo Finance data into a Python DataFrame 
   try:
      print( "Getting daily price data for %s" % ticker )
      df = web.DataReader( ticker, 'yahoo', start, end )
   except Exception as e:
      print( "[ERROR] Could not get daily price data for %s" % ticker )
      print( e )
      return 1

   # Write the DataFrame into a CSV
   if not dest:
      dest = '/%s.csv' % ticker
   df.to_csv( dest )
   return 0

def getQuarterlyFinancialCsv( stock, destDir ):
   ''' Get quarterly financial info for a stock into a csv file '''

   # Work in-progress
   
   csvFile = '%s_quarterly_financial_data.csv' % stock
   url = 'http://www.stockpup.com/data/%s' % csvFile
   try:
      print( "Getting quarterly financial data for %s" % stock )
      subprocess.check_output( ['wget', '-N', '-q', '-P', 'csvs', url ] )
   except:
      print( "[ERROR] Could not get quarterly financial data for %s" % stock )
