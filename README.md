copy the converasions zip file into CHATGPT directory
XXXXXXXXXXXXXXXXXXXXXXXX81170fe5ceac0c6089de278f53bc59d14c24d71-2024-02-22-00-35-13.zip
notice the date at the end: -2024-02-22-00-35-13.zip
unzip it:
CHATGPT/chat.html
*  CHATGPT/conversations.json
/home/jack/Desktop/HDD500/Desktop/flask_conversations_readable/CHATGPT/XXXXXXXXXXXXXXXXXXXXXXXX-2024-02-22-00-35-13.zip
CHATGPT/message_feedback.json
CHATGPT/model_comparisons.json
CHATGPT/shared_conversations.json
CHATGPT/user.json

conversations.json is the file of interest
run:
python create_tree.py
that will create

CHATGPT/html
CHATGPT/individual_sessions
CHATGPT/text
