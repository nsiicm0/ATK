import os
import re
import tweepy
import codecs
from ATK.lib import Base
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Tweet():
    name: str
    handle: str
    text: str
    date: str
    profile_image_url: str
    oembed: Dict
    render_path: str
    id: str

class TwitterApi(Base.Base):

    def __init__(self) -> None:
        self.api_key = os.environ.get('TWITTER_API_KEY')
        self.api_secret = os.environ.get('TWITTER_API_SECRET')
        self.api_bearer = os.environ.get('TWITTER_API_BEARER')
        self.auth = tweepy.AppAuthHandler(self.api_key, self.api_secret)
        self.api = tweepy.API(self.auth)

    #def get_tweets(self) -> List[tweepy.models.Status]:
    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def get_tweets(self, **kwargs) -> List[Dict]:
        n_topics = kwargs['n_topics']
        n_tweets_per_topic = kwargs['n_tweets_per_topic']
        country = kwargs['country']
        trends = sorted((self.api.trends_place(country))[0]['trends'], key=lambda x: x['tweet_volume'] or 0, reverse=True) # fetch worldwide trends
        results = []
        # we will focus on trends that only contain english characters
        reg = re.compile('^[A-z0-9\.#\_]+$')
        for i, trend in enumerate(trends):
            # TODO: For some reason it prematurely stops
            # TODO: Clean tweets from URLs and hashtags
            if i >= n_topics:
                break
            trend_data = dict()
            if not bool(reg.match(trend['name'])):
                continue
            trend_data['query'] = trend['name']
            search_results = self.api.search(q=trend['query'], lang='en', result_type='popular')
            tweets = []
            for j, status in enumerate(search_results):
                if j >= n_tweets_per_topic:
                    break
                # get oembed info
                oembed = self.api.get_oembed(id=status.id_str, hide_media=True, hide_thread=True, lang='en')
                tweets.append(Tweet(name=status.user.name, handle=status.user.screen_name, text=status.text, date=status.created_at.strftime('%b %d %Y, %I:%M:%S %p UTC'), profile_image_url=status.user.profile_image_url_https, oembed=oembed, render_path='', id=status.id_str))
            trend_data['content'] = tweets
            results.append(trend_data)

        return results
