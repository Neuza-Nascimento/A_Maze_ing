PYTHON = python
UV = uv
CONFIG = config.txt
MAIN = a_maze_ing.py
SUBDIR = src/mazegen
CACHE = __pycache__ .mypy_cache .ruff_cache \

all: install

install:
	$(UV) sync

run:
	$(UV) run $(MAIN) $(CONFIG)

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
	rm -rf $(CACHE)
	rm -rf $(addprefix $(SUBDIR)/,$(CACHE))

fclean: clean
	rm -rf .venv

.PHONY: all install run debug lint lint-strict clean
