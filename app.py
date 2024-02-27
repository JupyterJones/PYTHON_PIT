from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from icecream import ic
import os
import datetime
from flask import request
import uuid
from flask import request, render_template
import uuid
import os
import shutil
import sys
import subprocess
#app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
#https://www.youtube.com/watch?v=mwzlySJJJQQvs
#https://www.youtube.com/watch?v=04HykJ0XfEA
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#db_file_path = "/home/jack/Desktop/test/conversations.db"
#db_file_path = "text_files_txt.db"
db_file_path='PYTHON_PIT.db'
DB_FILE_PATH=db_file_path
app.config['DB_FILE_PATH'] = DB_FILE_PATH
PYTHON_CODE = 'static/python'
app.config['PYTHON_CODE'] = PYTHON_CODE

debug_directory = "static/Logs"
if not os.path.exists(debug_directory):
    # If it doesn't exist, create it
    os.mkdir(debug_directory)
    print(f"The '{debug_directory}' directory has been created.")
else:
    print(f"The '{debug_directory}' directory already exists.")

def logit(argvs):
    argv = argvs   
    log_file = debug_directory+"/app_log.txt"  # Replace with the actual path to your log file
    timestamp = datetime.datetime.now().strftime("%A_%b-%d-%Y_%H-%M-%S")
    with open(log_file, "a") as log:
        log.write(f"{timestamp}: {argv}\n")

logit("This is a DEBUG message")

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect(db_file_path)
    conn.row_factory = sqlite3.Row
    return conn

#link to index
@app.route('/') 
def index():
    return render_template('index_insert.html')    

@app.route('/view_html_directory') 
def view_html_directory():
    return render_template('index.html')    


@app.route('/index_insert', methods=['GET'])
def index_insert():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, content FROM text_files where rowid = ?", (1,))
    rows = cursor.fetchall()
    results = [{'rowid': row[0], 'text': row[1]} for row in rows]
    conn.close()
    logit(rows)
    return render_template('index_insert.html',results = results , rowid = 1)

# Route to display the query form and results
@app.route('/query_form', methods=['GET', 'POST'])
def query_form():
    if request.method == 'POST':
        # Get the user query from the form
        query = request.form['query']
        # Execute the query and fetch results
        conn = get_db_connection()
        cursor = conn.cursor()
        logit(query)

        cursor.execute("SELECT rowid, content FROM text_files WHERE content LIKE ? LIMIT 2", ('%' + query + '%',))

        rows = cursor.fetchall()

        # Decode byte strings into readable text and include row IDs
        #results = [{'rowid': row[0], 'text': row[1].decode('utf-8')} for row in rows]
        results = [{'rowid': row[0], 'text': row[1]} for row in rows]       

        conn.close()
        logit(results)
        return render_template('query_result.html', query=query, results=results)
    return render_template('query_form.html')

# Route to edit and save data
# Route to edit and save data
@app.route('/edit', methods=['GET'])
def edit_row():
    rowid = request.args.get('rowid')
    if rowid:
        return redirect(url_for('edit_data', rowid=rowid))
    else:
        # Handle the case when no row ID is provided
        return "Please enter a valid Row ID"

@app.route('/edit/<int:rowid>', methods=['GET', 'POST'])
def edit_data(rowid):
    if request.method == 'POST':
        # Get the edited data from the form
        edited_text = request.form['edited_text']
        # Update the database with the edited data
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE text_files SET content = ? WHERE rowid = ?", (edited_text, rowid))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        # Fetch the data to edit based on rowid
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM text_files WHERE rowid = ?", (rowid,))
        data = cursor.fetchone()
        conn.close()
        return render_template('edit_text.html', rowid=rowid, data=data['content'])

# Route to delete data
@app.route('/delete', methods=['GET', 'POST'])
def delete_row():
    rowid = None  # Default value for rowid
    if request.method == 'POST':
        rowid = request.form.get('rowid')
        if rowid:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM text_files WHERE rowid = ?", (rowid,))
            conn.commit()
            conn.close()
            return redirect('/')
    return render_template('delete.html', rowid=rowid)


@app.route('/insert_data', methods=['POST', 'GET'])
def insert_data():
    if request.method == 'POST':
        code_content = None
        # Check if the textarea is filled
        if 'code' in request.form:
            code_content = request.form['code']
        # Check if a file is uploaded
        elif 'code_file' in request.files:
            code_file = request.files['code_file']
            if code_file.filename != '':
                code_content = code_file.read().decode('utf-8')
        # If neither textarea nor file is provided
        if code_content is None:
            return 'Error: No code provided'
        filename = str(uuid.uuid4()) + '.txt'  # Generate UUID as filename
        directory = UPLOAD_FOLDER
        file_path = os.path.join(directory, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code_content)
        insert_text_file(DB_FILE_PATH, filename, directory, code_content)
        return redirect(url_for('index'))
    return render_template('index.html')  # Properly close the render_template function call


