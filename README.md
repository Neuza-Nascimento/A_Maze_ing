*This project has been created as part of the 42 curriculum by nedo-nas, rodrpere.*

# A-Maze-Ing: This is the way

## Table of Contents

1. [Introduction](#introduction)
	1. [Description](#description)
	2. [Instalation](#instalation)
	3. [Resources](#resources)
2. [Structure](#structure)
	1. [Parsing](#parsing)
	2. [Configuration](#configuration)
	3. [Generation](#generation)
	4. [Visualization](#visualization)
	5. [Tools](#tools)
3. [Features](#features)
	1. [Package Project](#package-project)
	2. [Code Reusability](#code-reusability)
	3. [Bonus Features](#bonus-features)
	4. [Project Management](#project-management)
4. [Team](#team)
	1. [Neuza](#neuza)
	2. [Rodrigo](#rodrigo)

# Introduction

Generate a Maze? We are going to build this from the ground up!

## Description

The A-Maze-Ing Project asks us to implement a maze generator in Python that takes a configuration file in order to generate a maze, possibly perfect (with a single path between entrance and exit), and writes it to a output file of the user's name choice, using a hexadecimal wall representation. Provididing a visual representation of the maze as well.

## Instructions

It is best to install the UV dependency manager in order to use the provided Makefile, a requirements.txt is also found at the root of the repository in case UV cannot be used, and in that case run the following commands to install the dependencies for the project:
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

	If your python version is not python 3.14.0, the python command may not be usable, so instead use python3. 

The Makefile provided can be used to:  
 - Install
 - Run
 - Build
 - Debug
 - Lint

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

Both the *lint* and *lint-strict* instructions will call uv to run mypy and flake8, if the lint-strict instruction is used, mypy will be executed with the --strict flag. We use uv to run these tools in order that the 'missing-imports' warn doesn't show up since that could be a misleading warn if the dependencies are all installed. UV is cannot be used, calling either `python -m flake8/mypy .` or `flake8/mypy .` will work as well.

The *build* and *debug* instructions are stricly for building the whells and tar file asked by the subject and helping to debug the code found here. They shouldnt be used unless for those that maintain this project

## Resources

AI was used to do shit here, 

# Structure
## Parsing
## Configuration
## Generation
## Visualization
## Tools

# Features
## Package Project
## Code Reusability
## Bonus Features
## Project Management

# Team
## Neuza
## Rodrigo
