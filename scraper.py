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

# save results into a JSON file & separated by page
with open("reddit_image_posts.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False, indent=2)


# Generate HTML to display posts with images
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Reddit Images</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f4f4f4; }
        .post { margin-bottom: 30px; padding: 15px; background: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .title { font-size: 18px; margin-bottom: 10px; }
        img { max-width: 500px; display: block; margin-bottom: 10px; border-radius: 6px; }
    </style>
</head>
<body>
    <h1>Reddit Posts with Images</h1>
"""
for page in pages:
    html_content += f"<h2>Page {page['page']}</h2>\n"
    for post in page["posts"]:
        html_content += f'<div class="post">\n'
        html_content += f'  <div class="title">{post["post_title"]}</div>\n'
        html_content += f'  <img src="{post["image_url"]}" alt="Image">\n'
        html_content += "</div>\n"

html_content += """
</body>
</html>
"""
# Save HTML file
with open("reddit_images_posts.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Open reddit_images_posts.html in your browser to view posts.")

