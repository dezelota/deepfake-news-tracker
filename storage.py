import sqlite3

#step 1 open/create the database file where I shall store the articles we grabbed using the other script fetcher.py
#step one should actually be learn sqlite3 but i have no timeeeee, will ask claude to give me run down 

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
CREATE TABLE IF NOT EXISTS articles(
               id INTEGER PRIMARY KEY,
               url TEXT UNIQUE,
               title TEXT,
               source TEXT,
               published TEXT,
               summary TEXT
               ) 
""")

db_connection.commit() #saves changes

print("database created :)")

db_connection.close() #closes  connection