import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
DB_FILE_PATH = 'database.db'

def insert_text_file(db_path, filename, directory, content):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS text_files (
                        id INTEGER PRIMARY KEY,
                        filename TEXT,
                        content TEXT
                    )''')
    cursor.execute('''INSERT INTO text_files (filename, content) VALUES (?, ?)''',
                   (filename, content))
    conn.commit()
    conn.close()

@app.route('/insert_data', methods=['POST', 'GET'])
def insert_data():
    if request.method == 'POST':
        if 'code' in request.form:  # Insert from textarea
            code_content = request.form['code']
            filename = str(uuid.uuid4()) + '.txt'
            directory = UPLOAD_FOLDER
            file_path = os.path.join(directory, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code_content)
            insert_text_file(DB_FILE_PATH, filename, directory, code_content)
            return redirect(url_for('index'))
        elif 'file' in request.files:  # Insert from file
            code_file = request.files['file']
            if code_file.filename != '':
                code_content = code_file.read().decode('utf-8')
                return render_template('insert_from_file.html', code_content=code_content)
    return render_template('index_insert.html')

@app.route('/save_from_file', methods=['POST'])
def save_from_file():
    code_content = request.form['code']
    filename = str(uuid.uuid4()) + '.txt'
    directory = UPLOAD_FOLDER
    file_path = os.path.join(directory, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code_content)
    insert_text_file(DB_FILE_PATH, filename, directory, code_content)
    return redirect(url_for('index'))

@app.route('/')
def index():
     return render_template('index_insert.html')

if __name__ == '__main__':
    app.run(debug=True)
