#!/usr/bin/env python
import twitter, twitter_config
import requests, json, re
import untangle
import youtube_search
from os import path
from datetime import datetime


cred = next(acct for acct in twitter_config.accounts if acct['username'] == 
            'UYDMusic')
last_epfile = '/home/git/pi/uydmusic/last_ep.p'

def tweet_uyd(api):
    if path.isfile(last_epfile):
        last_ep = pickle.load(last_epfile)
    else:
        last_ep = datetime.strptime('Mon, 01 Feb 2016 19:51:00 +0000', '%a, %d %b %Y %H:%M:%S +0000')

    #req = requests.get('http://uhhyeahdude.com/podcast/')
    #feed = xml.etree.ElementTree.parse(req.content).getroot()
    feed = untangle.parse('http://uhhyeahdude.com/podcast/')
    eps = feed.rss.channel.item
    new_eps = []
    for ep in eps:
        pubdate = ep.pubDate.cdata
        pubdate = datetime.strptime(pubdate, '%a, %d %b %Y %H:%M:%S +0000')
        if pubdate > last_ep:
            new_eps.append(ep)
    for ep in reversed(new_eps):
        desc = ep.description.cdata
        #words = re.findall(r'[\w]+', desc)
        desc = desc.replace('\n', ' ').replace('\t', ' ')
        words = desc.split(' ')
        if set(['intro:', 'outro:', 'http://uhhyeahdude.com']).issubset(set(words)):
            intro = ' '.join(words[words.index('intro:')+1:words.index('outro:')-1])
            intro_url = youtube_search.search(intro)
            api.PostUpdate('{0} intro: {1} {2}'.format(ep.title.cdata, intro, intro_url))
            print '{0} intro: {1} {2}'.format(ep.title.cdata, intro, intro_url)
            outro = ' '.join(words[words.index('outro:')+1:words.index('http://uhhyeahdude.com')])
            outro_url = youtube_search.search(outro)
            api.PostUpdate('{0} outro: {1} {2}'.format(ep.title.cdata, outro, outro_url))
            print '{0} outro: {1} {2}'.format(ep.title.cdata, outro, outro_url)
            
if __name__ == '__main__':
    try:
        api = twitter.Api(consumer_key=cred['consumer_key'], consumer_secret=cred['consumer_secret'],
                          access_token_key=cred['access_token_key'], access_token_secret=cred['access_token_secret'])
    except:
        print 'Failed to authenticate.'
        exit()

    tweet_uyd(api)

