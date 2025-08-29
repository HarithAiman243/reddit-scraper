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

    page_posts = []  # store this page’s posts
    for post in data['data']['children']:
        post = post['data']

        if post.get("post_hint") == "image": # Filter out by Image
            title = post['title'] # Get post title
            img = post['url'] # Get post img url
            page_posts.append({
                "post_title": title,
                "image_url": img
            })
    
    if page_posts: # Separate page.
        pages.append({
            "page": i + 1,
            "posts": page_posts
        })

    after = data['data']['after']  # update for next "page"

    print(f"Scraped page {i+1}, total collected posts so far: {sum(len(p['posts']) for p in pages)}")
    time.sleep(2)  # wait for 2 seconds (avoid rate limiting to avoid getting banned)

print("\nDone. Total collected image posts:", sum(len(p['posts']) for p in pages))