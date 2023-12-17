import argparse
import json
import os
from collections import deque

# Create the parser
parser = argparse.ArgumentParser()

# Add the arguments
parser.add_argument('--target_user', type=str, required=True,
                    help='Slack user ID to extract messages and response for e.g. U027S88LZ6U')
parser.add_argument('--input_path', type=str, default="slack_messages",
                    help='Input path for slack-export json formatted messages and responses')
parser.add_argument('--output_path', type=str, default="data",
                    help='Output path for OpenAI jsonl formatted messages and responses')

# Parse the arguments
args = parser.parse_args()

# Set your target user ID to use for the 'assistant' responses
target_user = args.target_user
print(f"Extracting data to respond like user {target_user}")

# Initialize the root directory where your JSONL will be output
proj_path = os.getcwd()
root_dir = os.path.join(proj_path, args.input_path)

# Create list to hold Slack data for JSONL output
res = []
# Loop through the files in the root directory
print(f"Searching for json files in {root_dir}")
for dirpath, dirnames, filenames in os.walk(root_dir):
    for file_name in filenames:
        if file_name.endswith('.json'):
            file_path = os.path.join(dirpath, file_name)

            # Open and read the JSON file
            with open(file_path, 'r') as f:
                data = json.load(f)

            # Initialize a deque to store messages from the target user
            buffer = deque()
            last_question = ""
            last_user = None

            for elem in data:
                try:
                    # Process blocks containing the messages
                    if 'blocks' in elem and elem['blocks']:
                        full_text = ''
                        for block in elem['blocks']:
                            for text_section in block['elements']:
                                for part in text_section['elements']:
                                    if part['type'] == 'text':
                                        full_text += part['text']
                                    elif part['type'] == 'link':
                                        full_text += part['url']
                        # Determine if the element is from the target user
                        if elem['user'] == target_user:
                            if last_user != target_user and last_question:
                                # Only add to buffer if the last user was not the target user
                                buffer.append(full_text)
                        else:
                            if buffer:
                                # If there is a response from the target user to the last conversation,
                                # combine and add it to the result.
                                combined_message = '\n'.join(buffer)
                                res.append({
                                    "messages": [
                                        {"role": "system", "content": ""},
                                        {"role": "user", "content": last_question},
                                        {"role": "assistant", "content": combined_message}
                                    ]
                                })
                                buffer.clear()
                            # Update the new last question and last user
                            last_question = full_text

                        # Update the last user for the next iteration
                        last_user = elem['user']

                except Exception as e:
                    print(f"Error processing message: {e}")
                    continue

            # Check for the last conversation in the file, if present
            if buffer and last_question:
                combined_message = '\n'.join(buffer)
                res.append({
                    "messages": [
                        {"role": "system", "content": ""},
                        {"role": "user", "content": last_question},
                        {"role": "assistant", "content": combined_message}
                    ]
                })

# Save the results to a JSONL file
with open(os.path.join(proj_path, args.output_path, 'all_messages.jsonl'), 'w') as outfile:
    for entry in res:
        json.dump(entry, outfile)
        outfile.write('\n')
