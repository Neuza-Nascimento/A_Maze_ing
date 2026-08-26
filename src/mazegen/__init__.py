# src/mazegen/__init__.py

"""Mazegen Package.

This init.py grants access to the:
    MagicValues Enum
    MazeConfig Class
    MazeGenerator Class
    MazeVisualizer Class
"""

from .magic_values import MagicValues
from .maze_config import MazeConfig
from .maze_generator import MazeGenerator
from .maze_visualizer import MazeVisualizer

__all__: list[str] = ["MagicValues", "MazeConfig", "MazeGenerator", "MazeVisualizer"]
