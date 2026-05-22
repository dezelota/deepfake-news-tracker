#now to summarize. I am using ollama so we dont need to use an api key. 
#Later maybe I can add options for what LLM someone wants to use

import sqlite3
import ollama

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

    response = ollama.chat(
        model="llama3.2",
        messages=[{
            "role": "user",
            "content": f"Summarize this news article in 2-3 sentences. Reply with just the summary, no intro phrase:\n\n{content}"
        }]
    )

    summary = response["message"]["content"]

    # save summary back to the database
    cursor.execute(
        "UPDATE articles SET summary = ? WHERE id = ?",
        (summary, article_id)
    )
    db.commit()
    print(f"Done!")

db.close()
print("All articles summarized!")