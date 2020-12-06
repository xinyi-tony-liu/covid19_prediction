import socket
import sys
import requests
import requests_oauthlib
import json
import bleach
from bs4 import BeautifulSoup


# Include your Twitter account details
ACCESS_TOKEN = '1733598223-PqbqmO8dDbLjmf76rvsUYo1M5DiPzekROOCyYSV'
ACCESS_SECRET = 'sYlA5X5ScEKlRtPyMjRlFKft2mrKsG5SsKYM3agqzR9UK'
CONSUMER_KEY = '3nwyJEIXKf2ht0OX2Z2JRMvDY'
CONSUMER_SECRET = 'S74LuAe5EOGb9qJfOEw6bKtAGH9zqjJORsyJNgZUHIZu7h0zdU'
my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)


def get_tweets():
    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    query_data = [('language', 'en'), ('track','covid,coronavirus')]
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    return response




def send_tweets_to_spark(http_resp, tcp_connection):
    for line in http_resp.iter_lines():
            try:
                full_tweet = json.loads(line)
                tweet_text = full_tweet['text']
                print("Tweet Text: " + tweet_text)
                print ("------------------------------------------")
                tcp_connection.send(f'{tweet_text}\n'.encode('utf-8'))

            except:
                continue


TCP_IP = 'localhost'
TCP_PORT = 9001
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((TCP_IP, TCP_PORT))
s.listen(1)

print("Waiting for TCP connection...")
conn, addr = s.accept()

print("Connected... Starting getting tweets.")
resp = get_tweets()
send_tweets_to_spark(resp, conn)
