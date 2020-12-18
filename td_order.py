import requests
from configparser import ConfigParser
import time
from datetime import datetime, timedelta
from datetime import date
import datetime
import urllib
from splinter import Browser
import json
import os


def place_order(headers, ticker, quantity, instruction, quantityType):
	# headers is the authorization token
	# instruction is either 'Buy' or 'Sell'

	config = ConfigParser()
	config.read('config.ini')
	client_id = config['info']['client_id']
	account_number = config['info']['account_number']
	password = config['info']['password']

	# ACCOUNTS ENDPOINT
	# print(headers['Authorization_refresh'])
	# headers = headers['Authorization']

	# define an endpoint with a stock of your choice, MUST BE UPPER
	endpoint = r"https://api.tdameritrade.com/v1/accounts"

	# make a request
	content = requests.get(url = endpoint, headers = headers)

	# convert it dictionary object
	data = content.json()
	# print(data)

	# grab the account id
	account_id = data[0]['securitiesAccount']['accountId']
	print(account_id)

	# -------------------------------------------------------------

	# ACCOUNT ENDPOINT

	# define an endpoint with a stock of your choice, MUST BE UPPER
	endpoint = r"https://api.tdameritrade.com/v1/accounts/{}".format(account_id)

	# define the payload
	payload = {'apikey':client_id}

	# make a request
	content = requests.get(url = endpoint, headers = headers)

	# convert it dictionary object
	data = content.json()
	print(data)

	# -------------------------------------------------------------

	# ORDERS ENDPOINT - POST
	# define our headers
	access_token = headers['Authorization'][7:]
	header = {'Authorization':"Bearer {}".format(access_token),
	          "Content-Type":"application/json"}

	# define the endpoint for Saved orders, including your account ID
	endpoint = r"https://api.tdameritrade.com/v1/accounts/{}/orders".format(account_id)

	# define the payload, in JSON format
	payload = {'orderType':'MARKET',
	           'session':'NORMAL',
	           'duration':'DAY',
	           'orderStrategyType':'SINGLE',
	           'orderLegCollection':[{'instruction':instruction, 'quantity':quantity, 'quantityType': quantityType, 'instrument':{'symbol':ticker,'assetType':'EQUITY'}}]}


	# make a post, NOTE WE'VE CHANGED DATA TO JSON AND ARE USING POST
	content = requests.post(url = endpoint, json = payload, headers = header)

	# show the status code, we want 200
	content.status_code

def get_quote(ticker):

	config = ConfigParser()
	config.read('config.ini')
	client_id = config['info']['client_id']
	account_number = config['info']['account_number']
	password = config['info']['password']

	endpoint = r"https://api.tdameritrade.com/v1/marketdata/{}/quotes".format(ticker)
	payload = {'apikey': client_id,
			  }
	content = requests.get(url = endpoint, params = payload)
	data = content.json()
	# print(data)
	return data

def account_info(headers):

	config = ConfigParser()
	config.read('config.ini')
	client_id = config['info']['client_id']
	account_number = config['info']['account_number']
	password = config['info']['password']

	# ACCOUNTS ENDPOINT
	# print(headers['Authorization_refresh'])
	# headers = headers['Authorization']

	# define an endpoint with a stock of your choice, MUST BE UPPER
	endpoint = r"https://api.tdameritrade.com/v1/accounts"

	# make a request
	content = requests.get(url = endpoint, headers = headers)

	# convert it dictionary object
	data = content.json()
	# print(data)

	# grab the account id
	account_id = data[0]['securitiesAccount']['accountId']
	# print(account_id)

	# -------------------------------------------------------------

	# ACCOUNT ENDPOINT

	# define an endpoint with a stock of your choice, MUST BE UPPER
	endpoint = r"https://api.tdameritrade.com/v1/accounts/{}".format(account_id)

	# define the payload
	payload = {'fields':'positions'}

	# make a request
	content = requests.get(url = endpoint, params = payload, headers = headers)

	# convert it dictionary object
	data = content.json()
	# print(data)
	return data