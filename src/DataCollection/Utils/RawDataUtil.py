#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
#
# Utilities to collect raw data from the Internet


##################
# IMPORTS
##################
import yfinance as yf
import pandas as pd
import datetime
import os, subprocess
import json


##################
# HELPER FUNCTIONS
##################

def shiftDateStr( dateStr, nDays ):
   '''
   Shift the date by nDays.
   return the date string for the following day.

   Keyword arguments:
      dateStr -- Date string the form 'YYYY-MM-DD'
      nDays   -- Integer-valued shift.
   '''
   return ( datetime.datetime.strptime( dateStr, '%Y-%m-%d' ) + \
            datetime.timedelta( days=nDays ) ).strftime('%Y-%m-%d')


def isMostRecentWeekday( dateStr ):
   '''
   Returns whether the dateStr is equal to the most recent weekday.

   TODO: Handle holidays?

   Keyword arguments:
      dateStr -- Date string the form 'YYYY-MM-DD'
   '''
   today = datetime.datetime.today()
   todayStr = today.strftime( '%Y-%m-%d' )
   return dateStr == todayStr \
      or today.weekday() == 5 and dateStr == shiftDateStr( todayStr, -1 ) \
      or today.weekday() == 6 and dateStr == shiftDateStr( todayStr, -2 )


##################
# FUNCTIONS
##################

def getTickerList( tickerListPath ):
   '''
   Read list of ticker symbols from text file.

   Keyword arguments:
      stockListPath -- Path to the list of tickers
   '''
   with open( tickerListPath, 'r' ) as f:
      tickers = f.readlines()
   tickers = [ t.strip() for t in tickers ]
   return tickers
   

def getDailyPriceCsv( ticker, dest='' ):
   '''
   Get daily price info for a stock in csv format.
   
   Keyword arguments:
      ticker -- The ticker symbol
      dest   -- Path to the created CSV file
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


def getDailyPriceCsvFast( ticker, dest='' ):
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
      return

   if isMostRecentWeekday( lastDateInExistingCsv ):
      print( "Daily price data for %s is already up-to-date" % ticker )
      return

   # Fetch Yahoo Finance data into a Python DataFrame, starting
   # from the date after the last date in our existing CSV.
   startDate = shiftDateStr( lastDateInExistingCsv, 1 )
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
   return


def getYahooFinanceInfoDict( ticker, dest='' ):
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
