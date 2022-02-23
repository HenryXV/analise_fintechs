import data_collection
import sentiment
import wordcloud_maker
import pandas as pd

mencoes = data_collection.get_user_mentions("pagseguro")

tweets = [sentiment.preprocessing(i) for i in mencoes['text']]

list_tweets = []

for tweet in tweets:
    parsed_tweet = {'text': tweet}
    list_tweets.append(parsed_tweet)

df = pd.DataFrame(list_tweets)

wordcloud_maker.get_wordcloud(df)
