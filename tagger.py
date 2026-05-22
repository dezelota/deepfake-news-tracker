import sqlite3
import ollama

# connect to the database
db = sqlite3.connect("deepfake.db")
cursor = db.cursor()

# grab articles that have summaries but haven't been tagged yet
cursor.execute("SELECT id, title, summary FROM articles WHERE summary IS NOT NULL AND tags IS NULL")
articles = cursor.fetchall()

print(f"Found {len(articles)} articles to tag")

# fixed tag options
TAGS = [
    "politics & policy",
    "technology",
    "crime & scams",
    "education",
    "entertainment",
    "privacy & consent"
]

for article_id, title, summary in articles:
    print(f"Tagging: {title[:60]}...")

    response = ollama.chat(
        model="llama3.2",
        messages=[{
            "role": "user",
            "content": f"""Choose the most relevant tag for this article from the list below.
Reply with just the tag, nothing else.

Tags: {", ".join(TAGS)}

Title: {title}
Summary: {summary}"""
        }]
    )

    tag = response["message"]["content"].strip()

    # save tag to database
    cursor.execute(
        "UPDATE articles SET tags = ? WHERE id = ?",
        (tag, article_id)
    )
    db.commit()
    print(f"Tagged as: {tag}")

db.close()
print("All articles tagged!")