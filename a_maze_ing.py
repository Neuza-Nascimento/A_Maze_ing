import sys
from parsing import parsing


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: pyhton3 a_maze_ing.py <file>.txt")
        sys.exit(1)
    file: str = sys.argv[1]
    try:
        config = parsing(file)
        print(config)
    except FileNotFoundError as e:
        print(f"Error Opening File: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Value Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
