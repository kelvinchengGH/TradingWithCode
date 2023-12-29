# Utilities to collect raw data from the Internet and save them into files.


##################
# IMPORTS
##################
import yfinance as yf
import pandas as pd
import datetime
import os, subprocess
import json

from UtilLib import Util



##################
# FUNCTIONS
##################

def getDailyPriceCsv( ticker: str, dest: str = '' ) -> int:
   '''
   Get daily price info for a stock in csv format.
   
   Keyword arguments:
      ticker -- The ticker symbol
      dest   -- Path to the directory where we want the CSV file
   '''

   # Fetch Yahoo Finance data into a Python DataFrame 
   try:
      print( "Getting daily price data for %s" % ticker )
      df = yf.Ticker( ticker ).history( period='max' )
   except Exception as e:
      print( "[ERROR] Could not get daily price data for %s" % ticker )
      print( e )
      return 1

   df = df.round( 2 )
   # Write the DataFrame into a CSV
   if not dest:
      dest = './%s.csv' % ticker
   df.to_csv( dest )
   return 0


def getDailyPriceCsvFast( ticker: str, dest: str = '' ) -> int:
   if not dest:
      dest = './%s.csv' % ticker

   # Check if the CSV already exists and holds valid data..
   try:
      existingDf = pd.read_csv( dest )
      lastDateInExistingCsv = existingDf.iloc[ -1 ][ 'Date' ]
   except Exception as e:
      # A valid CSV does not already exist,
      # so download the whole CSV.
      getDailyPriceCsv( ticker, dest )
      return 0

   if Util.isMostRecentWeekday( lastDateInExistingCsv ):
      print( "Daily price data for %s is already up-to-date" % ticker )
      return 0

   # Fetch Yahoo Finance data into a Python DataFrame, starting
   # from the date after the last date in our existing CSV.
   startDate = Util.shiftDateStr( lastDateInExistingCsv, 1 )
   try:
      print( "Updating daily price data for %s" % ticker )
      df = yf.Ticker( ticker ).history( start=startDate )
   except Exception as e:
      print( "[ERROR] Could not get daily price data for %s" % ticker )
      print( e )
      return 1

   # Write the df we got from yfinance to a CSV and read it back.
   # This helps us cleanly concatenate it to exsitingDf.
   df = df.round( 2 )
   tempFilename = '%s-tmp.csv' % ticker
   df.to_csv( tempFilename )
   df1 = pd.read_csv( tempFilename )

   # Concatenate the existing data with the latest data,
   # and write it to a CSV.
   finalDf = pd.concat( [ existingDf, df1 ] )
   finalDf.set_index( 'Date', inplace=True )
   finalDf.to_csv( dest )

   # Clean up temporary file.
   os.system( 'rm %s' % tempFilename )
   return 0


def getYahooFinanceInfoDict( ticker: str, dest: str = '' ) -> int:
   '''
   Fetch dictionary of info and metrics for the given ticker,
   and save it in a JSON.
      This info includes things like forwardPE and dividendYield.
   '''
   try:
      print( "Getting Yahoo! Finance info dict for %s" % ticker )
      infoDict = yf.Ticker( ticker ).info
   except Exception as e:
      print( "[ERROR] Could not get info for %s" % ticker )
      print( e )
      return 1

   if not dest:
      dest = './%s.json' % ticker

   with open( dest, 'w' ) as f:
      f.write( json.dumps( infoDict, indent=4, sort_keys=True ) )
   return 0


def getYahooFinanceFastInfo( ticker: str, dest: str = '' ) -> int:
   '''
   Fetch dictionary of fast_info and metrics for the given ticker,
   and save it in a JSON.
      This info includes things like shares outstanding and market cap.
   '''
   try:
      print( "Getting Yahoo! Finance fast_info dict for %s" % ticker )
      infoDict = dict( yf.Ticker( ticker ).fast_info )
   except Exception as e:
      print( "[ERROR] Could not get info for %s" % ticker )
      print( e )
      return 1

   if not dest:
      dest = './%s.json' % ticker

   with open( dest, 'w' ) as f:
      f.write( json.dumps( infoDict, indent=4, sort_keys=True ) )
   return 0


def getDividendsCsv( ticker: str, dest: str = '' ) -> int:
   if not dest:
      dest = './%s.csv' % ticker

   try:
      print( "Getting Dividend history for %s" % ticker )
      dividends = yf.Ticker( ticker ).dividends
      dividends.to_csv( dest )
   except Exception as e:
      print( "[ERROR] Could not get info for %s. Writing empty CSV." % ticker )
      print( e )
      with open( dest, 'w' ) as f:
         f.write( "Date,Dividends\n" )
      return 1

   return 0


def getQuarterlyFinancialCsv( stock: str, destDir: str ) -> None:
   ''' Get quarterly financial info for a stock into a csv file '''

   # Work in-progress
   
   csvFile = '%s_quarterly_financial_data.csv' % stock
   url = 'http://www.stockpup.com/data/%s' % csvFile
   try:
      print( "Getting quarterly financial data for %s" % stock )
      subprocess.check_output( ['wget', '-N', '-q', '-P', 'csvs', url ] )
   except:
      print( "[ERROR] Could not get quarterly financial data for %s" % stock )
