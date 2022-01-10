# Intended flow of the exercise 

# 1. Do a simple scrape of tweets of users we like because we want to see if there's any new users we should add to our list based on their responses, mentions, or retweets 
# 2. Add any potential new users to your master list of users, but keep two seperate entities so you can reference it at the end ["we added these new users, etc."]
# 3. Run a full serach of X tweets for your combined master list of users
# 4. Slice/dice the dataframe of the master list of tweets so that you isolate the top tweets based on retweets (or likes), save this slice to a new variable 
# 5. Slice/dice based on location -- this one is more difficult because we do not possess the know-how to create a map key [Asia: Taiwan, Japan, Korean, China, etc.] so for now
    # later we would like to test if grouping based geolocation is more effective 
    # We have to potentially manually slice the tweets based on a specific city. For now, see if you can slice based on a city so that your final text reads
    # "In {location}, the top tweet is {X}" -- in Los Angeles, the top tweet is X. 
# 6. Apply NLP to the original master list of tweets, pull out the stop words, and see what are the most common words being used in these tweets. 
# 7. Use the information to run a phrase-based query in Twitter, in this case I've created a hashtag-driven search. 
    # similar to how you had a list of users initially, but then added some new users based on the retweets. 
    # Write a CSV with all tweets (organized in a dataframe) as a reference point for step 8 
# 8. Print a preliminary draft of my weekly write-up to work off of.  

# 1/10/2022 
# took out use of snscrape because Twitter is effectively blocking AWS API requests, and I discovered that tweepy's user_timeline function can also include native retweets which is what I was originally using snscrape for 

import pandas as pd
import csv 
from csv import writer 
import tweepy
import numpy as np 
import re 
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import seaborn as snsf
import nltk
from nltk.corpus import stopwords
import spacy
nlp = spacy.load('en_core_web_sm')

from copy import deepcopy 
from copy import copy 
import datetime as dt

# global variables that we're putting at the top so everyone can access 

phrase_search_tweets = [] # this list is for the phrase search, regardless of user - used in step # 7 

new_phrases_list = [] # use this to collect any manual new phrases you want to search, first used in step # 6 
initial_phrase_list = ['#christmascheer', '#holidaykindness', '#kinship'] # first used in step # 6 
master_phrase_list = [] # first used in step # 6 

US_tweets = []
ASIA_tweets = [] 

final_text = [] # this is to be used in our final step, # 8, when we print an outline of the weekly draft, but we are not printing it here. This is first used in step # 4
master_tweets = [] # creating an empty list to house all of your tweets, before putting them in a Dataframe - first used in #3
master_user_list = [] # this is to house the adding of two lists - first used in # 2
new_user_list = [] # this is to house the additional users you found - first used in # 2
first_users_list = ['HEB', 'DalaiLama','jnovogratz','FredRogersPro','Yoyo_Ma','somegoodnews','goodgoodgood','goodnewsmoveme3','withlovecleo']  # first used in part # 1

# 8 --- let's create the final preview 

def weekly_preview():
    
    final_CSV = open('full_tweet_search.csv', 'w', encoding='utf-8')
    # 'w' is write or overwrite 
    writer = csv.writer(final_CSV) 
    writer.writerows(master_tweets) 
    writer.writerows(phrase_search_tweets)
    final_CSV.close()
    # this is so you can access full_tweet_search when deciding which one is your favorite story 
    
    today = dt.datetime.today().strftime("%m/%d/%Y")
    favorite_story = input("What do you want the favorite story or tweet of this week to be? ")
    
    print(f"This week in Kind Corners {today}")
    print("\n")
    print(f"Our favorite story is {favorite_story}") 
    print("\n")
    print(f"The most popular retweets of this week, based on number of retweets, was {final_text}")
    print("\n")
    print(f"In Asia, the top trending stories are {ASIA_tweets}") 
    print("\n")
    print(f"In the US, the top trending stories are {US_tweets}") 
    print("\n")
    print(f"Based on some of the retweets of our favorite people, we found some additional stories from {new_user_list} this week") # their stories include [G,H,I] (where G,H,I are the stories you added from their pages)
    print("\n")
    print(f"We particularly liked some stories that focused on {master_phrase_list}") # add later - and our picks for this week are [J,K,L], where [J,K,L] should be the top stories from a sorted [phrase_search_tweets]
    print("\n")
    print("For a heartwarming longer read, check out [Y]") #later on, build an input function or variable for this when you find ways to collect longer reads 
    print("\n")
    print("Wishing you a happy weekend and see you next week!") 
    # can we write this in word document form? At the very least, write a CSV file including 1. master_user_list 2. master_tweets 3. master_phrase_list 4. phrase_search_tweets

    exit() 

# 7 ---- running a new, phrase-based, query on twitter unristricted to specific users. 

