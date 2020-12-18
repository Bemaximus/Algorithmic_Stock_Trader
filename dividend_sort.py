import pandas as pd
from datetime import date
from datetime import datetime, timedelta
import os
import yfinance as yf
# dir_path = os.path.dirname(os.path.realpath(__file__)) 

entries = pd.read_csv("all_entries_filtered.csv")
# entries = pd.read_csv("data/all_thestreet_dividends_updated_normal.csv")
# entries = pd.read_csv("../../data/dividends/all_entries_filtered_andrew.csv")
entries = entries.dropna()

def all_tickers_today():
	# Note: this outputs the tickers for the next_day's ex-dividend date
	ex_dates_list = entries['Ex-Dividend Date']
	ex_ticker_list = entries['Ticker']
	# day shift should normally be at 1, but can be changed to look at future dates
	# day_shift = 1
	today = date.today()# + timedelta(days=day_shift)

	# The following checks if today is a weekend and (if True) shifts the date to Monday
	while True:
		if today.weekday() == 5 or today.weekday() == 6:
			day_shift = 1
			today = today + timedelta(days=day_shift)
			# print(today)
		else:
			break

	day_shift = 2
	today = today + timedelta(days=day_shift)

	print('Ex-date:', str(today))
	today = str(today)

	today_date = str(today[5:7]) + '/' + str(today[8:10]) + '/' + str(today[0:4])
	if today_date[0] == '0':
		today_date_month = today_date[1]
	else:
		today_date_month = today_date[0:2]
	if today_date[3] == '0':
		today_date_day = today_date[4]
	else:
		today_date_day = today_date[3:5]
	today_date_year = today_date[6:]
	today_date = today_date_month + '/' + today_date_day + '/' + today_date_year
	today_ticker_dates_index = []
	for idx, item in ex_dates_list.iteritems():
		item = str(item)
		if item == today_date:
			today_ticker_dates_index.append(idx)
	ticker_list = []

	# duplicate removal loop
	today_ticker_dates_index_new = []
	for i in today_ticker_dates_index:
		if ex_ticker_list[i] in ticker_list:
			pass
		else:
			ticker_list.append(ex_ticker_list[i])
			today_ticker_dates_index_new.append(i)

	# ticker validation (removes any invalid ticker symbols)
	today_final_ticker_index = []
	today_final_ticker_list = []
	for i in today_ticker_dates_index_new:
		stock = yf.Ticker(ex_ticker_list[i])
		hist = stock.history(period='1d')
		if hist.empty:
			pass
		else:
			today_final_ticker_index.append(i)
			today_final_ticker_list.append(ex_ticker_list[i])

	return today_final_ticker_list, today_final_ticker_index

def highest_paying_tickers(top_n):
	ticker_list, ticker_index = all_tickers_today()
	# print(ticker_list)
	# print(ticker_index)
	data = {'ticker': [],
			'payout': []}
	entries_today = pd.DataFrame(data, columns = ['ticker', 'payout'])
	for item in ticker_index:
		if entries['Period'][item] == 'monthly':
			payout = float(entries['Yield'][item][:-1]) / 12
			new_row = {'ticker': entries['Ticker'][item], 'payout': payout}
			entries_today = entries_today.append(new_row, ignore_index=True)
		elif entries['Period'][item] == 'quarterly':
			payout = float(entries['Yield'][item][:-1]) / 4
			new_row = {'ticker': entries['Ticker'][item], 'payout': payout}
			entries_today = entries_today.append(new_row, ignore_index=True)
		elif entries['Period'][item] == 'semi-annual':
			payout = float(entries['Yield'][item][:-1]) / 2
			new_row = {'ticker': entries['Ticker'][item], 'payout': payout}
			entries_today = entries_today.append(new_row, ignore_index=True)
		elif entries['Period'][item] == 'annual':
			payout = float(entries['Yield'][item][:-1]) / 1
			new_row = {'ticker': entries['Ticker'][item], 'payout': payout}
			entries_today = entries_today.append(new_row, ignore_index=True)

	entries_today = entries_today.nlargest(top_n, ['payout'])
	entries_today.reset_index(drop=True, inplace=True)
	print(entries_today)
	return entries_today




if __name__ == '__main__':
	pass
	highest_paying_tickers(3)
	# all_tickers_today()
# output ticker(s) to invest in for the day 