#!/usr/bin/env python3

import json
import sys
from pathlib import Path
import subprocess

from .converter import MarkdownToDocx


def main():
    if len(sys.argv) != 2:
        print(
            f"Usage: {Path(sys.argv[0]).name} input.md | config.json",
            file=sys.stderr,
        )
        return 2

    try:
        converter = MarkdownToDocx()
        input_path = Path(sys.argv[1])

        if input_path.suffix.lower() == ".json":
            output = converter.convert_config(input_path)
        else:
            output = converter.convert(input_path)

        print(f"Created: {output}")
        return 0

    except (
        OSError,
        RuntimeError,
        ValueError,
        json.JSONDecodeError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
