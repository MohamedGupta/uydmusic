#!/usr/bin/env python
import twitter, twitter_config
import untangle
import youtube_search
from os import path
from datetime import datetime


cred = twitter_config.accounts['UYDMusic']
last_epfile = '/home/pi/git/uydmusic/last_ep.date'

def tweet_uyd(api):
    if path.isfile(last_epfile):
        last_ep = datetime.strptime(open(last_epfile, 'r').read(), '%a, %d %b %Y %H:%M:%S +0000')
    else:
        last_ep = datetime.strptime('Fri, 15 Jul 2016 19:51:00 +0000', '%a, %d %b %Y %H:%M:%S +0000')

    #req = requests.get('http://uhhyeahdude.com/podcast/')
    #feed = xml.etree.ElementTree.parse(req.content).getroot()
    feed = untangle.parse('http://uhhyeahdude.com/podcast/')
    eps = feed.rss.channel.item
    new_eps = []
    for ep in eps:
        pubdate = datetime.strptime(ep.pubDate.cdata, '%a, %d %b %Y %H:%M:%S +0000')
        if pubdate > last_ep:
            new_eps.append(ep)
            last_ep = pubdate

    if new_eps == []:
        #print 'No new eps'
        return

    #pickle.dump(last_ep, open(last_epfile, 'w'))
    open(last_epfile, 'w').write(last_ep.strftime('%a, %d %b %Y %H:%M:%S +0000'))
    for ep in reversed(new_eps):
        desc = ep.description.cdata
        desc = desc.replace('\n', ' ').replace('\t', ' ')
        words = desc.split(' ')
        if set(['intro:', 'outro:', 'http://uhhyeahdude.com']).issubset(set(words)):
            intro = ' '.join(words[words.index('intro:')+1:words.index('outro:')-1])
            intro_url = youtube_search.search(intro)
            api.PostUpdate('{0} intro: {1} {2}'.format(ep.title.cdata, intro, intro_url))
            outro = ' '.join(words[words.index('outro:')+1:words.index('http://uhhyeahdude.com')])
            outro_url = youtube_search.search(outro)
            api.PostUpdate('{0} outro: {1} {2}'.format(ep.title.cdata, outro, outro_url))
            #print 'Posting {0}'.format(ep.pubDate.cdata)
            
if __name__ == '__main__':
    try:
        api = twitter.Api(consumer_key=cred['consumer_key'], consumer_secret=cred['consumer_secret'],
                          access_token_key=cred['access_token_key'], access_token_secret=cred['access_token_secret'])
    except:
        print 'Failed to authenticate.'
        exit()

    tweet_uyd(api)

