#TVOC - TradingView On Console
#Rui Pedro Moreira - 2022
from tradingview_ta import *
import os

os.system('clear')

interval=Interval.INTERVAL_4_HOURS
symbols=['BINANCE:BTCUSDT','BINANCE:ETHUSDT','BINANCE:BNBUSDT','BINANCE:ADAUSDT','BINANCE:SOLUSDT','BINANCE:DOGEUSDT','BINANCE:DOTUSDT','BINANCE:SHIBUSDT','BINANCE:AVAXUSDT','BINANCE:MATICUSDT','BINANCE:ETCUSDT','BINANCE:LTCUSDT','BINANCE:HNTUSDT','BINANCE:KDAUSDT']

for symbol in symbols:
	exchange=symbol.split(':')[0]
	handle=symbol.split(':')[1]
	output = TA_Handler(
		symbol=handle,
	    screener="crypto",
	    exchange=exchange,
	    interval=interval
	)

	price_delta=output.get_analysis().indicators["close"] - output.get_analysis().indicators["open"]
	price_delta_perc=round(float(price_delta)/float(output.get_analysis().indicators["open"])*100,2)


	print(f'- {handle} {output.get_analysis().indicators["close"]} ({price_delta_perc}%) Open {output.get_analysis().indicators["open"]} High {output.get_analysis().indicators["high"]} Low {output.get_analysis().indicators["low"]} {exchange} {output.get_analysis().summary["RECOMMENDATION"]}')

print(f'...')