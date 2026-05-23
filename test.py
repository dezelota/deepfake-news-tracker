import feedparser

feeds = [
    "https://time.com/feed/",
    "https://time.com/tag/deepfake/feed/",
]

for url in feeds:
    feed = feedparser.parse(url)
    print(f"{url}: {len(feed.entries)} entries")
    if feed.entries:
        print(f"  Sample: {feed.entries[0].title}")