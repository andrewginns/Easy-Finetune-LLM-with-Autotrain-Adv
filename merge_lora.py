import os
import shutil

from peft import AutoPeftModelForCausalLM
from transformers import AutoModelForCausalLM

# Specify the paths to your base model and LoRA adapter
base_model_path = "mistralai/Mistral-7B-Instruct-v0.1"
lora_location = "my-custom-Mistral-7B-Instruct-v0.1"
proj_path = os.getcwd()
lora_adapter_path = os.path.join(proj_path, lora_location)

# Load the base model with 4-bit integer quantization
print("Loading base model")
base_model = AutoModelForCausalLM.from_pretrained(base_model_path, load_in_4bit=True)

# Load the LoRA adapter
print("Loading LORA")
adapter_model = AutoPeftModelForCausalLM.from_pretrained(lora_adapter_path)

# Merge the LoRA adapter with the base model
print("Merging LORA with base")
merged_model = adapter_model.merge_and_unload()

# Save the merged model
merged_model_path = os.path.join(proj_path, f"{lora_location}/merged_model")
merged_model.save_pretrained(merged_model_path)

# Copy the tokenizer files to the merged model directory
tokenizer_files = ['tokenizer_config.json', 'tokenizer.json', 'special_tokens_map.json']
for filename in tokenizer_files:
    shutil.copy(os.path.join(lora_adapter_path, filename), os.path.join(merged_model_path, filename))
