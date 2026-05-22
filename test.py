import sqlite3
db = sqlite3.connect("deepfake.db")
cursor = db.cursor()
cursor.execute("SELECT title, tags FROM articles WHERE tags IS NOT NULL")
rows = cursor.fetchall()
for title, tags in rows:
    print(f"{tags:<25} {title[:60]}")
db.close()