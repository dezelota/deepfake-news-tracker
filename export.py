import sqlite3
import csv

# connect to the database
db = sqlite3.connect("deepfake.db")
cursor = db.cursor()

# grab everything
cursor.execute("SELECT title, source, published, summary, tags, url FROM articles")
rows = cursor.fetchall()

# write to csv
with open("articles.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    # header row
    writer.writerow(["title", "source", "published", "summary", "tags", "url"])
    
    # data rows
    writer.writerows(rows)

db.close()
print(f"Exported {len(rows)} articles to articles.csv")