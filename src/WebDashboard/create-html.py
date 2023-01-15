#!/usr/bin/env python

"""
Take the template HTML file, and add in the missing stuff.
"""

###########
# Imports
###########
import Screener


# Fetch the table of stock data, and convert it to an HTML table.
screener = Screener.Screener()
df = screener.df
tableText = df.to_html()
tableLines = tableText.split( '\n' )


# Now we edit some of the lines in the HTML.

# Set table id.
tableLines[ 0 ] = tableLines[ 0 ][:-1] + ' id="StockDataFrame">'

# Set name of the first column.
tableLines[ 3 ] = tableLines[ 3 ][:-5] + 'Ticker' + tableLines[ 3 ][-5:]


# Set onclick for the Ticker column, which is the index column of the DataFrame.
origLine = tableLines[ 3 ]
newLine = origLine[:9] + ' onclick="sortTable(0, false)"' + origLine[9:]
tableLines[ 3 ]  = newLine


# Set onclick for each of the other columns.
#    Keep in mind that the DataFrame's Ticker column is the index,
#    which doesn't appear in df.columns.
for dfColNum in range( len( df.columns ) ):
    lineNum = 4 + dfColNum
    htmlTableColNum = dfColNum + 1
    origLine = tableLines[ lineNum ]
    dfElement = df.iloc[ 0, dfColNum ]
    colIsNumerical = isinstance( dfElement, int ) or isinstance( dfElement, float )
    colIsNumerical = str( colIsNumerical ).lower()
    newLine = origLine[:9] + ' onclick="sortTable(%d, %s)"' % ( htmlTableColNum, colIsNumerical ) + origLine[9:]
    tableLines[ lineNum ] = newLine

# Form the finished HTML code for the table.
finishedTableText = '\n'.join( tableLines )


# Open the template HTML file, and substitute the table where the PLACEHOLDER comment is.
with open( 'template.html', 'r' ) as f:
    origHtmlText = f.read()

newHtmlText = origHtmlText.replace( '<!--PLACEHOLDER: StockDataFrame table -->', finishedTableText )

with open( 'index.html', 'w' ) as f:
    f.write( newHtmlText )

