import sqlite3
import feedparser
from newspaper import Article


####################################################
#step 1: open/create the database file where I shall store the articles we grab
####################################################

db_connection = sqlite3.connect("deepfake.db")
cursor = db_connection.cursor()

#CREATE TABLE IF NOT EXISTS articles: make a table called articles, but only if it doesn't already exist
#id INTEGER PRIMARY KEY: every row gets a unique number automatically
#url TEXT UNIQUE: store the url, and don't allow duplicates
#title TEXT: store the title
#source TEXT: where it came from
#published TEXT: when it was published
#summary TEXT: the LLM summary (empty for now)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id        INTEGER PRIMARY KEY,
        url       TEXT UNIQUE,
        title     TEXT,
        source    TEXT,
        published TEXT,
        content   TEXT,
        summary   TEXT,
        tags      TEXT
    )
""")

db_connection.commit() #saves changes

print("database created :)")

####################################################
#step 2: fetch articles using from RSS 
####################################################

feeds = {
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/technology-lab",
    "Hacker News": "https://hnrss.org/newest?q=deepfake",
    "NYT Technology": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.rss",
}

keywords = ["deepfake", "synthetic media", "AI-generated"]

matched_articles = []

for source, url in feeds.items():
    feed = feedparser.parse(url)
    for entry in feed.entries:
        if any(keyword.lower() in entry.title.lower() for keyword in keywords):
            matched_articles.append((entry, source))
print(f"Found {len(matched_articles)} articles")

####################################################
#step 3: save the articles to the database
####################################################
for post, source in matched_articles:
    # try to scrape the full article text
    try:
        article = Article(post.link)
        article.download()
        article.parse()
        content = article.text
    except Exception as e:
        print(f"Could not scrape {post.link}: {e}")
        content = None

    cursor.execute("""
        INSERT OR IGNORE INTO articles (url, title, source, published, content)
        VALUES (?, ?, ?, ?, ?)
    """, (
        post.link,
        post.title,
        source,
        post.published if hasattr(post, "published") else None,
        content
    ))

db_connection.commit()
db_connection.close()

print(f"Done! Saved articles to deepfake.db")
