"""Entry point for the 23 November 2026 news image.

Copies the pre-drawn entry.png (made by draw_image.py) into the output
directory. Standard library only: no drawing happens at grade time.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(source, target)
    size = os.path.getsize(target)
    print("copied", source, "->", target, "(%d bytes)" % size)


if __name__ == "__main__":
    main()
