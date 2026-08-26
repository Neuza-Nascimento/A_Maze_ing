*This project was developed as part of the 42 curriculum by nedo-nas and rodrpere.* 

# A-Maze-Ing: This is the way

## Table of Contents

1. [Introduction](#introduction)
   1. [Description](#description)
   2. [Objectives](#objectives)
2. [Instructions](#instructions)
   1. [Prerequisites](#prerequisites)
   2. [Installation](#installation)
   3. [Running the Project](#running-the-project)
   4. [Makefile Commands](#makefile-commands)
3. [Configuration](#configuration)
4. [Architecture and Implementation](#architecture-and-implementation)
   1. [Parsing and Validation](#parsing-and-validation)
   2. [Maze Representation](#maze-representation)
   3. [Maze Generation](#maze-generation)
   4. [Maze Solving](#maze-solving)
   5. [Output File Format](#output-file-format)
5. [Visualization](#visualization)
6. [Features](#features)
   1. [Required Features](#required-features)
   2. [Bonus: Pac-Man Mode](#bonus-pac-man-mode)
7. [Reusable Module](#reusable-module)
8. [Work Distribution](#work-distribution)
9. [Resources](#resources)

## Introduction

### Description

**A-Maze-Ing** is a maze generation, solving, and visualization project. The application reads a configuration file, builds a maze using the selected algorithm, calculates a path between the entrance and the exit, and writes the results to a text file. It then displays a graphical and interactive representation using **MiniLibX**, a graphics library based on X11.

The maze can be **perfect**, meaning that its structure is built without cycles and that there is a single path between any two connected cells, or **imperfect**, meaning that additional passages are opened to create alternative routes and reduce the number of dead ends.

### Objectives

The project is organized around four main responsibilities: interpreting and validating the supplied configuration; generating the maze deterministically when a seed is used; finding a valid path and, whenever possible, the shortest path; and providing a clear and interactive visualization of the result.

The implementation includes three generation algorithms — **Kruskal**, **Prim**, and **DFS with backtracking** — and uses **BFS** to solve the maze. This separation makes it possible to compare different generation strategies while keeping a common solving mechanism.

## Instructions

### Prerequisites

A compatible version of **Python**, the **uv** dependency manager, and the libraries required to run the project are needed. The visualization also requires an environment with **MiniLibX/X11** support.

The project includes a `pyproject.toml`, a `requirements.txt`, and a `Makefile` to simplify environment setup.

### Installation

The recommended way to install the project is through the Makefile:

```bash
make install
```

This command creates or synchronizes the virtual environment and installs the dependencies declared by the project.

If `uv` cannot be used, a virtual environment can be created and prepared manually:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Running the Project

The application receives the path to the configuration file as its only argument:

```bash
python3 a_maze_ing.py config.txt
```

The Makefile command can also be used when it is configured to use the project's default configuration file:

```bash
make run
```

The application exits with an error message when the file does not exist, when the configuration is invalid, or when no path can be found between the entrance and the exit.

### Makefile Commands

| Command | Purpose |
|---|---|
| `make install` | Creates or updates the virtual environment and installs the dependencies. |
| `make run` | Runs the application using the project's default configuration. |
| `make lint` | Runs the code-quality checks. |
| `make lint-strict` | Runs the code-quality checks with stricter rules. |
| `make build` | Prepares the distribution artifacts required by the subject. |
| `make debug` | Provides the execution flow intended for debugging. |

## Configuration

Execution depends on a configuration file. This file defines the maze dimensions, the entrance and exit coordinates, the generation algorithm, the seed, the perfect or imperfect mode, and the output file name.

The configuration is validated before generation begins. Invalid dimensions, out-of-bounds coordinates, unknown algorithms, or incompatible values are therefore rejected in a controlled manner.

A conceptual configuration example is shown below; names and values must follow exactly the format defined by the project's parser:

```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
ALGORITHM=KRUSKAL
```

The available algorithms are `KRUSKAL`, `PRIM`, and `DFS`. Setting `PERFECT=False` activates the additional phase that opens passages and introduces alternative routes.

## Architecture and Implementation

### Parsing and Validation

The parsing module reads the file specified on the command line and converts its textual values into a validated configuration object. Validation takes place before the `MazeGenerator` is created, separating input errors from the generation logic and the graphical layer.

The main program coordinates the complete workflow: it validates the number of arguments, reads the configuration, creates the generator, generates the maze, solves it, writes the result, and finally starts the visualization.

### Maze Representation

Each cell is represented by a four-bit hexadecimal value. Each bit indicates whether a wall exists in one of the four directions:

| Direction | Representation |
|---|---|
| North | `N` |
| East | `E` |
| South | `S` |
| West | `W` |

A wall is stored symmetrically: when a passage is opened between two cells, the bit for the corresponding direction is removed from the first cell and the bit for the opposite direction is removed from the second cell. This representation makes generation, solving, and file output efficient.

The **42 pattern** is reserved in the centre of the maze whenever the dimensions allow it. Cells blocked by this pattern do not participate in path generation.

### Maze Generation

#### Kruskal

Kruskal's algorithm starts with each cell as an independent set. The walls between neighbouring cells are shuffled, and a wall is removed only when it joins two different sets. Under normal conditions, the resulting structure is a spanning tree, producing a perfect maze.

#### Prim

The randomized version of Prim's algorithm starts at the entrance cell and maintains a frontier of candidate walls. At each step, it selects a random wall connecting the already generated maze to an unvisited cell. The maze therefore grows progressively from the entrance.

#### DFS with Backtracking

DFS starts at the entrance, randomly selects an unvisited neighbouring cell, and opens the wall between the two cells. When no unvisited neighbours are available, it backtracks through the stack until it finds a cell with new possibilities. This process continues until all accessible cells have been visited.

#### Imperfect Maze

When `PERFECT=False`, an additional phase is executed after the main generation step. Walls separating valid cells are selected, prioritizing walls adjacent to cells with only one open passage. Removing some of these walls creates cycles and alternative paths, reducing the number of dead ends and producing behaviour closer to a Pac-Man maze.

### Maze Solving

The maze is solved using **Breadth-First Search (BFS)**. The algorithm explores cells level by level, starting at the entrance, and stores the path followed to reach each position. When the exit is found, the reconstructed path is returned as a sequence of directions.

Because BFS visits positions in order of their distance from the entrance, the resulting path is the **shortest path in terms of the number of moves**, as long as all transitions have the same cost. The solution is stored and used both in the output file and in the graphical animation.

### Output File Format

The generated file contains the following sections, in order:

1. The maze grid, with one hexadecimal row per grid row.
2. A blank separator line.
3. The entrance coordinates.
4. The exit coordinates.
5. A blank separator line.
6. The sequence of letters representing the path found.

Example structure:

```text
F9D...
...

0, 0
19, 14

EESSE...
```

## Visualization

The `MazeVisualizer` class uses **MiniLibX** to create a window and draw the maze cell by cell. Walls, cells, entrance, exit, the 42 pattern, and the path are drawn using distinct colours. The size of each cell is calculated from a fixed graphical unit, ensuring a consistent representation.

The interface provides the following controls:

| Key | Action |
|---|---|
| `1` | Generates a new maze using a random seed and updates the window. |
| `2` | Displays the path between the entrance and the exit as an animation. |
| `3` | Switches to another colour theme. |
| `ESC` | Exits the application. |
| Window close button | Exits the application through the window event. |

The animation progressively draws the cells belonging to the path, making it possible to observe the solution rather than only seeing its final state.

## Features

### Required Features

The program reads and validates the configuration, supports three generation algorithms, writes the maze in hexadecimal format, finds a solution using BFS, and displays a graphical version through MiniLibX. Using a seed makes it possible to repeat generation with the same parameters and obtain the same logical result.

The application also handles configuration errors, missing files, and situations in which the exit cannot be reached. The generation and solving logic is separated from the visualization layer, making the code easier to reuse and maintain.

### Bonus: Pac-Man Mode

The imperfect mode is the project's bonus feature. When the `PERFECT` parameter is false, the maze is no longer only a tree of paths: additional passages are opened and the number of dead ends is reduced. The result aims to reproduce the structure of a **Pac-Man** maze, with more intersections, cycles, and possible routes.

## Reusable Module

### Purpose and package structure

The maze-generation logic is implemented in the reusable `MazeGenerator` class inside the `mazegen` module. It is kept separate from the command-line entry point (`a_maze_ing.py`) and from the MiniLibX visualizer, so that another Python project can import the generator without depending on the graphical interface.

The reusable package is intended to be built from the repository root and distributed using the `mazegen-*` package name. The package contains the generator, its configuration model, the direction and wall constants required by the algorithms, and the public methods needed to generate, inspect, and solve a maze.

A typical repository layout is:

```text
.
├── a_maze_ing.py          # Command-line entry point
├── config.txt             # Default configuration
├── mazegen/               # Reusable package
│   ├── __init__.py
│   ├── maze_generator.py
│   ├── maze_config.py
│   └── magic_values.py
├── maze_visualizer.py     # MiniLibX visualization
├── pyproject.toml
├── Makefile
├── LICENSE.md
└── README.md
```

### Building and installing the module

The package can be built from the source files supplied in the repository. In an activated virtual environment, install the standard build tool and create the distribution artifacts:

```bash
python3 -m pip install build
python3 -m build
```

The generated files are placed in the `dist/` directory. The reusable module can then be installed from the wheel or source archive:

```bash
python3 -m pip install dist/mazegen-*.whl
# or
python3 -m pip install dist/mazegen-*.tar.gz
```

The package can also be installed directly from the project root during development:

```bash
python3 -m pip install .
```

The exact versioned filename depends on the version declared in `pyproject.toml`, for example `mazegen-1.0.0-py3-none-any.whl`.

## Work Distribution

| Person | Main responsibilities |
|---|---|
| **Neuza** | Development of the visual component; implementation of the BFS solving algorithm; implementation of Kruskal's algorithm; development of the imperfect maze generator. |
| **Rodrigo** | Implementation of the Prim and DFS algorithms; development of the parser; virtual-environment setup; preparation and maintenance of the Makefile. |

Although responsibilities were initially divided, the project was developed collaboratively. Both team members followed all components, discussed implementation decisions, and participated in testing, integration, and the final adjustments.

## Resources

The subject materials and the documentation for the tools used were consulted throughout development. The main references are:

- [MiniLibX Documentation](https://harm-smits.github.io/42docs/libs/minilibx)
- [Python Documentation](https://docs.python.org/3/)
- [uv — Python Package and Project Manager](https://docs.astral.sh/uv/)

Support tools, including artificial intelligence, were used for research, review, and development assistance. All architecture, implementation, integration, and validation decisions were reviewed by the team.
