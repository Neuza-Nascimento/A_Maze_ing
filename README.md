*This project has been created as part of the 42 curriculum by nedo-nas, rodrpere.*

# A-Maze-Ing: This is the way

## Table of Contents

## Introduction

Create your own maze generator and display its result!

## Description

The A-Maze-Ing Project asks us to implement a maze generator in Python that takes a configuration file in order to generate a maze, possibly perfect (with a single path between entrance and exit), and writes it to a output file of the user's name choice, using a hexadecimal wall representation. Provididing as well a visual representation of the maze.

## Instructions

It is best to install the UV dependency manager in order to use the provided Makefile, a requirements.txt is also found at the root of the repository in case UV is cannot be used, and in that case:

Run the following commands to install the dependencies for the package
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

	If your python version is not python 3.14.0, the python command my not be usable, so instead use python3. 

The Makefile provided can be used to:  
install, run, build, debug, and lint the code in this repository.

```bash
make install
```

The *install* instruction will execute uv to sync the virtual enviroment to the pyproject file, if there is no venv in the current directory it will create one and install all the necessary dependencies to use the project 

```bash
make run
```

The *run* instruction will execute uv to run the main script with the config.txt file present at the root of the repository, in case the config file is not present, the main script will raise an 'File Not Found Error' and exit with the status of 1

```bash
make lint
# or 
make lint-strict
```

Both the *lint* and *lint-strict* instructions will call uv to run mypy and flake8, if the lint-strict instruction is used mypy will be executed with the --strict flag. We use uv to run these tools in order that no missing-imports warn shows up because that could be a misleading warn if the dependencies are all installed but if UV is cannot be used, calling either `python -m flake8/mypy .` or `flake8/mypy .` will work

The *build* and *debug* instructions are stricly for building the whells and tar file asked by the subject and helping to debug the code found here. They shouldnt be used unless for those that maintain this project

## Resources

AI was used to do shit here, 

## Structure
### Parsing
### Configuration
### Generation
### Visualization
### Tools
## Features
### Package Project
### Code Reusability
### Bonus Features
### Project Management
## Team
### Neuza
### Rodrigo