@app.route('/search_text_files', methods=['GET'])
def search_text_files():
    search_terms = request.args.get('search_terms', '')  # Get search terms from query parameter
    if search_terms:
        conn = sqlite3.connect(DB_FILE_PATH)
        c = conn.cursor()

        # Split search terms into individual words
        search_words = search_terms.split()

        query = "SELECT * FROM text_files WHERE "
        conditions = []
        for word in search_words:
            conditions.append("content LIKE ?")
        query += " AND ".join(conditions)
        query += " LIMIT 4"

        # Now execute the query with the proper placeholders
        # Make sure to adjust this according to your database library
        c.execute(query, ['%' + word + '%' for word in search_words])

        results = c.fetchall()

        conn.close()
        return render_template('search_text_files.html', results=results)
    else:
        return render_template('search_text_files.html', results=[])
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
directory = UPLOAD_FOLDER
def insert_text_file(db_path, filename, directory, content):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS text_files
                 (id INTEGER PRIMARY KEY, filename TEXT, filepath TEXT, content TEXT)''')   
    cursor.execute('''INSERT INTO text_files (filename, filepath, content) VALUES (?, ?, ?)''',
                   (filename, UPLOAD_FOLDER, content))
    conn.commit()
    conn.close()
@app.route('/preview_file/<filename>', methods=['GET'])
def preview_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        code_content = f.read()
    return render_template('preview_file.html', code_content=code_content)








@app.route('/upload_python', methods=['POST'])
def upload_python():
    if 'file' in request.files:  # Insert from file
        code_file = request.files['file']
        if code_file.filename != '':
            code_content = code_file.read().decode('utf-8')
            filename = str(uuid.uuid4()) + '.py'
            file_path = os.path.join(PYTHON_CODE, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code_content)
        return redirect(url_for('preview_python', filename=filename))
    return redirect(url_for('index_insert'))
#directory = UPLOAD_FOLDER
def insert_text_file(db_path, filename, directory, content):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS text_files
                 (id INTEGER PRIMARY KEY, filename TEXT, filepath TEXT, content TEXT)''')   
    cursor.execute('''INSERT INTO text_files (filename, filepath, content) VALUES (?, ?, ?)''',
           (filename, PYTHON_CODE, content))
    conn.commit()
    conn.close()
@app.route('/preview_python/<filename>', methods=['GET'])
def preview_python(filename):
    file_path = os.path.join(PYTHON_CODE, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        code_content = f.read()
    return render_template('preview_python.html', code_content=code_content)














@app.route('/last_row_inserted')
def last_row_inserted():
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, content FROM text_files ORDER BY rowid DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        rowid, content = row
        return render_template('last_row_inserted.html', rowid=rowid, content=content)
    else:
        return "No rows found in the database."
# Function to fetch records from the database

@app.route('/runcode')
def run_code():
    try:
        # Run the script using subprocess and capture the output
        result = subprocess.run(["python", "static/python/spiderweb.py"], capture_output=True, text=True)
        app.logger.info("Script executed successfully")
        return render_template('test_code.html', output=result.stdout)
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Error running script: {e}")
        return render_template('error.html', error=str(e))




# Adjust the fetch_records function to fetch filename along with the content
def fetch_records(page_num, page_size):
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    offset = (page_num - 1) * page_size
    cursor.execute("SELECT filename, content FROM text_files LIMIT ? OFFSET ?", (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# Route to serve the HTML page and handle pagination
@app.route('/view_all')
def view_all():
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    
    # Fetch paginated records from the database
    page_records = fetch_records(page, size)
    
    # Calculate total number of pages
    total_pages = calculate_total_pages(size)
    
    return render_template('view_all.html', records=page_records, total_pages=total_pages, current_page=page, page_size=size)

# Route to view content based on filename
@app.route('/view_content/<filename>')
def view_content(filename):
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ROWID,content FROM text_files WHERE filename=?", (filename,))
    row = cursor.fetchone()
    rowid = row[0]  # Extract the ROWID from the row
    content = row[1]  # Extract the content from the row
    cursor.close()
    conn.close()
    return render_template('previewfile.html', code_content=content, rowid=rowid)



def calculate_total_pages(page_size):
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM text_files")
    total_records = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return (total_records + page_size - 1) // page_size

@app.route('/view_youtube')
def view_youtube():
    return render_template('view_youtube.html')

@app.route('/create_pyfile')
def create_pyfile():
    return render_template('create_pyfile.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)