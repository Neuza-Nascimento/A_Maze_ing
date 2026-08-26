PYTHON = python
UV = uv
INSTALL = $(UV) sync
RUN = $(UV) run
BUILD = $(UV) build
CONFIG = config.txt
MAIN = a_maze_ing.py
SUBDIR = src/mazegen
CACHE = __pycache__ .mypy_cache .ruff_cache \

all: install

install:
	$(INSTALL)

run:
	$(RUN) $(MAIN) $(CONFIG)

build:
	$(BUILD) --no-create-gitignore

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint:
	$(RUN) flake8 . --exclude=lib
	$(RUN) mypy . --exclude lib --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	$(RUN) flake8 . --exclude=lib
	$(RUN) mypy . --exclude=lib --strict

clean:
	rm -rf $(CACHE)
	rm -rf $(addprefix $(SUBDIR)/,$(CACHE))

fclean: clean
	rm -rf .venv maze.txt

.PHONY: all install run build debug lint lint-strict clean fclean
