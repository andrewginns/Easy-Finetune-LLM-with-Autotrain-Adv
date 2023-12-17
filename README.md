# Introduction
Simple repo to finetune an LLM on your own hardware. Base models are pulled from Hugging Face (HF), LORA is created on new data, resulting model is merged from base+LORA.

The repo allows you to take [OpenAI formatted datasets designed for fine-tuning](https://platform.openai.com/docs/guides/fine-tuning) and use them to finetune of the the model base `Mistral-7B-Instruct-v0.2` pulled from HF.

The [Quickstart](#quickstart) example The Slack messages to the OpenAI format Takes in a folders of downloaded Slack messages and re-formats them to create a `train.csv` so that the LLM learns to respond like a specific target user.

Training data is formatted with the [Mistral instruction format](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2#instruction-format):
*  `<s>[INST] Message to target user [/INST] Target user response </s>`

# Quickstart
1. Utilises an example `json` obtained from slack with a tool like https://github.com/chr1spy1/slack-export/tree/master
    * Contains message history between users `U0XXXXXXXXXX` and `U0ZZZZZZZZZZ`

2. `make TARGET_USER=U0ZZZZZZZZZZ slack_to_oai`
    * Converts downloaded Slack messages to the [format needed by OpenAI](https://platform.openai.com/docs/guides/fine-tuning/example-format)
    * Data formatted so that the selected user `U0ZZZZZZZZZZ` message responses are set as the 'assistant' responses for fine-tuning
        * In actual use modify the value of `TARGET_USER` to a specific Slack id e.g. `U027S88LZ6U`
    * Uses very basic methods to extract the question-response flow between users
    * Outputs a `jsonl` holding conversations between `user` and `assistant` to `data/all_messages.jsonl`

3. `make oai_to_autotrain`
    * Converts OAI formatted dataset of user-assisant message pairs to the format needed by `autotrain`
    * Outputs a `csv` file for fine-tuning to `data/train.csv`

4. `make fine_tune`
    * Creates a command to fine-tune a Hugging Face model to respond like the target user on Slack
        * Run the printed output in terminal
        * [Optionally] Configure in `finetune_LLM.py`
    * Example `data/train.csv` only contains 4 examples to fine-tune. Actual use should have 1000's of examples for decently tuned models
    * Once run the command will output to a folder named `my-custom-Mistral-7B-Instruct-v0.2`

5. `make test_lora`
    * Tests the LORA with a simple question "I can't access the code repo, do you know what's wrong?"

## Converting the Output Fine-tuned Models to GGUF format

1. Utilise llama.cpp to [convert the model to OpenLLaMA format](https://github.com/ggerganov/llama.cpp#using-openllama)
    * `python convert.py /path/to/my-custom-Mistral-7B-Instruct-v0.2/ --outfile /path/to/my-custom-Mistral-7B-Instruct-v0.2/my-custom-Mistral-7B-Instruct-v0.2.gguf`
    * Will require an environment with the llama.cpp dependencies installed
2. Quantise to the desired bpw
    * `./quantize /path/to/my-custom-Mistral-7B-Instruct-v0.2/my-custom-Mistral-7B-Instruct-v0.2.gguf /path/to/my-custom-Mistral-7B-Instruct-v0.2/ggml-model-q4_0.gguf q4_0`

## Hardware Requirements
Using the default repo configuration and `finetune_LLM.py` parameters to fine-tune `Mistral-7B-Instruct-v0.2` requires ~24GB of VRAM and ~3 hours of compute on an Nvidia A10G
* Configuring `USE_INT4 = True` and `USE_INT8 = False` will decrease VRAM requirements by roughly half

If you do not have enough VRAM you will experience CUDA errors.