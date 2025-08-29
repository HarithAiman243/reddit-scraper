import requests
import time
import json

headers = {'User-agent': 'Mozilla/5.0'}
url = "https://www.reddit.com/r/malaysia/top.json?t=week"  # Filter by Top Post, Week

pages = []  # list of pages, each page is a list of posts
after = None

for i in range(10):  # simulate 10 pages
    params = {
        'after': after,
        'limit': 25   # fetch 25 posts per request
    }
    res = requests.get(url, headers=headers, params=params)
    data = res.json()