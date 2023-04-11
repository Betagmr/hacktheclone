# define the name of the virtual environment directory
VENV = .venv
PY = python3
PI = pip3

BIN=$(VENV)/bin
PYTHON = $(BIN)/$(PY)
PIP = $(BIN)/$(PI)

all: run clean

run:
	./$(VENV)/bin/python3 -m streamlit run src/app.py

update: requirements.txt
	$(PYTHON) -m piptools sync ./requirements.txt

install:
	$(PI) install virtualenv
	$(PY) -m virtualenv $(VENV)
	$(PIP) install pip-tools
	$(PYTHON) -m piptools sync ./requirements.txt
	$(PYTHON) -m pre_commit install

clean:
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	find . -type f -name '*.pyc' -delete

.PHONY: all run clean update
