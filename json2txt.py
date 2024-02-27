#!/home/jack/miniconda3/envs/cloned_base/bin/python
import json
import os
from sys import argv

# Load the JSON data from the uploaded file
DIR = os.getcwd() + "/CHATGPT/individual_sessions/"
DIR_text = os.getcwd() + "/CHATGPT/text"
# Ensure the output folder exists
os.makedirs(DIR_text, exist_ok=True)
filename = argv[1]
Filename = DIR + filename
print(Filename)

with open(Filename, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

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
TEXTfile = DIR_text + "/" + filename[:-5] + ".txt"  # Changed this line to properly handle the filename
print("TEXTfile: ", TEXTfile)
with open(TEXTfile, "w", encoding='utf-8') as Input:
    result_str = result_str.replace("/n", "XXXXXXX\n")
    for line in result_str.split("XXXXXXX"):
        Input.write(line)
