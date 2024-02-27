# ------ Converting_blob_to_text.py ---------

import sqlite3
import base64

# Set up SQLite connection and cursor
conn = sqlite3.connect('your_database.db')  # Replace 'your_database.db' with your actual database file
cursor = conn.cursor()


def create_database():
    cursor.execute("CREATE VIRTUAL TABLE PROJECT using FTS4 (binput BLOB,input text)")
    conn.commit()
    conn.close()


def convert_blob_to_text(blob_data):
    # Decode the blob data using base64
    decoded_data = base64.b64decode(blob_data)
    # Convert bytes to string
    text_data = decoded_data.decode('utf-8')
    return text_data

def fetch_data_from_database():
    try:
        # Execute a SELECT query to get the blob data
        cursor.execute("SELECT binput,input FROM PROJECT WHERE input = "?", ('ia_01.jpg',)");
        result = cursor.fetchone()

        if result:
            blob_data = result[0]
            image_data = convert_blob_to_text(blob_data)
            return image_data
        else:
            print("No data found.")
            return None
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None

if __name__ == "__main__":
    # Fetch and print the text data
    text_data = fetch_data_from_database()
    if text_data:
        print("Converted Text Data:")
        print(text_data)

    # Close the connection
    conn.close()