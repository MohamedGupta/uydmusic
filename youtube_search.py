from bs4 import BeautifulSoup
import requests, random


def search(query):
    url = "https://www.youtube.com/results?search_query=" + str(query)
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    vids = soup.findAll(attrs={'class':'yt-lockup-tile'})
    vid = vids[0]
    return 'https://www.youtube.com/watch?v=' + vid.attrs['data-context-item-id']