def text_based_search():

    global master_phrase_list 
    global initial_phrase_list
    global new_phrases_list 
    global phrase_search_tweets 
    
    for phrase in master_phrase_list:

        print(phrase)
        # it doesn't make sense to me why the phrases are printed in succession -- it should be that for each phrase in the list, you print the list related to the query, run the search, and then do it again
        tweets = api.search_tweets(q=phrase, count=10)
        # you want to finess this search so that you can eliminate retweets -- often times we're getting the same original tweet multiple times b/c of the #hashtag-driven search 
        outtweets = [[info.user.screen_name, info.text, info.created_at, info.user.location, info.retweet_count, info.favorite_count] for info in tweets]
        phrase_search_tweets.extend(outtweets)
    
    df_last_frame = pd.DataFrame(phrase_search_tweets, columns=['Username','Text','Tweet Datetime', 'Place', 'Retweets', 'Favorites'])
    print(df_last_frame)
    # if you push this one tab over, it will print a new list for every phrase count you have, so 3 phrases = 3 prints, each one 10 tweets longer thant he earlier one  
    
    weekly_preview()

# 6 --- use NLP to plot a visual of the top words being used among all the tweets you've collected 

def find_top_words():

    # do not use global master_tweets 
    # we did not use global master_tweets because in this case, I do not want to permanently delete columns from master_tweets raw data, I only want to do it for this local exercise
    global master_phrase_list
    global initial_phrase_list
    global new_phrases_list 
    
    # we want to create a local copy so that the global variable remains untouched 
    local_tweets = deepcopy(master_tweets)
    # there is a diff between copy an deepcopy if you have lists within lists -- which in this case we do, mastertweets is al ist of tweets, tweet is a list of details 
    # if you working with a list that does not have sublists, then copy vs deepcopy does not matter. 
    
    parsed_lines = []  
    word_box = []
    # these 2 dont need to be global so we make them variable 
    print("Now we are looking for the top words in the existing tweets we've scraped to help us consider other phrases want to search twitter for additional stories. ")
    
    for tweet in local_tweets:

        del tweet[2:6]
        del tweet[0]
    
    for raw_text_tweet in local_tweets:
        for words in raw_text_tweet: 
            list_of_words = words.split()
            word_box.extend(list_of_words)
    
    # print(word_box) - print the word box if you need a sanity check to see what words are being picked up 

    lines = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in word_box] 

    for word_2 in lines:
        if word_2 not in nlp.Defaults.stop_words: 
            parsed_lines.append(word_2)
            
    df = pd.DataFrame(parsed_lines)
    
    df = df[0].value_counts()

    df = df[:20,]
    
    plt.figure(figsize=(10,5))
    x = df.values
    y = df.index
    sns.barplot(x=x, y=y, alpha=0.8)

    plt.title('Top words overall')
    plt.ylabel('Word from tweet',fontsize=12)
    plt.xlabel('Count of words', fontsize=12)
    plt.show()
    
##    there is an error here where we have an empty space with a word count of 40, what is it? 

    while True:
    
        new_phrase = input("Are there any (more) phrases you'd like to add to a phrase-search based on the top words you see here? If so, type the phrase here. If not, type 'no'. ")
    
        if new_phrase == 'no':
            master_phrase_list = initial_phrase_list + new_phrases_list # if this is empty, then it won't do anything, but it won't hurt either to have this all-encompassing addition
            print(f"The list of phrases we are searching twitter for is {master_phrase_list}. ")
            text_based_search() # now move on to # 7 
        else:
            new_phrases_list.append(new_phrase)   
            

# 5 --- adjusting the master tweets list to now identify the buzz based on region specifically 


def top_tweets_per_location():
    
    global master_tweets 
    global US_tweets
    global ASIA_tweets

    df=pd.DataFrame(master_tweets,columns=['Username','Text','Tweet Datetime', 'Place', 'Retweets', 'Favorites'])
    
    # try creating a new column to show the broader region its part of 
    df['Global Region'] = df['Place'].map({'San Antonio, Texas' : 'United States', 'Dharamsala, India' : 'Asia', 'New York, NY': 'United States', 'Pittsburgh' : 'United States'})
    # you can print this out if you want confirmation that the additional column is being added, and to see what other keys you would want to add to your map
 
    # one way to filter pandas is using boolean expressions -- below is a creation of a boolean variable where if the global region is equal to United States, the statement is true
    is_region_USA = df['Global Region']=='United States'
    df_USA = df[is_region_USA]
    df_USA_sorted=df_USA.sort_values(["Retweets"],ascending=(False))
    top_USA_likes=df_USA_sorted.head(5)
    print("The top tweets in the U.S. include: ")
    print(top_USA_likes['Text'])
    US_tweets.extend(top_USA_likes['Text'])
    
    print("\n")
    
    is_region_ASIA = df['Global Region']=='Asia'
    df_ASIA = df[is_region_ASIA]
    df_ASIA_sorted=df_ASIA.sort_values(["Retweets"],ascending=(False))
    top_ASIA_likes=df_ASIA_sorted.head(5)
    print("The top tweets in Asia include: ")
    print(top_ASIA_likes['Text'])
    ASIA_tweets.extend(top_ASIA_likes['Text'])
    # find a way to write these instructions only 1x, never manually 2x 

    find_top_words()
    
   
