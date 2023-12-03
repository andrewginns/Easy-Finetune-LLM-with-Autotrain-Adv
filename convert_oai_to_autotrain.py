import pandas as pd
import json
import os


def jsonl_to_dataframe(jsonl_path):
    data = []
    with open(jsonl_path, 'r') as file:
        for line in file:
            obj = json.loads(line)
            record = {
                'instruction': '',
                'input': '',  # This is left blank as its intended usage is instruction + input --> output
                'output': '',
                'text': ''
            }
            # Parse the jsonl
            for message in obj['messages']:
                if message['role'] == 'user':
                    record['instruction'] = message['content']
                elif message['role'] == 'assistant':
                    record['output'] = message['content']
            # Format text in the way the model expects it (This is the Mistral format)
            record['text'] = f"<s>[INST] {record['instruction']} [/INST] {record['output']} </s>"
            data.append(record)

    df = pd.DataFrame(data)
    return df


# Load OpenAI formatted jsonl
proj_path = os.getcwd()
jsonl_path = os.path.join(proj_path, 'all_messages.jsonl')
df = jsonl_to_dataframe(jsonl_path)
df.to_csv(os.path.join(proj_path, 'data/train.csv'), index=False)
