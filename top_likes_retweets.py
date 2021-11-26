# importing libraries and packages
import snscrape.modules.twitter as sntwitter
import pandas as pd 

# Creating list to append tweet data 
tweets_list1 = []

# Using TwitterSearchScraper to scrape data and append tweets to list

for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:kevinroose, include:nativeretweets').get_items()): #declare a username 
    if i>10: #number of tweets you want to scrape
        break
    tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.retweetedTweet]) #declare the attributes to be returned
    
# Creating a dataframe from the tweets list above 
tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Retweet ID'])
print(tweets_df1)


#likes_retweet('kevinroose')
                          
# pull the retweets 
# for tweet in tweepy.Cursor(api.search, q='github filter:retweets',tweet_mode='extended').items(5)
# does tweepy.cursor still work? 

# find the user_id of the person who originally tweeted the tweet that is being retweeted 

# https://towardsdatascience.com/how-to-scrape-more-information-from-tweets-on-twitter-44fd540b8a1f#eaf6

#The two options for retweets are:

#snscrape twitter-search 'from:username include:nativeretweets' – This only works for retweets from the past 7 days (and only returns normal tweets further back).
#snscrape twitter-profile username – This only returns the ~3200 most recent tweets, including retweets among those (which may go back further than 7 days).
#I am not aware of any way to get retweets beyond these two methods. GetOldTweets3 seems to have used the (old design) web search just like snscrape does, 
    #so it should have had the same 7-day limitation.

#Replies are normal tweets and extracted with the standard twitter-user scraper or the equivalent twitter-search from:username. 
#twitter-profile also returns them but with the same limitation as above.