import requests
import json
from configparser import ConfigParser
import time # remove this (temporary)
import os

config = ConfigParser()
config.read('config.ini')
telegram_key = config['info']['telegram_key']
telegram_chat_id = config['info']['telegram_chat_id']

def get_last_message_telegram():
    endpoint = r'http://api.telegram.org/bot{}/getUpdates'.format(telegram_key)
    content = requests.get(url=endpoint)
    data = content.json()
    try: 
        last_message = data['result'][-1]['message']['text']
    except:
        last_message = 'none'
    # print(data)
    # print(last_message)
    return last_message

    # the following is to get all the messages (unnecessary)
    # for item in data['result']:
    #   print(item['message']['text'])
    # print(data)

def delete_last_message_telegram():
    endpoint = r'http://api.telegram.org/bot{}/getUpdates'.format(telegram_key)
    content = requests.get(url=endpoint)
    data = content.json()
    last_message_id = data['result'][-1]['message']['message_id']

    endpoint = r'http://api.telegram.org/bot{}/deleteMessage?chat_id='.format(telegram_key)
    endpoint = (endpoint + '{}' + '&message_id=').format(telegram_chat_id)
    endpoint = (endpoint + '{}').format(last_message_id)
    content = requests.get(url=endpoint)

def send_message_telegram(body):
    endpoint = r'http://api.telegram.org/bot{}/sendMessage?chat_id='.format(telegram_key)
    endpoint = (endpoint + '{}' + '&text=').format(telegram_chat_id)
    endpoint = (endpoint + '{}').format(body)
    requests.get(url=endpoint)
    # data = content.json()

# temp_blacklist_telegram = None
def reply_message_telegram_1(prompt, reply):
    # Note: important, you must use a different function (with ending number) to test
    # for a message being recieved or else it would not work, as each function uses its 
    # own temp-file. If used more than once in the same loop, all runs after the first will
    # not work.

    # global temp_blacklist_telegram
    endpoint = r'http://api.telegram.org/bot{}/getUpdates?offset=133494340'.format(telegram_key)
    content = requests.get(url=endpoint)
    data = content.json()
    
    # print('last update id', data['result'][-1]['update_id'])
    # for item in data['result']:
    #     print(item['message']['text'])
    # print('length', len(data['result']))

    try:
        # print('try')
        last_message = data['result'][-1]['message']['text']
        last_message_id = data['result'][-1]['message']['message_id']
    except:
        # print('except')
        last_message = 'none'
        last_message_id = '0'

    # print(temp_blacklist_telegram)
    with open('temp_blacklist_telegram_1.json', 'r') as json_file:
        temp_blacklist = json.load(json_file)

    # print(last_message.lower(), prompt)
    # print(temp_blacklist, last_message_id)

    # print(last_message.lower(), '---', prompt)
    # print(temp_blacklist, '---', last_message_id)
    if last_message.lower() == prompt and temp_blacklist != last_message_id:
        print('send')
        # print(data)
        send_message_telegram(reply)

        with open('temp_blacklist_telegram_1.json', 'w') as outfile:
          json.dump(last_message_id, outfile)

        return prompt
        # time.sleep(3)


    # time.sleep(0.5)
    # os.remove('temp_blacklist_telegram.json')
    with open('temp_blacklist_telegram_1.json', 'w') as outfile:
        json.dump(last_message_id, outfile)
    # outfile.close()
    # print('pass')
    # temp_blacklist_telegram = last_message_id


    # endpoint = (endpoint + '?offset={}').format(message_length - 1)
    # content = requests.get(url=endpoint)
    # data = content.json()
    # print(data)

