#!/usr/bin/env python
# coding: utf-8

# # Social Web -  Twitter
# 
# Twitter implements OAuth 1.0A as its standard authentication mechanism, and in order to use it to make requests to Twitter's API, you'll need to go to https://dev.twitter.com/apps and create a sample application. 
# 
# Twitter examples from the python-twitter API  [https://github.com/ideoforms/python-twitter-examples](https://github.com/ideoforms/python-twitter-examples)  

# ## Authorizing an application to access Twitter account data

# In[17]:


import pandas as pd
import twitter # pip install twitter

# Go to http://dev.twitter.com/apps/new to create an app and get values
# for these credentials, which you'll need to provide in place of these
# empty string values that are defined as placeholders.
# See https://dev.twitter.com/docs/auth/oauth for more information 
# on Twitter's OAuth implementation.

CONSUMER_KEY = 'OEI2FGg6CmqvegsnMfLrj2oNf'
CONSUMER_SECRET = '9TQcPiWBVFUCKtCFIuXd25GKiI270dPxppC8oI5jN0GlewKeI8'
OAUTH_TOKEN = '104745048-sD2ixBTZYgYnd0amOqQKZmkTv7cybefY44bAnnkI'
OAUTH_TOKEN_SECRET = '3Eq217JOxKUmBl233fZjjyRdCLrmvWQWz2P5xh1EheYdb'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

# Nothing to see by displaying twitter_api except that it's now a
# defined variable

print(twitter_api)



# In[20]:


from requests import get
from bs4 import BeautifulSoup as bs

url = "https://www.imdb.com/search/title?title_type=tv_series"

response = get(url)
response

html_soup = bs(response.text,'html.parser')
type(html_soup)


id_check = html_soup.find(id ="main")
tv_show_container = id_check.find_all(class_ ="lister-item mode-advanced")
len(tv_show_container)

container = tv_show_container[0]
print(container)

#list to store scraped value data in:
tv_show_names = []


for container in tv_show_container:
    
    if container.find("div", class_ = "ratings-bar") is not None:
        
        name = container.h3.a.text
        tv_show_names.append(name)

TVShowDF = pd.DataFrame({"tv_show_names":tv_show_names})


# In[27]:


#Create a new column called "hashtag" in the dataframe and remove all spaces
TVShowDF['hashtag'] = TVShowDF.tv_show_names.str.replace(' ','')
#Remove non alphabetic characters
TVShowDF['hashtag'] = TVShowDF.hashtag.str.replace('[^a-zA-Z]', '')
#Prefix "#" symbol to all the values in the hashtag column
TVShowDF['hashtag'] = '#'+TVShowDF.hashtag
TVShowDF.hashtag

# In[41]:
n = 5000
from urllib.parse import unquote
# See https://dev.twitter.com/rest/reference/get/search/tweets
tweet_results = []

for row in TVShowDF.index:
    tweet_results.append(twitter_api.search.tweets(q=TVShowDF.hashtag[row], count=n, lang='en'))
print(tweet_results[0])


# In[41]:
def GetTweetFields(tr):
    return {"text": tr["text"]
            , "created_at": tr["created_at"]
            , "favourites_count" :  tr["user"]["favourites_count"]
            }
alltweets = [[GetTweetFields(ttrr) for ttrr in tr["statuses"]] for tr in tweet_results]
print(alltweets[11])
df = pd.DataFrame([item for sublist in alltweets for item in sublist],columns=['text','created_date','favourites_count'])

#export the dataframe to csv
df.to_csv('tweets.csv')