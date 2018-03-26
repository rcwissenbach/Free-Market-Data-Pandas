import pandas as pd
import os
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import numpy as np
import re
import tiingo as tg
import quandl as qt

#setting up Tiingo
from tiingo import TiingoClient
config = {}
config['session'] = True
config['api_key'] = "API_KEY_HERE"
client = TiingoClient(config)

'''Example shell for getting GOOGL prices
historical_prices = client.get_ticker_price("GOOGL",
                                            fmt='json',
                                            startDate='2017-08-01',
                                            endDate='2017-08-31',
                                            frequency='daily')
'''
#futures for quandl
crude = 'ICE_T1'
spy = 'CME_SP1'
cc = 'ICE_CC1'
vix = 'CBOE_VX1' #2010 for normalized prices
five = 'CME_FV1'
gas = 'CME_NG1'

#Tiingo for Equities
def equities(x):
    df = pd.DataFrame(client.get_ticker_price("%s" %(x), fmt='json',
                                              startDate='2017-01-01',
                                              endDate=pd.to_datetime('today').normalize(),
                                              frequency='daily'))
#Removing letters from date/time field
    df['date'] = df['date'].str.split('T').str[0]
    df = df.set_index(pd.DatetimeIndex(df['date']))
    df = df[['open', 'high', 'low', 'close', 'volume']]
    range = (df['high'] - df['low'])
    df.insert(5, 'range', range)
    relclose = ((df['high'] - df['close']) / df['range'])
    df.insert(6, 'rclose', relclose)
    pchange = (df['close'].pct_change() * 100)
    df.insert(7, 'pchange', pchange)
    #df = df[['Open','High', 'Low', 'Settle','Range', 'RClose', 'PChange', 'Volume']]
    #df.insert(7, 'Consec', 0.0)
    #df.insert(8, 'ConsecD', 0.0)
    df = df.replace(['inf', '-inf'], 0)
    #df.reindex(index=df.index[::-1])
    return df

def futures(x):
    df = qt.get("CHRIS/%s" %(x), authtoken="API_KEY_QUANDL")
    df.columns = map(str.lower, df.columns)
    range = (df['high'] - df['low'])
    df.insert(4, 'range', range)
    relclose = ((df['high'] - df['settle']) / df['range'])
    df.insert(5, 'rclose', relclose)
    pchange = (df['settle'].pct_change() * 100)
    df.insert(6, 'pchange', pchange)
    df = df[['open','high', 'low', 'settle','range', 'rclose', 'pchange']]
    #df.insert(7, 'Consec', 0.0)
    #df.insert(8, 'ConsecD', 0.0)
    df = df.replace(['inf', '-inf'], 0)
    #df.reindex(index=df.index[::-1])
    return df

# coming someday from pandas data reader pdr.get_data_quandl()

