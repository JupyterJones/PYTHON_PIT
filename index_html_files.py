import os
import shutil

# Define source and destination directories
source_dir = 'CHATGPT/html'
destination_dir = 'templates'  # Or 'static/html' if you prefer

# Ensure destination directory exists
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Copy HTML files from source directory to destination directory
html_files = [file for file in os.listdir(source_dir) if file.endswith('.html')]
for html_file in html_files:
    shutil.copy(os.path.join(source_dir, html_file), os.path.join(destination_dir, html_file))

# Generate index.html file
index_file_path = os.path.join(destination_dir, 'index.html')
with open(index_file_path, 'w') as index_file:
    index_file.write('<!DOCTYPE html>\n')
    index_file.write('<html lang="en">\n')
    index_file.write('<head>\n')
    index_file.write('<meta charset="UTF-8">\n')
    index_file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
    index_file.write('<title>HTML File Index</title>\n')
    index_file.write('</head>\n')
    index_file.write('<body>\n')
    index_file.write('<h1>HTML File Index</h1>\n')
    index_file.write('<ul>\n')
    for html_file in html_files:
        index_file.write(f'<li><a href="{html_file}">{html_file}</a></li>\n')
    index_file.write('</ul>\n')
    index_file.write('</body>\n')
    index_file.write('</html>\n')

print("Index.html file and HTML files copied successfully.")
