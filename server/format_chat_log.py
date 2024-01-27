import json
import os
from datetime import datetime

def format_chat_log(chat_log):
    formatted_chat_log = ""
    requests = chat_log['requests']
    for request in requests:
        # Check if the 'message' key exists before trying to access it
        if 'message' in request and 'text' in request['message']:
            # Add the line of dashes
            formatted_chat_log += "------------------------------------------------------------------------------------------------------------------------------------------------\n"
            # Add the message text to the log with 'input:' prepended
            formatted_chat_log += f"input: {request['message']['text']}\n"
        
        # Add the response text to the log with 'output:' prepended
        for response in request['response']:
            formatted_chat_log += f"output: {response['value']}\n"
        
        # Add any follow-up messages to the log
        if 'followups' in request:
            for followup in request['followups']:
                if 'message' in followup:
                    # Add the line of dashes
                    formatted_chat_log += "--------------------------------------------------------------------------------------------------------------------------------------------------------\n"
                    # Add the follow-up message to the log with 'input:' prepended
                    formatted_chat_log += f"input: {followup['message']}\n"
    
    return formatted_chat_log

# Read the JSON file
with open('chat.json', 'r') as f:
    chat_log = json.load(f)

# Format the chat log
formatted_chat_log = format_chat_log(chat_log)

# Get the current date
current_date = datetime.now()

# Format the date as a string in the "dd/mm/yyyy" format
date_string = current_date.strftime("%d_%m_%Y")

# Create the file name
file_name = f"{date_string}.txt"

# Specify the directory where you want to create the file
directory = r"/home/wangding/adeept_rasptank/server/chat_logs"

# Create the full file path
file_path = os.path.join(directory, file_name)

# Create and open the file
with open(file_path, 'w') as f:
    f.write(formatted_chat_log)