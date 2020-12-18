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

def generate_tokens():
	config = ConfigParser()
	config.read('config.ini')
	client_id = config['info']['client_id']
	account_number = config['info']['account_number']
	password = config['info']['password']

	# define the location of the Chrome Driver - CHANGE THIS!!!!!
	executable_path = {'executable_path': r'C:\Users\lenovo\Desktop\chromedriver'}

	# Create a new instance of the browser, make sure we can see it (Headless = False)
	browser = Browser('chrome', **executable_path, headless=False)

	# define url components
	method = 'GET'
	client_code = client_id + '@AMER.OAUTHAP'
	url = 'https://auth.tdameritrade.com/auth?'
	payload = {'response_type':'code', 'redirect_uri':'http://localhost', 'client_id':client_code}

	# build the URL and store it in a new variable
	p = requests.Request(method, url, params=payload).prepare()
	myurl = p.url

	# go to the URL
	browser.visit(myurl)

	# define items to fillout form
	payload = {'username': account_number,
	           'password': password}

	# Fill Out the Form
	browser.find_by_id('username0').first.fill(payload['username'])
	browser.find_by_id('password').first.fill(payload['password'])
	browser.find_by_id('accept').first.click()
	time.sleep(1)

	# Get the Text Message Box
	browser.find_by_text('Can\'t get the text message?').first.click()

	# Get the Answer Box
	browser.find_by_value("Answer a security question").first.click()

	# Answer the Security Questions.
	if browser.is_text_present('INSERT SECURITY QUESTION 1'):
	    browser.find_by_id('secretquestion0').first.fill('INSERT SECURITY ANSWER 1')

	elif browser.is_text_present('INSERT SECURITY QUESTION 2'):
	    browser.find_by_id('secretquestion0').first.fill('INSERT SECURITY ANSWER 2')

	elif browser.is_text_present('INSERT SECURITY QUESTION 3'):
	    browser.find_by_id('secretquestion0').first.fill('INSERT SECURITY ANSWER 3')

	elif browser.is_text_present('INSERT SECURITY QUESTION 4'):
	    browser.find_by_id('secretquestion0').first.fill('INSERT SECURITY ANSWER 4')

	# Submit results
	browser.find_by_id('accept').first.click()

	# trust device
	time.sleep(1)
	browser.find_by_text('Yes, trust this device').first.click()
	# browser.find_by_id('trustthisdevice0_0').first.click()
	browser.find_by_id('accept').first.click()

	# Sleep and click Accept Terms.
	time.sleep(1)
	browser.find_by_id('accept').first.click()

	# give it a second, then grab the url
	time.sleep(1)
	new_url = browser.url

	# grab the part we need, and decode it.
	parse_url = urllib.parse.unquote(new_url.split('code=')[1])

	# close the browser
	browser.quit()

	# print(parse_url)


	# ---------------------------------------------------------------


	# THE AUTHENTICATION ENDPOINT

	# define the endpoint
	url = r"https://api.tdameritrade.com/v1/oauth2/token"

	# define the headers
	headers = {"Content-Type":"application/x-www-form-urlencoded"}

	# define the payload
	payload = {'grant_type': 'authorization_code', 
	           'access_type': 'offline', 
	           'code': parse_url, 
	           'client_id':client_id, 
	           'redirect_uri':'http://localhost'}

	# post the data to get the token
	authReply = requests.post(r'https://api.tdameritrade.com/v1/oauth2/token', headers = headers, data=payload)

	# convert it to a dictionary
	decoded_content = authReply.json()
	print(decoded_content)


	# grab the access_token and refresh_token
	access_token = decoded_content['access_token']
	refresh_token = decoded_content['refresh_token']
	headers = {'Authorization': "Bearer {}".format(access_token)}
	headers_refresh = {'Authorization': "Bearer {}".format(refresh_token)}

	# save the access_token and refresh_token
	with open('temp_data.json', 'w') as outfile:
	    json.dump(headers, outfile)
	with open('temp_data_refresh.json', 'w') as outfile:
	    json.dump(headers_refresh, outfile)