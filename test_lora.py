import os

from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cuda:0"
proj_path = os.getcwd()
model_path = os.path.join(proj_path, "my-custom-Mistral-7B-Instruct-v0.1")
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, load_in_4bit=True)

input_text = "I can't access the code repo, do you know what's wrong?"
input_ids = tokenizer.encode('[INST]' + input_text + '[/INST]', return_tensors="pt").to(device)
output = model.generate(input_ids, max_new_tokens=200)
predicted_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(predicted_text)
