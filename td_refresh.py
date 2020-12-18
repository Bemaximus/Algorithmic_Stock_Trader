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


def get_token_from_refresh():

	config = ConfigParser()
	config.read('config.ini')
	client_id = config['info']['client_id']
	account_number = config['info']['account_number']
	password = config['info']['password']

	with open('temp_data.json', 'r') as json_file:
	    headers_auth = json.load(json_file)
	with open('temp_data_refresh.json', 'r') as json_file:
	    headers_refresh = json.load(json_file)
	headers_refresh['Authorization'][7:]


	# Refresh authorization check and endpoint

	# # checks refresh_token age
	# file = os.stat('temp_data_refresh.json')
	# st = file.st_mtime
	# datetime_object = datetime.date.fromtimestamp(st)
	# print(datetime_object)
	# age = str(date.today() - datetime_object)
	# age = age.split('day')[0][:-1]
	# if age[0] == '0':
	#     age = 0
	# print(age)
	# def check_token():
	#     if age > 89:
	#         return('erorr: create new access token')
	# check_token()

	# define the endpoint
	url = r"https://developer.tdameritrade.com/authentication/apis/post/token-0"
	# url = r"https://api.tdameritrade.com/v1/oauth2/token"


	# define the headers
	headers = {"Content-Type":"application/x-www-form-urlencoded"}

	# define the payload
	payload = {'grant_type': 'refresh_token', 
	           'refresh_token': headers_refresh['Authorization'][7:],
	#            'access_type': 'offline', 
	#            'code': parse_url, 
	           'client_id':client_id, 
	#            'redirect_uri':'http://localhost'
	          }

	# post the data to get the token
	authReply = requests.post(r'https://api.tdameritrade.com/v1/oauth2/token', headers=headers, data=payload)

	# convert it to a dictionary
	decoded_content = authReply.json()
	# print(decoded_content)

	access_token = decoded_content['access_token'] 
	headers = {'Authorization': "Bearer {}".format(access_token)}
	return headers