
from sys import exit, argv
from parsing import parsing


def main() -> None:
    if len(argv) != 2:
        print("Usage: pyhton3 a_maze_ing.py <file>.txt")
        exit(1)
    file: str = argv[1]
    try:
        config = parsing(file)
        print(config)
    except FileNotFoundError as e:
        print(f"Error Opening File: {e}")
        exit(1)
    except ValueError as e:
        print(f"Configuration Error: {e}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
