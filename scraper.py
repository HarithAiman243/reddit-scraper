import requests
import time
import json

headers = {'User-agent': 'Mozilla/5.0'}
url = "https://www.reddit.com/r/malaysia/top.json?t=week"  # Filter by Top Post, Week
