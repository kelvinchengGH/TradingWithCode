#!/Users/kelvincheng/anaconda2/bin/python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os
import json
import datetime

import yfinance as yf

### Read in data ###
csvBaseDir = '../../data/RawData/DailyPriceCsvs/'
def symbolToCsvPath( symbol, baseDir=csvBaseDir ):
    ''' Return CSV file path for the given ticker symbol. '''
    return os.path.join(baseDir, "{}.csv".format(str(symbol)))


jsonBaseDir = '../../data/RawData/YahooFinanceInfo'
def symbolToJsonPath( symbol, baseDir=jsonBaseDir ):
    return os.path.join(baseDir, "{}.json".format(str(symbol)))
    

def getDailyStockPrices( symbols, dates=None ):
    """
    Read daily price data from the CSV files for each symbol in the list,
    and return a DataFrame with this data.

    Paramters:
       symbols ( list ): List of ticker symbols to gather info on.
       dates ( DateTimeIndex ): A pandas list of dates to read info for.

    Returns:
       DataFrame: A table with the daily prices for each symbol in the list.

    Example:
       startDate = '2000-01-01'
       endDate = datetime.datetime.today().strftime('%Y-%m-%d')
       dates = pd.date_range( startDate, endDate )
       symbols = [ 'AAPL', 'MSFT' ]
       getDailyStockPrices( symbols, dates )
    """    
    # Use the SPY as a reference for which trading days to include.
    dropSpy = False
    if 'SPY' not in symbols:
        dropSpy = True
        symbols.insert( 0, 'SPY' )

    if not dates:
        startDate = '1900-01-01'
        endDate = datetime.datetime.today().strftime('%Y-%m-%d')
        dates = pd.date_range( startDate, endDate )

    df = pd.DataFrame( index=dates )
        
    for symbol in symbols:
        path = symbolToCsvPath( symbol )
        df_temp = pd.read_csv( path, index_col='Date', parse_dates=True,
                               usecols=[ 'Date', 'Close' ], na_values=[ 'nan' ] )
        df_temp = df_temp.rename( columns={ 'Close' : symbol } )
        df = df.join( df_temp )
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna( subset=["SPY"] )

    if dropSpy:
        symbols.remove( 'SPY' )
        df = df.drop( [ 'SPY' ], axis=1 )
    return df


def getYahooFinanceInfoDict( symbol ):
    with open( symbolToJsonPath( symbol ), 'r' ) as f:
        infoDict = json.load( f )
    return infoDict

### Plot data ### 
def plotData( df, title='Stock Prices', xlabel='Date', ylabel='Price' ):
    ''' Plot stock prices with a custom title and meaningful axis labels. '''
    ax = df.plot( title=title, fontsize=12 )
    ax.set_xlabel( xlabel )
    ax.set_ylabel( ylabel )
    ax.grid()
    plt.show()
    
def plotHist( df ):
    ''' 
    Plot overlapping historgrams.
    This is useful for looking at the distribution of daily returns.
    '''
    for symbol in df.columns:
        df[ symbol ].hist( bins=20, label=symbol, alpha=0.4 )
    plt.legend( loc='upper right' )
    plt.show()


### Compute statistics on a DataFrame where each column is a stock's daily price ###x
def dailyReturns( df ):
    ''' Compute and return the daily return values '''
    returns = df.copy()
    returns[1:] = ( df[1:] / df[:-1].values ) - 1
    returns.ix[0,:] = 0
    return returns

def normalizeData( df ):
    return df / df.iloc[ 0 ]


def movingAverage( df, window ):
    ''' 
    df is a table of daily stock prices.
    Returns a table of "window"-day moving averages for each stock in df.
    '''
    averages = df[ [] ]
    for symbol in df.columns:
        dfTemp = df[ symbol ]
        dfMa = dfTemp.rolling( window ).mean()
        averages = averages.join( dfMa )
    return averages


def stockWithMovingAverages( df, symbol, windows=[ 20, 50, 200 ] ):
    ''' 
    From a DataFrame with daily price data for one or more stocks,
    choose one of the stocks and compute one or more moving averages.
    '''
    result = df[ [symbol ] ]
    for window in windows:
        df1 = df[ [ symbol ] ]        
        ma = movingAverage( df1, window )
        ma = ma.rename( columns={ symbol : '%d-day MA' % window } )
        result = result.join( ma )
    return result




##### One-off stats #####
def pctChangeFromAllTimeHigh( symbol ):
    '''
    Takes the last closing price and calculates the percentage
    difference from the all-time high.
    '''
    df = getDailyStockPrices( [ symbol ] )
    priceSeries = df[ symbol ]
    lastClosingPrice = priceSeries[-1]
    allTimeHigh = priceSeries.max()
    pctChange = ( lastClosingPrice - allTimeHigh ) / allTimeHigh
    return pctChange


def dividendYield( symbol ):
    infoDict = getYahooFinanceInfoDict( symbol )
    return infoDict.dividendYield


def forwardPE( symbol ):
    infoDict = getYahooFinanceInfoDict( symbol )
    return infoDict.forwardPE


def showPctChangeFromAllTimeHigh( symbols ):
    for symbol in symbols:
        pass
