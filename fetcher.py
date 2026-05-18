#oki so he wants me to grab the articles. store them in an sqlite db (never used need to learn D:) make sure theyre not duplicated and then summarize using an llm
#first i need to grab the articles. claude reccomended requests
#jk wasnt working we try feedparser now and we try BBC, Wired, or Reuters

import feedparser

url = "https://news.google.com/rss/search?q=deepfake&hl=en-US&gl=US&ceid=US:en"

feed = feedparser.parse(url)

keywords = ["deepfake"]

matched_articles = []

for entry in feed.entries:
    # Check if any keyword is in the title (case-insensitive)
    if any(keyword.lower() in entry.title.lower() for keyword in keywords):
        matched_articles.append(entry)




for post in matched_articles:
    print(f"Title: {post.title}\n Link: {post.link}\n")