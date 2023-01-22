#!/usr/bin/env python

import os, subprocess
from bs4 import BeautifulSoup

############
# Constants
############
ROOT_DIR = os.path.realpath( os.path.join( os.path.dirname( __file__ ), '../..' ) )

def getHtmlSoup( url ):
    cmd = [ "curl", "-s", url ]
    output = subprocess.check_output( cmd )
    return BeautifulSoup( output, 'html.parser' )


def getDividendAristocratList():
    '''
    Return a list of tickers for the S&P 500 Dividend Aristocrats.
    '''
    result = []
    url = "https://en.wikipedia.org/wiki/S%26P_500_Dividend_Aristocrats"
    soup = getHtmlSoup( url )
    table = soup.find( 'table' )
    rows = table.find_all( 'tr' )
    for row in rows[ 1: ]: # Skip the header
        ticker = row.find_all( 'td' )[ 1 ].text
        result.append( ticker )
    return sorted( result )


def getSp500List():
    '''
    Return a list of tickers for the stocks in the S&P 500.
    '''
    result = []
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    soup = getHtmlSoup( url )
    table = soup.find( 'table' )
    rows = table.find_all( 'tr' )
    for row in rows[ 1: ]: # Skip the header
        ticker = row.find_all( 'td' )[ 0 ].text.strip()
        result.append( ticker )
    return sorted( result )


def getNasdaq100List():
    '''
    Return a list of tickers for the stocks in the Nasdaq 100.
    '''
    result = []
    url = "https://en.wikipedia.org/wiki/Nasdaq-100"
    soup = getHtmlSoup( url )
    table = soup.find_all( 'table' )[4]
    rows = table.find_all( 'tr' )
    for row in rows[ 1: ]: # Skip the header
        ticker = row.find_all( 'td' )[ 1 ].text
        result.append( ticker )
    return sorted( result )


def getDowJonesList():
    '''
    Return a list of tickers for the stocks in the 
    Dow Jones Industrial Average.
    '''
    result = []
    url = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
    soup = getHtmlSoup( url )
    table = soup.find_all( 'table' )[1]
    rows = table.find_all( 'tr' )
    for row in rows[ 1: ]: # Skip the header
        ticker = row.find_all( 'td' )[ 1 ].text.strip()
        result.append( ticker )
    return sorted( result )



###########
# main()
###########
def testFunc( func ):
    tickers = func()
    print( "*** %s() output ***" % func.__name__ )
    print( ", ".join( tickers ) )
    print()


def main():
    funcs = [
        getDividendAristocratList,
        getSp500List,
        getNasdaq100List,
        getDowJonesList,
    ]
    for func in funcs:
        testFunc( func )

    

if __name__ == '__main__':
    main()
    
    
