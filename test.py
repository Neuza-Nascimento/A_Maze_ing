import sys
from pathlib import Path

from dotenv import dotenv_values, find_dotenv


def main() -> None:
    filename = sys.argv[1]
    file = Path(filename)
    raw: dict[str, str] = {}

    contents = file.read_text(encoding="utf-8")
    for line in contents.split("\n"):
        if line.startswith(("#", "\n")):
            continue
        if not line.strip():
            continue
        if "=" not in line:
            serr: str = "Invalid Syntax"
            raise SyntaxError(serr)

        key, value = line.split("=", 1)
        key = key.strip().upper()
        value = value.strip()
        raw[key] = value
    print(raw)


if __name__ == "__main__":
    main()
