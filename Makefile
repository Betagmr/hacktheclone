PY = python3
PI = pip3
VENV = .venv
BIN=$(VENV)/bin

ifeq ($(OS), Windows_NT)
    BIN=$(VENV)/Scripts
    PY=python
endif

PYTHON = $(BIN)/$(PY)
PIP = $(BIN)/$(PI)

install:
	$(PI) install virtualenv
	$(PY) -m virtualenv $(VENV)
	$(PIP) install pip-tools
	$(PYTHON) -m piptools sync ./requirements-dev.txt
	$(PYTHON) -m pre_commit install

run:
	$(PYTHON) -m streamlit run src/app.py

clean:
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf .pytest_cache
	find . -name '__pycache__' -type d -exec rm -rf {} +
