# @Author: Yehya Albakri

# External package imports:
import pandas as pd
import os, glob
import time
from datetime import datetime, timedelta, date
import datetime
from pytz import timezone
import pytz
import requests
import json
# from pushbullet import Pushbullet
from configparser import ConfigParser
# from telegram import ReplyKeyboardMarkup
# from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
# 						  ConversationHandler)


# Internal package imports:
import dividend_sort
# import scrape_dividends_future
import td_access_generator
import td_order
import td_refresh
import telegram


# def dividend_csv_maintenance():
# 	file = os.stat('all_entries_filtered.csv')
# 	st = file.st_mtime
# 	datetime_object = datetime.date.fromtimestamp(st)
# 	age = str(date.today() - datetime_object)
# 	age = age.split('day')[0][:-1]
# 	# print(age)
# 	if age[0] == '0':
# 		age = 0
# 	# print(age)
# 	if int(age) > 3:
# 		scrape_dividends_future.get_all_dividends().to_csv('all_entries_filtered_temp.csv', index=False)
		
# 		df1 = pd.read_csv('all_entries_filtered.csv')
# 		df2 = pd.read_csv('all_entries_filtered_temp.csv')

# 		full_df = pd.concat([df1, df2])
# 		full_df = full_df.drop_duplicates(subset=['Ticker'])
# 		full_df.to_csv("all_entries_filtered.csv",index=False)

def get_token():
	file = os.stat('temp_data_refresh.json')
	st = file.st_mtime
	datetime_object = datetime.date.fromtimestamp(st)
	age = str(date.today() - datetime_object)
	age = age.split('day')[0][:-1]
	if age[0] == '0':
		age = 0
	# print('age', age)
	while True:
		if int(age) > 85:
			td_access_generator.generate_tokens()
		else:
			token = td_refresh.get_token_from_refresh()
			# print(token)
			return token

def get_tickers(top_n):
	daily_tickers = dividend_sort.highest_paying_tickers(top_n)
	ticker_list = []
	for item in daily_tickers['ticker']:
		ticker_list.append(item)
	print(ticker_list)
	return ticker_list

def order(headers, ticker, amount, instruction, if_quantity, quantity_type):
	# if_quantity will only be used if the inputted value is greater than 0
	# quantity_type has been disabled/deleted from the "td_order" file

	last_buy = []
	stock = td_order.get_quote(ticker)
	stock_price = stock[ticker]['lastPrice']
	quantity = int(amount / stock_price)
	if if_quantity > 0:
		quantity = if_quantity

	if quantity > 0:
		td_order.place_order(headers, ticker, quantity, instruction, quantity_type)

def is_weekend():
	if date.today().weekday() == 5 or date.today().weekday() == 6:
		# print('true')
		return True
	else:
		# print('false')
		return False

def main_function(amount, top_n_tickers):
	# headers = get_token()
	# account = td_order.account_info(headers)
	# portfolio_value = account['securitiesAccount']['currentBalances']['equity']
	# temp_blacklist_telegram = None
	amount_per_ticker = amount / top_n_tickers
	# day_move = account['securitiesAccount']['positions'][0]['currentDayProfitLoss']
	# day_move_percentage = account['securitiesAccount']['positions'][0]['currentDayProfitLossPercentage']
	try:
		while True:
			if is_weekend() == False:
				current_time = datetime.datetime.now().strftime("%H:%M")
				print(current_time) 

				telegram.reply_message_telegram_2('test', 'Test recieved, program is working.')

				# the following chunk is an emergency stop algorithm
				if telegram.reply_message_telegram_1('stop', 'Emergency stop activated, program stopped.') == 'stop':
					print('emergency stop')
					main_function_remote_start(amount, top_n_tickers)
					return

				if str(current_time) == '19:55':
					headers = get_token()
					tickers = get_tickers(top_n_tickers)
					for ticker in tickers:
						order(headers, ticker, amount_per_ticker, 'Buy', 0, 'SHARES')

					account = td_order.account_info(headers)
					portfolio_value = account['securitiesAccount']['currentBalances']['equity']
					payload = str(tickers) + ' - ' + 'current portfolio value: ' + str(portfolio_value)
					telegram.send_message_telegram('Purchased Shares: ' + payload)
					# send_notification('Purchased Shares', payload)

				if str(current_time) == '18:00':
					headers = get_token()
					account = td_order.account_info(headers)
					available = []
					for item in account['securitiesAccount']['positions']:
						if item['instrument']['assetType'] == 'EQUITY':
							available.append((item['instrument']['symbol'], int(item['longQuantity'])))

					print('account', account['securitiesAccount']['positions'])
					for ticker in available:
						order(headers, ticker[0], 0, 'Sell', ticker[1], 'SHARES')
					
					account = td_order.account_info(headers)
					portfolio_value = account['securitiesAccount']['currentBalances']['equity']
					payload = str(available) + ' - ' + 'current portfolio value: ' + str(portfolio_value)
					telegram.send_message_telegram('Sold Shares: ' + payload)
					# send_notification('Sold Shares', payload)

				# dividend_csv_maintenance()

				portfolio_tracking()

				time.sleep(60)
			else:
				current_time = datetime.datetime.now().strftime("%H:%M")
				print('is weekend ', current_time)

				telegram.reply_message_telegram_2('test', 'Test recieved, program is working.')

				# the following chunk is an emergency stop algorithm
				if telegram.reply_message_telegram_1('stop', 'Emergency stop activated, program stopped.') == 'stop':
					print('emergency stop')
					main_function_remote_start(amount, top_n_tickers)
					return

				time.sleep(60)
	except Exception as e:
		print(e)
		with open('last_crash_error.json', 'w') as outfile:
			json.dump(e, outfile)
		telegram.send_message_telegram('Error occured, program stopped.')
		return 'Error occured, program stopped.'
	
