# An open-source project by
# Rui Pedro Moreira 2022

# This is just an experiment,
# Please use with caution!

import ccxt
import config
import schedule
import pandas as pd
import numpy as np
from ta.utils import dropna
from ta.momentum import RSIIndicator
from ta.trend import MACD, PSARIndicator
from ta.volatility import AverageTrueRange
from ta.volume import MFIIndicator
from datetime import datetime
from numerize import numerize
import time
import os



pd.set_option('display.max_rows', None)
# text colors and format
buy_long="\033[1;32;49mLONG\033[0;37;49m"
short_sell="\033[1;31;49mSHORT\033[0;37;49m"

arrow_up="\033[0;32;49m▴\033[0;37;49m"
arrow_down="\033[0;31;49m▾\033[0;37;49m"

bold="\033[1;37;49m"
white="\033[0;37;49m"
yellow="\033[0;33;49m"
red="\033[0;31;49m"
green="\033[0;32;49m"


# define pairs, timeframe and how many candles.
symbols=config.symbols
timeframes=config.timeframes
limit=config.limit

# insert your exchange keys on the config.py file.
exchange_to_use='Binance'
if exchange_to_use == 'Binance':
    exchange = ccxt.binance({
        "apiKey": config.BINANCE_API_KEY,
        "secret": config.BINANCE_SECRET_KEY
    })
elif exchange_to_use == 'Bybit':
    exchange = ccxt.bybit({
        "apiKey": config.BYBIT_API_KEY,
        "secret": config.BYBIT_SECRET_KEY
    })


while True:
    c=0
    os.system('clear')
    print(f'{white}fetching data from {len(symbols)} pairs on {exchange_to_use}...')
    # we want to look up multiple symbols...
    for symbol in symbols:
        # ...in multiple timeframes.
        for timeframe in timeframes:
            print(f'processing {symbol} {timeframe} chart     ', end='\r')
            bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            # ignore current candle still in progress
            df = pd.DataFrame(bars, columns=['timestamp','open','high','low','close','volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

            # get technical analysis indicators
            # calculate basic trend
            df['close_prev'] = df['close'].shift(1)
            df['close_delta'] = df['close'] - df['close_prev']
            df['close_delta_perc'] = round(df['close_delta'] / df['close_prev']*100,2)
            price_change=df['close_delta_perc'].iat[-1]
            if price_change >= 0:
                price_change=green+str(price_change)
            else:
                price_change=red+str(price_change)

            #Volume
            volume=df['volume'].iat[-1]
            volume_prev=df['volume'].shift(1).iat[-1]
            volume_delta=volume-volume_prev
            if volume_delta >= 0:
                vol_dir=arrow_up
            else:
                vol_dir=arrow_down
            vol_show=numerize.numerize(volume,3)

            #RSI (Relative Strength Index)
            df['rsi']=RSIIndicator(close=df['close'], window=14, fillna=True).rsi()
            rsi=round(df['rsi'].iat[-1],1)
            rsi_prev=round(df['rsi'].shift(1).iat[-1],1)
            rsi_diff=rsi-rsi_prev
            if rsi_diff <=0:
                rsi_dir=arrow_down
            else:
                rsi_dir=arrow_up
            if rsi_prev <= 30 and rsi > 30:
                if rsi_diff > 0:
                    rsi_buy_signal=True
                    rsi_sell_signal=False
                else:
                    rsi_buy_signal=False
                    rsi_sell_signal=False
            elif rsi_prev >= 60 and rsi < 60:
                if rsi_diff < 0:
                    rsi_sell_signal=True
                    rsi_buy_signal=False
                else:
                    rsi_sell_signal=False
                    rsi_buy_signal=False
            else:
                rsi_sell_signal=False
                rsi_buy_signal=False

            #MACD (Moving Average Convergence Divergence)
            df['macd']=MACD(close=df['close'], window_slow=26, window_fast=12, window_sign=9, fillna=True).macd()
            df['macd_signal']=MACD(close=df['close'], window_slow=26, window_fast=12, window_sign=9, fillna=True).macd_signal()
            df['macd_histogram']=MACD(close=df['close'], window_slow=26, window_fast=12, window_sign=9, fillna=True).macd_diff()
            macd=round(df['macd'].iat[-1],1)
            macd_signal=round(df['macd_signal'].iat[-1],1)
            macd_hist=round(df['macd_histogram'].iat[-1],1)
            macd_hist_prev=round(df['macd_histogram'].shift(1).iat[-1],1)
            if macd_hist < macd_hist_prev:
                macd_dir=arrow_down
                macd_sell_signal=True
                macd_buy_signal=False
            else:
                macd_dir=arrow_up
                macd_sell_signal=False
                macd_buy_signal=True


            #PSAR (Parabolic Stop and Reverse)
            df['psar']=PSARIndicator(high=df['high'], low=df['low'], close=df['close'], step=0.02, max_step=0.2, fillna=True).psar()
            psar=df['psar'].iat[-1]
            psar_prev=df['psar'].shift(1).iat[-1]
            close=df['close'].iat[-1]
            close_prev=df['close'].shift(1).iat[-1]
            psar_delta=round((close-psar)-(close_prev-psar_prev),3)
            if psar_delta>0:
                psar_trend=arrow_up
            else:
                psar_trend=arrow_down
            
            # MFI (Money Flow Indicator)
            df['mfi']=MFIIndicator(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'], window=14, fillna=True).money_flow_index()
            mfi=round(df['mfi'].iat[-1],1)
            mfi_prev=df['mfi'].shift(1).iat[-1]
            mfi_delta=round(mfi-mfi_prev,1)
            if mfi_prev >= 80:
                mfi_sell_signal=True
                mfi_buy_signal=False
            elif mfi_prev <= 20:
                mfi_sell_signal=False
                mfi_buy_signal=True
            if mfi_delta < 0:
                mfi_dir=arrow_down
            else:
                mfi_dir=arrow_up

         

            # calculate buy/sell signals
            if rsi_sell_signal == True and macd_sell_signal == True and mfi_sell_signal == True:
                signal=short_sell
            elif rsi_buy_signal == True and macd_buy_signal == True and mfi_buy_signal == True:
                signal=buy_long
            else:
                signal=False
                signal_color=False

            # print stuff
            if signal != False:
                c=c+1
                print(f'{yellow}<{bold}{symbol[0:-5]}{yellow}@{white}{timeframe}{yellow}>{white} {price_change}%{white} {bold}RSI{white}{rsi_dir}{white}{rsi} {bold}MACD{macd_dir}{white}{macd_hist} {bold}PSAR{psar_trend}{white}{psar_delta} {bold}MACD{macd_dir}{white}{macd_hist} {bold}MFI{mfi_dir}{white}{mfi} {bold}VOL{vol_dir}{white}${vol_show} {signal}{white}')
            #print(df)
    if c > 0:
        print(f'{white}done. found {c} potential trades.')
    else:
        os.system('clear')
        print(f'やれやれだぜ...')
    time.sleep(600)