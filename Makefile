SHELL := /bin/sh

MAKEFILE_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))
ENV_DIR = $(MAKEFILE_DIR)/.venv
PY = python3
ENV_PY = $(ENV_DIR)/bin/$(PY)
GIT = git

.PHONY: play clean check

play:
	$(PY) $(MAKEFILE_DIR)/etch.py

$(ENV_DIR):
	$(PY) -m venv $(ENV_DIR)
	$(ENV_DIR)/bin/pip install --upgrade pip

venv: $(ENV_DIR)

install: venv
	$(ENV_DIR)/bin/pip install $(MAKEFILE_DIR)

install-%: venv
	$(ENV_DIR)/bin/pip install --editable $(MAKEFILE_DIR)[$*]

clean:
	$(GIT) clean --force -x --exclude="\.idea/" -- $(MAKEFILE_DIR)

check: install-dev
	$(ENV_PY) -m ruff check --fix