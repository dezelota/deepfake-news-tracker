#now to summarize. I am using a claude api key. 
#Later maybe I can add options for what LLM someone wants to use

import sqlite3
import anthropic
from dotenv import load_dotenv
import os

#read the .env file which contains the api key
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY") #grabs key

#open sonnection to Claude so we can talk to it
client = anthropic.Anthropic(api_key=api_key)

#set model to use
MODEL = "claude-sonnet-4-5"

# connect to the database
db = sqlite3.connect("deepfake.db")
cursor = db.cursor()

# grab articles that have content but haven't been summarized yet
cursor.execute("SELECT id, title, content FROM articles WHERE content IS NOT NULL AND summary IS NULL")
articles = cursor.fetchall()

print(f"Found {len(articles)} articles to summarize")

# summarize each article
for article_id, title, content in articles:
    print(f"Summarizing: {title[:60]}...")

    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Summarize this news article in 2-3 sentences. Reply with just the summary, no intro phrase:\n\n{content}"
        }]
    )

    summary = message.content[0].text

    cursor.execute(
        "UPDATE articles SET summary = ? WHERE id = ?",
        (summary, article_id)
    )
    db.commit()
    print(f"Done!")

db.close()
print("All articles summarized!")