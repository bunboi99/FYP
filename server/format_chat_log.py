import json

def format_chat_log(chat_log):
    formatted_chat_log = ""
    requests = chat_log['requests']
    for request in requests:
        # Check if the 'message' key exists before trying to access it
        if 'message' in request and 'text' in request['message']:
            # Add the message text to the log with 'input:' prepended
            formatted_chat_log += f"input: {request['message']['text']}\n"
        
        # Add the response text to the log with 'output:' prepended
        for response in request['response']:
            formatted_chat_log += f"output: {response['value']}\n"
        
        # Add any follow-up messages to the log
        if 'followups' in request:
            for followup in request['followups']:
                if 'message' in followup:
                    # Add the follow-up message to the log with 'input:' prepended
                    formatted_chat_log += f"input: {followup['message']}\n"
    
    return formatted_chat_log

# Read the JSON file
with open('chat.json', 'r') as f:
    chat_log = json.load(f)

# Format the chat log
formatted_chat_log = format_chat_log(chat_log)

# Write the formatted chat log to a text file
with open('formatted_chat_log.txt', 'w') as f:
    f.write(formatted_chat_log)