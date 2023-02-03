.PHONY: *
.DEFAULT_GOAL := help

#################################################################################
# USER DEFINED                                                                  #
#################################################################################

PYTHON_VERSION = 3.10

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = ipython-memory-magics
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

ifeq (,$(shell which mamba))
HAS_MAMBA=False
else
HAS_MAMBA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Set up Python interpreter environment
create_environment:
ifeq (True,$(HAS_MAMBA))
	mamba create --name $(PROJECT_NAME) python=$(PYTHON_VERSION)
else
	ifeq (True,$(HAS_CONDA))
		conda create --name $(PROJECT_NAME) python=$(PYTHON_VERSION)
	else
		python -m venv .venv
	endif
endif

## Create requirements.txt files from pyproject.toml
create_requirements:
	poetry export -f requirements.txt -o requirements.txt --with=dev --without-hashes

## Install Python dependencies
install:
	# using requirements.txt to allow installation without Poetry
	- make create_requirements  # update requirements.txt if Poetry is installed
	pip install -r requirements.txt  # install pinned dependencies
	- jupyter contrib nbextension install --user

## Delete all unwanted files
clean:
	find . -type f -name ".DS_Store" -exec rm -r -v {} +
	find . -type f -name "*.py[co]" -exec rm -r -v {} +
	find . -type d -name "__pycache__" -exec rm -r -v {} +
	find . -type d -name ".pytest_cache" -exec rm -r -v {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -r -v {} +

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' uniq \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
