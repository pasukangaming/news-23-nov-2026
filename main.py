#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261123 bounty.

Copies the pre-drawn front page, entry.png (drawn by draw_image.py from
the verified news of Monday 23 November 2026), to the output path the
grader reads. Standard library only, no network, no randomness: every run
writes the exact same bytes.
"""

import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    destination = os.path.join(out_dir, "entry.png")

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, destination)
    return 0


if __name__ == "__main__":
    sys.exit(main())
