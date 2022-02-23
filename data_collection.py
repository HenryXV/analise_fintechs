import sys
import tweepy
import os
import pandas as pd
from tweepy import OAuthHandler
from tweepy import Cursor
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
KEY_SECRET = os.getenv('KEY_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
TOKEN_SECRET = os.getenv('TOKEN_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

def get_twitter_auth():
    try:
        consumer_key = API_KEY
        consumer_secret = KEY_SECRET
        access_token = ACCESS_TOKEN
        access_secret = TOKEN_SECRET

    except KeyError:
        sys.stderr.write("Não foi possível autenticar\n")
        sys.exit(1)

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    return auth

def get_twitter_api():
    auth = get_twitter_auth()
    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api

def get_user_id(twitter_username):
    client = get_twitter_api()

    user = client.get_user(id=twitter_username)

    return user.id_str

def get_user_mentions(query, page_limit=16, count_tweet=200):
    api = get_twitter_api()

    lista_mentions = []

    # busca as menções em diferentes páginas do twitter
    for page in Cursor(api.search_tweets,
                       q=query,
                       lang='pt',
                       count=count_tweet).pages(page_limit):
        for mention in page:
            parsed_mention = {'text': mention.text}

            lista_mentions.append(parsed_mention)

    # criando dataframe com as mentions
    df = pd.DataFrame(lista_mentions)

    # removendo tweets duplicados
    df = df.drop_duplicates('text', keep='first')

    return df
