#PART 1 = preparing the enviroment
# install the TWEEPY module per TERMINAL (in windows open cmd and "pip install tweepy")
from tweepy.streaming import StreamListener #the guy who receive our data
from tweepy import OAuthHandler #the connection with Twitter
from tweepy import Stream #the data in real time
from datetime import datetime #we´ll need datetime to structure our datas
import json #json to NoSQL dbms 

# in "https://developer.twitter.com/en/apps" creat you app to get the 4 keys from API
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

#now we have to create the authentication for twitter:
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Creat a class to capture the data from Twitter:
class MyListener(StreamListener):
    def on_data(self, dados):
        tweet = json.loads(dados)
        created_at = tweet["created_at"]
        id_str = tweet["id_str"]
        text = tweet["text"]
        obj = {"created_at":created_at,"id_str":id_str,"text":text,}
        tweetind = col.insert_one(obj).inserted_id
        print (obj)
        return True

# now create the objects, ok?
mylistener = MyListener()
mystream = Stream(auth, listener = mylistener)

#PART 2 = connecting with NoSQL DBMS(MongoDB)
from pymongo import MongoClient   

client = MongoClient('localhost', 27017)
#create database to collect the tweets and the collection "col":
db = client.twitterdb
col = db.tweets 

#here you put your keywords to search:
keywords = ['Python', 'Data Mining', 'Github']

#PART 3 = collecting the tweets

# Iniciando o filtro e gravando os tweets no MongoDB
mystream.filter(track=keywords)
mystream.disconnect()
#here you can see your tweets:
col.find_one() 