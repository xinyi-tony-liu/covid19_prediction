import socket
import sys
import requests
import requests_oauthlib
import json
import bleach
from time import sleep
from bs4 import BeautifulSoup
from datetime import date, timedelta

year = int(sys.argv[1])
month = int(sys.argv[2])
day = int(sys.argv[3])
targetDate = date(year, month, day)

# Include your Twitter account details
ACCESS_TOKEN = '1733598223-PqbqmO8dDbLjmf76rvsUYo1M5DiPzekROOCyYSV'
ACCESS_SECRET = 'sYlA5X5ScEKlRtPyMjRlFKft2mrKsG5SsKYM3agqzR9UK'
CONSUMER_KEY = '3nwyJEIXKf2ht0OX2Z2JRMvDY'
CONSUMER_SECRET = 'S74LuAe5EOGb9qJfOEw6bKtAGH9zqjJORsyJNgZUHIZu7h0zdU'
my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)

nextParam = ''
def get_tweets(query_date = date.today()):
    toDate = query_date + timedelta(days = 1)
    query_url = 'https://api.twitter.com/1.1/tweets/search/fullarchive/dev.json'
    query_data = None
    global nextParam
    if nextParam == '':
        query_data = {
            'query': '(covid OR coronavirus) place_country:CA',
            'fromDate': query_date.strftime("%Y%m%d0000"),
            'toDate': toDate.strftime("%Y%m%d0000")
        }
    else:
        query_data = {
            'query': 'covid',
            'next': nextParam
        }
    response = requests.post(
        query_url,
        auth = my_auth,
        json = query_data
    )
    resJSON = response.json()
    nextParam = resJSON['next']
    print(query_url, response)
    return resJSON['results']

def send_tweets_to_spark(tcp_connection):
    for _ in range(100):
        tweets = get_tweets(targetDate)
        for tweet in tweets:
            try:
                tweet_text = tweet['text'] + '\n'
                print("Tweet Text: " + tweet_text)
                print ("------------------------------------------")
                tcp_connection.send(tweet_text.encode('utf-8'))
            except:
                continue
        sleep(1) # so that we don't exceed the rate limit


TCP_IP = 'localhost'
TCP_PORT = 9001
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((TCP_IP, TCP_PORT))
s.listen(1)

print("Waiting for TCP connection...")
conn, addr = s.accept()

print("Connected... Starting getting tweets.")
send_tweets_to_spark(conn)
