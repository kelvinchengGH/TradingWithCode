#!/usr/bin/env python3

import os



# Base directory of the repository
BASE_DIR = os.path.realpath( os.path.join( os.path.dirname( __file__ ), '..' ) )


def absolutePathLocator( relativePath: str ) -> str:
    return os.path.normpath(os.path.join(BASE_DIR, relativePath)) 


def formatDollarValue( value: float ) -> str:
    '''
    Returns a string representing the market cap.

    Some illustrative examples:
        marketCap    marketCapFormatted
    -----------------------------------
    1,234,567,890    1.23T
           69,420    69.4K
      123,456,789    123M
    '''
    # TODO: - Figure out how to sort strings of this form so that
    #            1.12T > 43.20B > 270.34K > 999.69

    # For values less than 1000, we don't need a suffix.
    if value < 1000:
        return "%.2f" % value

    orderOfMagnitudeToSuffixMap = {
        1e3  : "K",
        1e6  : "M",
        1e9  : "B",
        1e12 : "T",
        1e15 : "Qa",
        1e18 : "Qi",
    }

    orders = sorted( orderOfMagnitudeToSuffixMap.keys() )
    orderOfMagnitude = next( order for order in orders \
                             if value / 1e3 < order )
    suffix = orderOfMagnitudeToSuffixMap[ orderOfMagnitude ]
    scaledValue = value / orderOfMagnitude
    # Keep just 3 significant figures
    if scaledValue >= 100:
        return "%d%s" % ( scaledValue, suffix )
    elif scaledValue >= 10:
        return "%.1f%s" % ( scaledValue, suffix )
    return "%.2f%s" % ( scaledValue, suffix )
