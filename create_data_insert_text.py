#!/home/jack/miniconda3/envs/cloned_base/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import os

def create_database(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS text_files
                 (id INTEGER PRIMARY KEY, filename TEXT, filepath TEXT, content TEXT)''')
    conn.commit()
    conn.close()

def insert_text_files(db_file, files):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    for filepath in files:
        try:
            with open("CHATGPT/text/"+filepath, 'r', encoding='utf-8') as text_file:
                content = text_file.read()
                filename = os.path.basename(filepath)
                c.execute("INSERT INTO text_files (filename, filepath, content) VALUES (?, ?, ?)", (filename, filepath, content))
        except (UnicodeDecodeError, FileNotFoundError) as e:
            print(f"Error processing file {filepath}: {e}")
    conn.commit()
    conn.close()

# Read the list of files from all_files.txt
with open("text_files.txt", "r") as file:
    all_files = file.read().splitlines()

# Define the SQLite database file
db_file_path = "text_files_txt.db"

# Create the database if it doesn't exist
create_database(db_file_path)

# Process files in batches and insert into the database
batch_size = 100
cnt =100
print(len(all_files))
for i in range(0, len(all_files), batch_size):
    cnt=cnt+100
    print(cnt)
    batch = all_files[i:i+batch_size]
    print(batch)
    insert_text_files(db_file_path, batch)

print("All text files have been inserted into the SQLite database.")
