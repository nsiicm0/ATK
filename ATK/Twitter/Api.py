import os
import tweepy
from ATK.lib import Base
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Tweet():
    # TODO: remove and replace with Tweepy model
    name: str
    handle: str
    text: str
    date: str

class TwitterApi(Base.Base):

    def __init__(self) -> None:
        self.api_key = os.environ.get('TWITTER_API_KEY')
        self.api_secret = os.environ.get('TWITTER_API_SECRET')
        self.api_bearer = os.environ.get('TWITTER_API_BEARER')
        self.log_as.info(f'Got Key {self.api_key}')

    #def get_tweets(self) -> List[tweepy.models.Status]:
    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def get_tweets(self, query:str, n:int=1, **kwargs) -> List[Dict]:
        # TODO: Change return type to Status model
        tweets = list()
        for i in range(n):
            tweets.append(Tweet(name=f'Test {str(i)}', handle=f'test_{str(i)}', text=f'Lorem ipsum {str(i)}', date='2020-05-29 20:00:00'))
        return [dict({'query':query, 'content':tweets})] # TODO: Make sure list will be returned (for each topic one dict)
