import os
import shlex
import subprocess

# Data configs
PROJECT_NAME = 'my-custom-Mistral-7B-Instruct-v0.2'
SOURCE_MODEL = 'mistralai/Mistral-7B-Instruct-v0.2'
proj_path = os.getcwd()
DATA_PATH = os.path.join(proj_path, 'data')
TEXT_COLUMN = 'text'

# Model fine-tuning configs
LEARNING_RATE = 2e-4
BATCH_SIZE = 1
NUM_EPOCHS = 1
TRAINER = "sft"
USE_PEFT = True
USE_INT4 = False
USE_INT8 = True
TARGET_MODULES = "q_proj,v_proj"
LORA_ALPHA = 32
MERGE_ADAPTER = True

# Optional HF integrations - By default does not push anything to HF
PUSH_TO_HUB = False
HF_TOKEN = "YOUR HF TOKEN"
REPO_ID = "username/repo_name"

# Construct the command string
command = (
    f"autotrain llm --train --model {SOURCE_MODEL} "
    f"--project-name {PROJECT_NAME} --data-path {DATA_PATH} "
    f"--text-column {TEXT_COLUMN} --lr {LEARNING_RATE} --batch-size {BATCH_SIZE} "
    f"--epochs {NUM_EPOCHS} --trainer {TRAINER} "
    f"--target-modules {TARGET_MODULES} "
    f"--lora_alpha {LORA_ALPHA} "
    f"{'--use-peft' if USE_PEFT is True else ''} "
    f"{'--use-int4' if USE_INT4 is True else ''} "
    f"{'--use-int8' if USE_INT8 is True else ''} "
    f"{'--merge-adapter' if MERGE_ADAPTER is True else ''} "
    f"{'--push-to-hub --token ' + HF_TOKEN + ' --repo-id ' + REPO_ID if PUSH_TO_HUB == 'True' else ''}"
)

# Note: Running inline doesn't function properly as required conda env isn't activated
# Split the command string into a sequence of program arguments
# args = shlex.split(command)
# Run the command and allow terminal output
# subprocess.run(args) - Fails as an active environment cannot be defined for the subprocess to use

# Tell user to run a printed command
print(f"\n\nRun the following command in the bash terminal with the envrionment active:\n\n{command}")
