# review how to create a virutal environment so that you don't download information permanently
# this took me a long time to create because of the following bottlenecks
    # needed to upgrade my Twitter subscription
    # install pip tweepy -- here I have a question of when do you know you need to pip install AND import in the file?
    # when do you pip install X and not need to import, or import in the python file but not need to pip install? 

import tweepy
import csv
import ssl
import pandas


ssl._create_default_https_context = ssl._create_unverified_context


consumer_key = "JMFq9HN0USGrqjvtA8ZEBLHTT"
consumer_secret = "OlWgEZywRwYMdtGrm94z4WPtg9Hk5TQURXYntl6bsOPTMTE7eU"
access_token = "1462717268496842752-e3yRRPID1BfRmp0TsWEjEby0f7Tkbq"
access_token_secret = "bgpXRDDrOrfYq9FL5RKYz86xAkETguyEevKyTVRRrYX0M"

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
    
get_all_tweets("DalaiLama")