# 4 --- adjusting the master_tweets [] list which is now full of tweets and slicing/dicing it so that you isolate the top tweets based on what you're looking for 

def popular_rank():
    
    global master_tweets 
    global final_text 
    # the weird thing is that in our earlier version v1, we didn't need to specify 'global' master_tweets, and yet the script did not have an issue with master_tweets raw data, I wonder why that is 
    
    df=pd.DataFrame(master_tweets,columns=['Username','Text','Tweet Datetime', 'Place', 'Retweets', 'Favorites'])
    # remebmer that the dataframe itself is not accessible outside of full_search because you created it within the function, but the raw data is a global variable, not local 
    df=df.sort_values(["Retweets"],ascending=(False))
    top_retweets=df.head(3)
    # taking the top 3 tweets of our search, based on the number of retweets 
    
    top_tweets_by_retweets = top_retweets['Text']
    final_text.extend(top_tweets_by_retweets)
    print(f"This week, the top three tweets of our user-based search (based on number of retweets) is: \n {top_tweets_by_retweets} ")
    # we are adding the top retweets to our box of final_texts 

    top_tweets_per_location()

# 3 --- doing a full search of tweets now that you have a list of users you're comfortable with -- the instructions for a function has to come ABOVE/BEFORE the execution of a function


def full_search():
    
    global master_user_list
    global master_tweets
    # this is to indicate we want to access the global variable 
    
    for master_user in master_user_list:

        tweets = api.user_timeline(screen_name=master_user,
                                   count=10,
                                   tweet_mode = 'extended'
                                   )

        outtweets = [[info.user.screen_name, info.full_text, info.created_at, info.user.location, info.retweet_count, info.favorite_count] for info in tweets]
        master_tweets.extend(outtweets)
    
    df=pd.DataFrame(master_tweets,columns=['Username','Text','Tweet Datetime', 'Place', 'Retweets', 'Favorites'])
    
    fts = open('full_tweet_search.csv', 'w', encoding='utf-8')
    writer = csv.writer(fts) 
    writer.writerows(master_tweets) 
    fts.close()
    # will modify file at the end, but I think it helps to create the full_tweet_search in the interim so that we can open the file/look at it to input phrases as well 

    popular_rank()

# 2 ---- potentially adding new users 


def add_users(): 
    
    tweets_list2 = []
    # house tweets of new users -- making this a local variable instead of global since we won't need to reference this again
    global master_user_list
    global first_users_list
    global new_user_list 
    # we write global here to indicate we want to amend the global variables even after we leave this particular function 
    
    while True: 

        new_user = input("Are there any new users you would like to look up based on retweets? Type 'no one' if there is no one else you'd like to search tweets for at this time. ")
    
        if new_user == 'no one':
            master_user_list = first_users_list + new_user_list
            print(f"Great, these are the additional users we've added to our list of users. {new_user_list}")
            print(f"Our full list of users is now {master_user_list}.")
            full_search()
        
        else:
            
            tweets = api.user_timeline(screen_name=new_user,
                               count=10,
                               tweet_mode = 'extended'
                               )
        
        
            outtweets = [[info.user.screen_name, info.full_text, info.created_at, info.user.location, info.retweet_count, info.favorite_count] for info in tweets]
            tweets_list2.extend(outtweets)
      
            tweets_df2 = pd.DataFrame(tweets_list2, columns=['Username','Text','Tweet Datetime', 'Place', 'Retweets', 'Favorites'])
            print(tweets_df2)
        
            add_to_list = input("Do you want to add this user to our list of users to search? Type 'yes' or 'no'. ")
        
            if add_to_list == 'yes':
                new_user_list.append(new_user)
            else: 
                del tweets_list2[-1]
                #   tweets_list2 is the raw data form 

# 1 --------------

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def intro():

    tweets_list1 = []

    for user in first_users_list: 
        tweets = api.user_timeline(screen_name=user,
                               count=10,
                               tweet_mode = 'extended'
                               # find the correct syntax to eliminate @replies as well -- is there a way to filter out replies, but not mentions? 
                               # a reply feels like it would have less high quality content, a mention might still be a good way to find new twitter users 
                               )
           
        outtweets = [[info.user.screen_name, info.full_text, info.created_at, info.user.location, info.retweet_count, info.favorite_count] for info in tweets]
        tweets_list1.extend(outtweets)
        
    tweets_df1 = pd.DataFrame(tweets_list1, columns=['Username','Text','Tweet Datetime', 'Place', 'Retweets', 'Favorites'])
    print(tweets_df1)

    f = open('tweets_and_retweets.csv', 'w', encoding='utf-8')
    writer = csv.writer(f) 
    writer.writerows(tweets_list1) 
    f.close()
    
    add_users()
    # move onto step 2 
 
intro() # let's kick it off 

# some other ideas
    # can we search the biggest retweeters of a specific user? ex. find the twitter user that most often retweet Dalai Lama, that way you can find important, but less known users 
    