def main_function_remote_start(amount, top_n_tickers):
	while True:
		if telegram.reply_message_telegram_3('start', 'Remote start activated, program started.') == 'start':
			print('remote start')
			main_function(amount, top_n_tickers)
		time.sleep(10)

def portfolio_tracking():
	portfolio_data = {'datetime': [],
					  'portfolio_value': [],
					  'ticker': [],
					  'quantity': [],
					  'market_value': [],
					  'current_day_loss_profit': []}
	portfolio_data_df = pd.DataFrame(portfolio_data, columns = ['datetime', 
																'portfolio_value',
																'ticker',
																'quantity',
																'market_value',
																'current_day_loss_profit'])

	current_datetime = str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M"))

	headers = get_token()
	account = td_order.account_info(headers)

	portfolio_value = account['securitiesAccount']['currentBalances']['equity']
	ticker = []
	quantity = []
	market_value = []
	current_day_loss_profit = []

	for item in account['securitiesAccount']['positions']:
		if item['instrument']['assetType'] == 'EQUITY':
			# order goes like this: (ticker), (number of shares (no fractional shares)), (current market value of all shares held), (current day profit/loss in dollars)
			# available.append((item['instrument']['symbol'], int(item['longQuantity']), item['marketValue'], item['currentDayProfitLoss']))
			ticker.append(item['instrument']['symbol'])
			quantity.append(int(item['longQuantity']))
			market_value.append(item['marketValue'])
			current_day_loss_profit.append(item['currentDayProfitLoss'])
	
	new_row = {'datetime': current_datetime,
			   'portfolio_value': portfolio_value,
			   'ticker': ticker,
			   'quantity': quantity,
			   'market_value': market_value,
			   'current_day_loss_profit': current_day_loss_profit}
	portfolio_data_df = portfolio_data_df.append(new_row, ignore_index=True)

	# the following line creates a new csv for the data (keep it commented out)
	# portfolio_data_df.to_csv("portfolio_tracking.csv", index=True)

	# the following line appends the new row to pre-existing csv (mode a is append)
	portfolio_data_df.to_csv('portfolio_tracking.csv', mode='a', header=False, index=False)

	# todo:
"""
'$' means done
'?' means pospone
$add: check dividend sort tickers if they're valid
$add: implement td ameritrade 90 day validation and script management
$add: merge csv with old and remove duplicates every 90 days
$add: continual running loop and current time checking (use stock prediction notes)
$add: some sort of phone notification system updating portfolio value, purchases, sells, daily portfolio movement
$add: calculate how many shares to buy
$add: some sort of method to store what I purchased that day, so I know what and how much to sell the next day
$add: check for weekends
#add: fix order sell problem (I cant save the tickers from buy to sell them the next day)
$add: remote start functionality
$add: in case of any error/crash, send a message to my phone
$add: some sort of portfolio value tracking every 30 mins - added tracking every minute
?add: an interface where you can customize/create your own strategy
$add: try except to send any errrors to my phone
add: fix bug where the infinite while loop may purchase twice because some times are repeated twice (30 secs)
?add: machine learning interpratation to know the optimal time to sell
add: yfinance prediction indicator scrape (save predictions, and performances in timeline, probably csv)
add: look at previous reactions to dividends from the same stock (yahoo finance has it in chart), factor into decision
	 run simulation/papertrade on unconfirmed strategies.
$add: filter out low market stocks (calculated manually either at 100k or 1 mil) - backtested it, doesnt work
$add: fix fridays, it purchases for monday's ex dividend date, not tuesday's
add: sometimes it does a transaction twice, idk why fix it
add: sell only the previously purchased stocks, not everything
add: make another script that trades on indicators
add: update dividend_csv_maintenance for updated site (use Andrew's updated code)
add: upload all code to git (private)
add: the code in the main function takes some time to run in addition to the 60 second pause, 
	 this poses two issues; first, sometimes it would skip a minute because the total runtime 
	 is over 60 seconds. I need the total runtime to be exactly 60 seconds. I forgot the second lol.
add: fix dividend maintenance. install geckodriver
add: update: scrape dividends future with andrew's new scraping script
add: add gitignore
add: find reliable way to have task running in aws background
add: I can set the amount of money to invest with through text (stop the program, then send 
	 start + the amount)
add: create an additional script that checks if main.py is running and makes sure it's still running.
"""

if __name__ == '__main__':
	main_function(300, 3)