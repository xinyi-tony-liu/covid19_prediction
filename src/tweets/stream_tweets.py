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
ACCESS_TOKEN = '1338378148086505472-J3bioJBqkg3MsL1KXCqEwWjXODvqsR'
ACCESS_SECRET = '7RzXAusydHD1VvkGDJsIVBJBdJtDAY8nmengbbDnvlnI1'
CONSUMER_KEY = 'gu0BsNG3wvWqw7AL4z2W16x2G'
CONSUMER_SECRET = '3OvW9AIcbMIclS35DXNK1hLzPaWWKBMT3glcwk9ZeIzANyA6Jn'
my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)

def get_tweets(query_date = date.today(), countryCode = 'ca'):
    toDate = query_date + timedelta(days = 14)
    query_url = 'https://api.twitter.com/1.1/tweets/search/fullarchive/dev.json'
    query_data = {
        'query': '(covid OR coronavirus) place_country:{}'.format(countryCode),
        'fromDate': query_date.strftime("%Y%m%d0000"),
        'toDate': toDate.strftime("%Y%m%d0000")
    }
    response = requests.post(
        query_url,
        auth = my_auth,
        json = query_data
    )
    try:
        resJSON = response.json()
        print(query_url, response)
        return resJSON['results']
    except:
        print(response)
        print(response.text)


def send_tweets_to_spark(tcp_connection):
    for countryCode in ['AU', 'CA', 'CY', 'IS', 'NZ', 'US']:
        tweets = get_tweets(targetDate, countryCode)
        for tweet in tweets:
            try:
                tweet_text = tweet['text'].replace("\n", " ") + '\n'
                print("Tweet Text: " + tweet_text)
                print ("------------------------------------------")
                tcp_connection.send(
                    '{} {}'.format(countryCode, tweet_text).encode('utf-8')
                )
            except:
                continue
        sleep(2) # so that we don't exceed the rate limit
    tcp_connection.close()


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
