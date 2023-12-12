.ONESHELL:

TARGET_USER = default

# Define environment variables
SHELL = /bin/bash
CONDA_BASE = $(shell conda info --base)
CONDA_ACTIVATE = source $(CONDA_BASE)/etc/profile.d/conda.sh ; conda activate
ENV_NAME = autotrain
ENV_FILE = environment/autotrain.yml

# Define any reusable blocks that are not targets
define deactivate_conda
	for i in $$(seq $${CONDA_SHLVL}); do \
		source $(CONDA_BASE)/etc/profile.d/conda.sh ; conda deactivate ; \
	done
endef

# Define targets
env:
	# Deactivate any existing environments
	$(MAKE) remove-env
	# Install environment from .yml file
	$(CONDA_ACTIVATE) ; conda env create -f $(ENV_FILE)
	# Setup autotrain
	conda activate $(ENV_NAME) ; autotrain setup

slack_to_autotrain:
	# Check if TARGET_USER has been changed from the default value
	if [ "$(TARGET_USER)" = "default" ] ; then \
		echo "Set TARGET_USER to a specific Slack user id"; \
		exit 1; \
	fi

	# Deactivate any active environments
	$(deactivate_conda)
	# Add output path
	mkdir data
	# Activate env
	conda activate $(ENV_NAME)
	# Convert Slack messages to OpenAI fine-tuning format
	python slack_to_oai.py --target_user=$(TARGET_USER)
	# Convert OpenAI format to Hugging Face AutoTrain format
	python convert_oai_to_autotrain.py

fine_tune:
	# Deactivate any active environments
	$(deactivate_conda)
	# Activate env
	conda activate $(ENV_NAME)
	# Use Hugging Face AutoTrain to create a LORA for a base model on Slack messages
	python finetune_LLM.py

test_lora:
	# Deactivate any active environments
	$(deactivate_conda)
	# Activate env
	conda activate $(ENV_NAME)
	# Test the LORA
	python test_lora.py

remove-env:
	# Deactivate any active environments
	$(deactivate_conda)
	# Remove any prior installations of environment
	$(CONDA_ACTIVATE) ; conda remove --name $(ENV_NAME) --all -y