def reply_message_telegram_2(prompt, reply):
    # Note: important, you must use a different function (with ending number) to test
    # for a message being recieved or else it would not work, as each function uses its 
    # own temp-file. If used more than once in the same loop, all runs after the first will
    # not work.
    
    # global temp_blacklist_telegram
    endpoint = r'http://api.telegram.org/bot{}/getUpdates?offset=133494340'.format(telegram_key)
    content = requests.get(url=endpoint)
    data = content.json()
    
    # print('last update id', data['result'][-1]['update_id'])
    # for item in data['result']:
    #     print(item['message']['text'])
    # print('length', len(data['result']))

    try:
        # print('try')
        last_message = data['result'][-1]['message']['text']
        last_message_id = data['result'][-1]['message']['message_id']
    except:
        # print('except')
        last_message = 'none'
        last_message_id = '0'

    # print(temp_blacklist_telegram)
    with open('temp_blacklist_telegram_2.json', 'r') as json_file:
        temp_blacklist = json.load(json_file)

    # print(last_message.lower(), prompt)
    # print(temp_blacklist, last_message_id)

    print(last_message.lower(), '---', prompt)
    print(temp_blacklist, '---', last_message_id)
    if last_message.lower() == prompt and temp_blacklist != last_message_id:
        print('send')
        # print(data)
        send_message_telegram(reply)

        with open('temp_blacklist_telegram_2.json', 'w') as outfile:
           json.dump(last_message_id, outfile)

        return prompt
        # time.sleep(3)


    # time.sleep(0.5)
    # os.remove('temp_blacklist_telegram.json')
    with open('temp_blacklist_telegram_2.json', 'w') as outfile:
        json.dump(last_message_id, outfile)
    # outfile.close()
    # print('pass')
    # temp_blacklist_telegram = last_message_id


    # endpoint = (endpoint + '?offset={}').format(message_length - 1)
    # content = requests.get(url=endpoint)
    # data = content.json()
    # print(data)

def reply_message_telegram_3(prompt, reply):
    # Note: important, you must use a different function (with ending number) to test
    # for a message being recieved or else it would not work, as each function uses its 
    # own temp-file. If used more than once in the same loop, all runs after the first will
    # not work.
    
    # global temp_blacklist_telegram
    endpoint = r'http://api.telegram.org/bot{}/getUpdates?offset=133494340'.format(telegram_key)
    content = requests.get(url=endpoint)
    data = content.json()
    
    # print('last update id', data['result'][-1]['update_id'])
    # for item in data['result']:
    #     print(item['message']['text'])
    # print('length', len(data['result']))

    try:
        # print('try')
        last_message = data['result'][-1]['message']['text']
        last_message_id = data['result'][-1]['message']['message_id']
    except:
        # print('except')
        last_message = 'none'
        last_message_id = '0'

    # print(temp_blacklist_telegram)
    with open('temp_blacklist_telegram_3.json', 'r') as json_file:
        temp_blacklist = json.load(json_file)

    # print(last_message.lower(), prompt)
    # print(temp_blacklist, last_message_id)

    # print(last_message.lower(), '---', prompt)
    # print(temp_blacklist, '---', last_message_id)
    if last_message.lower() == prompt and temp_blacklist != last_message_id:
        print('send')
        # print(data)
        send_message_telegram(reply)

        with open('temp_blacklist_telegram_3.json', 'w') as outfile:
           json.dump(last_message_id, outfile)

        return prompt
        # time.sleep(3)


    # time.sleep(0.5)
    # os.remove('temp_blacklist_telegram.json')
    with open('temp_blacklist_telegram_3.json', 'w') as outfile:
        json.dump(last_message_id, outfile)
    # outfile.close()
    # print('pass')
    # temp_blacklist_telegram = last_message_id


    # endpoint = (endpoint + '?offset={}').format(message_length - 1)
    # content = requests.get(url=endpoint)
    # data = content.json()
    # print(data)

def remote_test_telegram():
    message = get_last_message_telegram()
    if message.lower() == 'test':
        # delete_last_message_telegram()
        send_message_telegram('Test recieved, program is working.')

def temp_main(prompt, body):
    x = 0
    while True:
        reply_message_telegram(prompt, body)
        x += 1
        print(x)
        # time.sleep(1)
        break


# reply_message_telegram('hii', 'hello')
# temp_main('test','test') 
# send_message_telegram('hellooo')

# get_last_message_telegram()







# endpoint = r'http://api.telegram.org/bot{}/getWebhookInfo'.format(telegram_key)
# content = requests.get(url=endpoint)
# data = content.json()
# print(data)













































# class telegram():

#     def __init__(self, config):
#         self.token = self.read_token_from_config_file(config)
#         self.base = "https://api.telegram.org/bot{}/".format(self.token)

#     def get_updates(self, offset=None):
#         url = self.base + "getUpdates?timeout=100"
#         if offset:
#             url = url + "&offset={}".format(offset + 1)
#         r = requests.get(url)
#         return json.loads(r.content)

#     def send_message(self, msg, chat_id):
#         url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
#         if msg is not None:
#             requests.get(url)

#     def read_token_from_config_file(self, config):
#         parser = cfg.ConfigParser()
#         parser.read(config)
#         return parser.get('creds', 'token')