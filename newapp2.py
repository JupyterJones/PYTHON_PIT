import os
import uuid
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
DB_FILE_PATH = 'database.db'

def insert_text_file(db_path, filename, content):
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

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('index_insert'))

@app.route('/insert_data', methods=['POST'])
def insert_data():
    if 'code' in request.form:  # Insert from textarea
        code_content = request.form['code']
        filename = str(uuid.uuid4()) + '.txt'
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code_content)
        insert_text_file(DB_FILE_PATH, filename, code_content)
    return redirect(url_for('index_insert'))

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' in request.files:  # Insert from file
        code_file = request.files['file']
        if code_file.filename != '':
            code_content = code_file.read().decode('utf-8')
            filename = str(uuid.uuid4()) + '.txt'
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code_content)
            return redirect(url_for('preview_file', filename=filename))
    return redirect(url_for('index_insert'))

@app.route('/index_insert', methods=['GET'])
def index_insert():
    return render_template('index_insert.html')

@app.route('/preview_file/<filename>', methods=['GET'])
def preview_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        code_content = f.read()
    return render_template('preview_file.html', code_content=code_content)

if __name__ == '__main__':
    app.run(debug=True)
