import os, subprocess
from bs4 import BeautifulSoup


def getDividendAristocratList():
    result = []
    url = "https://en.wikipedia.org/wiki/S%26P_500_Dividend_Aristocrats"
    cmd = [ "curl", "-s", url ]
    output = subprocess.check_output( cmd )
    soup = BeautifulSoup( output, 'html.parser' )
    table = soup.find( 'table' )
    rows = table.find_all( 'tr' )
    for row in rows[ 1: ]: # Skip the header
        ticker = row.find_all( 'td' )[ 1 ].text
        result.append( ticker )
    return result


def getSp500List():
    result = []
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    cmd = [ "curl", "-s", url ]
    output = subprocess.check_output( cmd )
    soup = BeautifulSoup( output, 'html.parser' )
    table = soup.find( 'table' )
    rows = table.find_all( 'tr' )
    for row in rows[ 1: ]: # Skip the header
        ticker = row.find_all( 'td' )[ 0 ].text.strip()
        result.append( ticker )
    return result


def getNasdaq100List():
    result = []
    url = "https://en.wikipedia.org/wiki/Nasdaq-100"
    cmd = [ "curl", "-s", url ]
    output = subprocess.check_output( cmd )
    soup = BeautifulSoup( output, 'html.parser' )
    table = soup.find_all( 'table' )[4]
    rows = table.find_all( 'tr' )
    for row in rows[ 1: ]: # Skip the header
        ticker = row.find_all( 'td' )[ 1 ].text
        result.append( ticker )
    return result


def getDowJonesList():
    result = []
    url = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
    cmd = [ "curl", "-s", url ]
    output = subprocess.check_output( cmd )
    soup = BeautifulSoup( output, 'html.parser' )
    table = soup.find_all( 'table' )[1]
    rows = table.find_all( 'tr' )
    for row in rows[ 1: ]: # Skip the header
        ticker = row.find_all( 'td' )[ 1 ].text.strip()
        result.append( ticker )
    return result

