#!/home/jack/miniconda3/envs/cloned_base/bin/python
import json
import logging
from sys import argv

# Configure logging
logging.basicConfig(filename='conversion_log.txt', level=logging.DEBUG)

# Load the JSON data from the uploaded file
#DIR = "CHATDPT/individual_sessions/"
file_name = argv[1]
#Filename = DIR + file_name
Filename=file_name
logging.info(f"Processing file: {Filename}")

try:
    with open(Filename, 'r') as file:
        json_data = json.load(file)
except Exception as e:
    logging.error(f"Error loading JSON file: {e}")
    raise

# Initialize the result string
result_str = ""

# Define a function to get conversation messages similar to the JavaScript logic
def get_conversation_messages(conversation):
    messages = []
    current_node = conversation.get('current_node')
    while current_node:
        node = conversation['mapping'][current_node]
        message = node.get('message')
        if (message and message.get('content') and message['content'].get('content_type') == 'text' and
            len(message['content'].get('parts', [])) > 0 and len(message['content']['parts'][0]) > 0 and
                (message['author']['role'] != 'system' or message.get('metadata', {}).get('is_user_system_message'))):
            author = message['author']['role']
            if author == 'assistant':
                author = 'ChatGPT'
            elif author == 'system' and message['metadata'].get('is_user_system_message'):
                author = 'Custom user info'
            messages.append({'author': author, 'text': message['content']['parts'][0]})
        current_node = node.get('parent')
    return messages[::-1]  # Reverse the list to maintain chronological order

# Iterate over each conversation in the JSON data and process it
for conversation in json_data:
    # Get the conversation title and messages
    title = conversation.get('title', '')
    messages = get_conversation_messages(conversation)

    # Append the title and messages to the result string
    result_str += title + '\n'
    for message in messages:
        result_str += message['author'] + '\n' + message['text'] + '\n'
    result_str += '\n'  # Add a newline between conversations

# Return the processed result string
logging.info("Conversion completed successfully.")
print(result_str.strip())

# Generate HTML file
TEXT = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Basic HTML Page</title>
</head>'''
#DIR = "CHATDPT/individual_sessions/"
HTMLfile =file_name[:-5] + "_new-.html"
logging.info(f"Creating HTML file: {HTMLfile}")

try:
    with open(HTMLfile, "w") as Input:
        Input.write(TEXT)
        result_str = result_str.replace("\n", "XXXXXXX\n")
        result_str = result_str.replace("<", "&lt;")
        result_str = result_str.replace(">", "&gt;")
        for line in result_str.split("XXXXXXX"):
            line = line.replace("\n", "<br />\n")
            Input.write(line)
except Exception as e:
    logging.error(f"Error creating HTML file: {e}")
    raise
else:
    logging.info("HTML file creation completed successfully.")
