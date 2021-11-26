import tweepy
import csv
import ssl
import pandas as pd 
import numpy as np
import re  
import nltk
from nltk.corpus import stopwords
import spacy
# come back to this and use nlp 
nlp = spacy.load('en_core_web_sm')

consumer_key = " "
consumer_secret = " "
access_token = " " 
access_token_secret = " " 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

screen_name = 'HEB'

# here we're extracting the last 10 tweets, tweets itself is a list of all the tweets -- it contains a ton of raw information in it 

tweets = api.user_timeline(screen_name=screen_name,
                           count=2,
                           include_rts = False, 
                           # necessary to keep full_text, otherwise only first 140 words extracted
                           tweet_mode = 'extended'
                           )
                           
# now we want to populate a 2-D array, start by looking for only the text and the user 

outtweets = [[info.full_text] for info in tweets] # this will give you an array of the tweet itself only 

#df = pd.DataFrame(t.__dict__ for t in tweets) # this will give you all of the information about the tweet, in text form -- not exactly what we're looking for

word_box = []

for outtweet in outtweets:
    # this is one of tweets, it's a list
    for words in outtweet:
        # now we're splitting the individual into the strings 
        list_of_words = words.split()
        word_box.extend(list_of_words)
        # replaced append with extend becaues we wanted to add to one existing list, not to add multiple lists of words 


# print(word_box)
# this is a list of all the words pulled from multiple tweets 

lines = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in word_box] 
# syntax of re.sub(pattern, replacement, original_string)
# here we're removing any extra punctuation like @ # etc. 

# print(lines)
# if you printed lines, it would be a list of words after you've removed extra punctuation 

lines_2 = []

for word_2 in lines:
    if word_2 not in nlp.Defaults.stop_words:
        # removing stop words to further clean the list of words 
        lines_2.append(word_2)

#print(lines_2)
# this is a list of words without stop words 

df = pd.DataFrame(lines_2)
#create a dataframe of the clean list of words 
#print(df)

df = df[0].value_counts()
# this counts the number of instances that the item in column [0] apperas 
print(df)

# ------------- later on, de-bug below for numeric array of the word count  

#from nltk.probability import FreqDist

#freqdoctor = FreqDist()

#for words in df:
    #freqdoctor[words] += 1 
    # this didn't work out but I think it's supposed to return the information in numeric form like this
    # FreqDist ({1: 952, 2: 359, 3: 145, 4: 93, 5: 70, 6: 54, 7: 27, 8: 22})
    
#-------------- 

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = df[:20,]
# this truncated the results to the top 20 words 
print(df)

plt.figure(figsize=(10,5))
x = df.values
y = df.index
sns.barplot(x=x, y=y, alpha=0.8)

plt.title('Top words overall')
plt.ylabel('Word from tweet',fontsize=12)
plt.xlabel('Count of words', fontsize=12)
plt.show()

# ----------------


# this is a natural language processing section that recognizes entities you can read more about 
# https://github.com/AlexTheAnalyst/PythonCode/blob/master/Twitter%20Scraper%20V8.ipynb
# in it, you can also scrub for entites/organizations, but for purposes of our exercise, we'll stick to top words and users for now 



           