#TVOC - TradingView On Console
#Rui Pedro Moreira - 2022
from tradingview_ta import *
import os, time

white="\033[0;37;40m"
bold="\033[1;37;40m"

interval=Interval.INTERVAL_4_HOURS
symbols=[
	'BINANCE:BTCUSDT',
	'BINANCE:ETHUSDT',
	'BINANCE:BNBUSDT',
	'BINANCE:XRPUSDT',
	'BINANCE:ADAUSDT',
	'BINANCE:SOLUSDT',
	'BINANCE:DOGEUSDT',
	'BINANCE:DOTUSDT',
	'BINANCE:SHIBUSDT',
	'BINANCE:AVAXUSDT',
	'BINANCE:MATICUSDT',
	'BINANCE:UNIUSDT',
	'BINANCE:ETCUSDT',
	'BINANCE:LTCUSDT',
	'BINANCE:FTTUSDT',
	'BINANCE:NEARUSDT',
	'BINANCE:LINKUSDT',
	'BYBIT:CROUSDT',
	'BINANCE:ATOMUSDT',
	'BINANCE:XLMUSDT',
	'BINANCE:XMRUSDT',
	'BINANCE:FLOWUSDT',
	'BINANCE:BCHUSDT',
	'BINANCE:ALGOUSDT',
	'BINANCE:FILUSDT',
	'BINANCE:VETUSDT',
	'BINANCE:EOSUSDT',
	'BINANCE:HNTUSDT',
	'BINANCE:KDAUSDT'
	]

while True:
	os.system('clear')
	output=""
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
		if price_delta > 0:
			price_text_color=32
		else:
			price_text_color=31
		if output.get_analysis().summary["RECOMMENDATION"]=="BUY" or output.get_analysis().summary["RECOMMENDATION"]=="STRONG_BUY":
			rec_color=32
		elif output.get_analysis().summary["RECOMMENDATION"]=="SELL" or output.get_analysis().summary["RECOMMENDATION"]=="STRONG_SELL":
			rec_color=31
		else:
			rec_color=37

		print(f'\033[0;33;40m>{bold}{handle[0:-4]}\033[0;33;40m@{bold}{exchange} \033[1;{price_text_color};40m${output.get_analysis().indicators["close"]} {price_delta_perc}% {bold}O{white}${output.get_analysis().indicators["open"]} {bold}H{white}${output.get_analysis().indicators["high"]} {bold}L{white}${output.get_analysis().indicators["low"]} \033[1;{rec_color};40m{output.get_analysis().summary["RECOMMENDATION"]}\033[0;37;40m')

	print(f'ok...')
	time.sleep(300)