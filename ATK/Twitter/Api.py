import os
import re
import tweepy
import preprocessor as p
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


    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def get_tweets(self, **kwargs) -> List[Dict]:
        p.set_options(p.OPT.URL, p.OPT.EMOJI)
        n_topics = kwargs['n_topics']
        n_tweets_per_topic = kwargs['n_tweets_per_topic']
        country = kwargs['country']
        trends = sorted((self.api.trends_place(country))[0]['trends'], key=lambda x: x['tweet_volume'] or 0, reverse=True) # fetch worldwide trends
        results = []
        # we will focus on trends that only contain english characters
        reg = re.compile('^[A-z0-9\.#\_]+$')
        for trend in trends[:n_topics]:
            trend_data = dict()
            if not bool(reg.match(trend['name'])):
                continue
            trend_data['query'] = trend['name']
            search_results = self.api.search(q=trend['query'], lang='en', result_type='popular', tweet_mode='extended')
            tweets = []
            for status in search_results[:n_tweets_per_topic]:
                oembed = self.api.get_oembed(id=status.id_str, hide_media=True, hide_thread=True, lang='en')
                tweets.append(Tweet(name=p.clean(status.user.name), handle=status.user.screen_name, text=p.clean(status.full_text), date=status.created_at.strftime('%b %d %Y, %I:%M:%S %p UTC'), profile_image_url=status.user.profile_image_url_https, oembed=oembed, render_path='', id=status.id_str))
            trend_data['content'] = tweets
            if len(tweets) != 0:
                results.append(trend_data)

        return results
