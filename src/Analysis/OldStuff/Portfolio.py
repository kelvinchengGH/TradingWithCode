# import os, math, datetime

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# import Stats


# #################
# # Portfolio
# #################
# class Portfolio:
#     def __init__(
#             self,
#             startVal: int,
#             startDate: datetime.datetime|str,
#             endDate: datetime.datetime|str,
#             symbols: list[str],
#             allocs: list[float]
#     ) -> None:

#         # Some checks for legitimate arguments
#         if len( symbols ) != len( allocs ):
#             raise ValueError( 'symbols and allocs must match in length' )
#         if sum( allocs ) - 1 > 0.0001:
#             raise ValueError( 'allocs must sum to 1' )
#         if startDate > endDate:
#             raise ValueError( 'endDate must come after startDate' )
#         if startVal < 0:
#             raise ValueError( 'startVal must be nonnegative' )
        
#         self.startVal = startVal
#         self.startDate = startDate
#         self.endDate = endDate
#         self.symbols = symbols
#         self.allocs = allocs

#     def sharesPerStock( self ):
#         ''' Return a numpy array  showing how many shares of each asset are in the portfolio. '''

#         # For each asset, take the amount of money invested on startDate,
#         # and divide by the price on startDate.
#         dates = pd.date_range( self.startDate, self.startDate )
#         df = Stats.getDailyStockPrices( self.symbols, dates )
#         allocs = np.array( self.allocs )
#         return allocs * self.startVal / df.values

#     def dailyValuePerStock( self ):
#         ''' Return a DataFrame showing the daily fluctuations in each asset. '''
#         dates = pd.date_range( self.startDate, self.endDate )
#         df = Stats.getDailyStockPrices( self.symbols, dates )
#         df = Stats.normalizeData( df )

#         df = df * self.allocs
#         portfolio = df * self.startVal

#         return portfolio

#     def totalDailyValue( self ):
#         ''' Return a DataFrame containing the total daily value of the portfolio. '''
#         return self.dailyValuePerStock().sum( axis=1 ).to_frame()


# #################
# # Useful Stats
# #################
# def sharpeRatioVsBenchmark( portfolio, benchmark ):
#     """
#     Compute the historical Sharpe ratio of a portfolio, compared to a benchmark.
#     S = avg( R - R_b ) / std( R - R_b )

#     Paramters:
#     portfolio ( Portfolio ): A stock portfolio to analyze.
#     benchmark ( str ): The symbol of a benchmark, e.g., "SPY"

#     Returns:
#     float: Sharpe ratio of the portfolio, compared to the benchmark.
#     """
#     dailyPortfolioValue = portfolio.totalDailyValue()
#     dates = pd.date_range( portfolio.startDate, portfolio.endDate )
    
#     dailyBenchmarkValue = Stats.getDailyStockPrices( [ benchmark ], dates )
    
#     dr = Stats.dailyReturns( dailyPortfolioValue )
#     drb = Stats.dailyReturns( dailyBenchmarkValue )

#     diff = dr.values - drb.values
#     return math.sqrt( 252 ) *  diff.mean() / diff.std()


# def sharpeRatioVsRiskFreeRate( portfolio, annualRiskFreeRate ):
#     """
#     Compute the historical Sharpe ratio of a portfolio, 
#     compared to the risk-free rate of return.
#     S = avg( R - R_f ) / std( R )

#     Paramters:
#     portfolio ( Portfolio ): A stock portfolio to analyze.
#     annualRiskFreeRate ( float ): The annual risk-free rate of return.

#     Returns:
#     float: Sharpe ratio of the portfolio.
#     """
#     dailyPortfolioValue = portfolio.totalDailyValue()

#     dr = Stats.dailyReturns( dailyPortfolioValue )
#     dailyRiskFreeRate = annualRiskFreeRate / 365
#     s = math.sqrt( 252 ) * ( dr.mean() - dailyRiskFreeRate ) / dr.std()
#     return float( s )
