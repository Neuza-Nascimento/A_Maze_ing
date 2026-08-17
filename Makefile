PYTHON = python3.14
UV = uv
REQS = requirements.txt
CONFIG = config.txt
MAIN = a_maze_ing.py

all: install

install:
	$(UV) sync

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint:
	flake8 . --exclude=lib
	mypy . --exclude lib --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	flake8 . --exclude=lib
	mypy . --exclude=lib --strict

clean:
	rm -rf __pycache__ .mypy_cache .ruff_cache

.PHONY: all install run debug lint clean