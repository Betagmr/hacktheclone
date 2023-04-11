# define the name of the virtual environment directory
VENV = .venv
PY = python3
PI = pip3

BIN=$(VENV)/bin
PYTHON = $(BIN)/$(PY)
PIP = $(BIN)/$(PI)

all: run clean

run: $(BIN)/activate
	./$(VENV)/bin/python3 -m streamlit run src/app.py

$(BIN)/activate: requirements-dev.txt
	$(PYTHON) -m piptools sync ./requirements-dev.txt

install:
	$(PI) install virtualenv
	$(PY) -m virtualenv $(VENV)
	$(PIP) install pip-tools
	$(PYTHON) -m piptools sync ./requirements-dev.txt
	$(PYTHON) -m pre_commit install

clean:
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	find . -type f -name '*.pyc' -delete

.PHONY: all run clean
