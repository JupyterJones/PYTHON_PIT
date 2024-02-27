import json
import logging
import os
import glob
import subprocess

# Example usage
conversations_file_path = 'CHATGPT/conversations.json'
output_folder = 'CHATGPT/text'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)


files = glob.glob("CHATGPT/individual_sessions/*.json")

for file in files:
    file_name = file.split('/')[-1]#[-:5]+"txt"
    print(file_name)
    print("--------")
    cmd = ["python","json2text.py", file_name]
    print (cmd)
    print("--------")
    # Use subprocess.run without terminal=True
    subprocess.run(cmd)
