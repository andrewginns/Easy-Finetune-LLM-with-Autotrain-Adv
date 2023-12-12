# Introduction
Simple repo to finetune an LLM on your own hardware. Base models are pulled from Hugging Face (HF), LORA is created on new data, resulting model is merged from base+LORA.

Repo creates a finetune of the the model base `Mistral-7B-Instruct-v0.1` pulled from HF.

Takes in a folders of downloaded Slack messages and re-formats them to create a `train.csv` so that the LLM learns to respond like a specific target user.

Training data is formatted with the Mistral format prompts:
*  `<s>[INST] Message to target user [/INST] Target user response </s>`

# Quickstart
1. Obtain Slack messages using https://github.com/chr1spy1/slack-export
    * Save them to a new directory in this repo root called `slack_messages`
    * Can include multiple levels of subfolder based on DM's, groups, etc.

2. `make TARGET_USER=default slack_to_autotrain`
    * Modify `default` value of `TARGET_USER` to a specific Slack id e.g. `U027S88LZ6U` 
    * Converts downloaded Slack messages to the format needed by `autotrain`
    * Data formatted to train an LLM to respond like a target user
    * Outputs a csv `data/train.csv`

3. `make fine_tune`
    * Creates a command to fine tune a Hugging Face model to respond like the target user on Slack
    * Merges the LORA with the base HF model in pytorch format
        * Can be converted to GGUF directly by llama.cpp
    * Command will output to a folder named `my-custom-Mistral-7B-Instruct-v0.1`

4. `make test_lora`
    * Tests the LORA with a simple question "I can't access the code repo, do you know what's wrong?"

5. `make merge_lora_to_base`
    * Merge the LORA to the base Hugging Face model
    * Outputs a merged model to a new folder `my-custom-Mistral-7B-Instruct-v0.1/merged_model`