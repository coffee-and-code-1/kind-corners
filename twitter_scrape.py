# review virtual env 

# this took me a long time initially b/c of the following bottlenecks 
    # needed to upgrade my Twitter subscription
    # install pip tweepy -- how do you know when you need to pip install + import file, vs only import file (no pip install)

import tweepy
import csv
import ssl
import pandas as pd 


#import nltk
#nltk.download('punkt')
#nltk.download('wordnet')
#from nltk import sent_tokenize, word_tokenize
#from nltk.stem.snowball import SnowballStemmer
#from nltk.stem.wordnet import WordNetLemmatizer
#from nltk.corpus import stopwords

import numpy as np
import re  

#import spacy
#nlp = spacy.load('en_core_web_lg')

#from twitterscraper import query_tweets
#from twitterscraper.query import query_tweets_from_user
#import datetime as dt 

ssl._create_default_https_context = ssl._create_unverified_context

consumer_key = " "
consumer_secret = " "
access_token = " "
access_token_secret = " " 

def get_all_tweets(screen_name):

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

#print(tweepy.__version__)

# extract the latest 200 tweets using api.user_timeline

    tweets = api.user_timeline(screen_name=screen_name,
                               count=10,
                               include_rts = False, 
                           # necessary to keep full_text, otherwise only first 140 words extracted
                               tweet_mode = 'extended'
                               )

# tweets is a list in this case, info is each item in the list 

    for info in tweets:
        print("ID: {}".format(info.id))
    # this is the ID of the tweet itself you would find it in the URL link
        print(info.created_at)
        print(info.full_text)
        print(info.user.location) 
        print(info.user.followers_count)
        print(info.retweet_count)
        print("\n")

# now we want to transform these tweets into a 2-D array that will populate the CSV 

    outtweets = [[info.id_str, info.created_at, info.full_text, info.user.location, info.retweet_count] for info in tweets] 

    with open(f'new_{screen_name}_tweets.csv', 'w', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id","created at","text","location","retweet count"])
        writer.writerows(outtweets)
        
    df=pd.read_csv("new_{}_tweets.csv".format(screen_name))
    print(df)
    # this is ok for now -- but can we find a better way to put all of the tweets in one file instead of multiple CSVs? 
    
    #ds_tweets=pd.DataFrame(t.__dict__ for ds in ds_tweets)
    #print(ds_tweets)


get_all_tweets("DalaiLama")

# eventually you want to automatically add people to the inspirational_individuals list if they show up a certain % of times in someone's retweets 

#for individual in inspirational_individuals:
    #get_all_tweets(individual)
   

# --- exercise #1 -- isolate the top words in the tweets when you remove the "in", "and", "etc." 

# to do this, you  need to isolate a dataframe for the text itself
#ds_tweets = pd.DataFrame(t.__dict__ for ds in ds_tweets)
#print(ds_tweets)

# ----- other exercises to be filled in
# top liked tweets 
# retweets, so that you can find additional twitter users to follow (follow your inspiration's inspiration) 
# region 
# words that are commonly used as in the same sentence as the search words you're initially looking for
