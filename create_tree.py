import json
import logging
import os
import glob
import subprocess
def split_and_save_conversations(conversations_file, output_folder):
    try:
        with open(conversations_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            for conversation in data:
                title = conversation.get('title', 'Unknown_Title')
                title_with_underscores = title.replace(' ', '_')
                title_with_underscores = title_with_underscores.replace(':','_')
                title_with_underscores = title_with_underscores.replace("'","_")
                title_with_underscores = title_with_underscores.replace("&","_")
                title_with_underscores = title_with_underscores.replace("*","_")
                title_with_underscores = title_with_underscores.replace("(","_")
                title_with_underscores = title_with_underscores.replace(")","_")
                chapter_filename = f"{title_with_underscores}.json"
                chapter_filepath = os.path.join(output_folder, chapter_filename)
                
                logging.info(f"Saving data for conversation '{title}' to {chapter_filepath}")
                
                with open(chapter_filepath, 'w', encoding='utf-8') as chapter_file:
                    json.dump([conversation], chapter_file, indent=2)

    except FileNotFoundError:
        logging.error(f"File not found: {conversations_file}")
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON in file: {conversations_file}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

# Example usage
conversations_file_path = 'CHATGPT/conversations.json'
output_folder = 'CHATGPT/individual_sessions'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Call the split and save function
split_and_save_conversations(conversations_file_path, output_folder)
files = glob.glob("CHATGPT/individual_sessions/*.json")

for file in files:
    file_name = file.split('/')[-1]
    print(file_name)
    cmd = ["./json2html.py", file_name]
    print (cmd)
    # Use subprocess.run without terminal=True
    subprocess.run(cmd)
# Example usage
conversations_file_path = 'CHATGPT/conversations.json'
output_folder = 'CHATGPT/text'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)


files = glob.glob("CHATGPT/individual_sessions/*.json")

for file in files:
    file_name = file.split('/')[-1]#[-:5]+".txt"
    print(file_name)
    print("--------")
    cmd = ["python","json2text.py", file_name]
    print (cmd)
    print("--------")
    # Use subprocess.run without terminal=True
    subprocess.run(cmd)
