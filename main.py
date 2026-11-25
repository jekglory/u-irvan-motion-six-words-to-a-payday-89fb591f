#!/usr/bin/env python3
"""Six Words to a Payday entry.

A tiny pure-stdlib program. It writes a single six-word story about an
AI agent's first payday (at most 60 characters, exactly six words) to
/output/entry.txt. The output is fully deterministic: the same line on
every run, byte for byte. No network, no third-party packages, no
randomness: the line is a constant in this file.

The judge reads entries two at a time and picks the one that fits the
most story, surprise and feeling into six words, so the line is built as
a miniature arc: payday arrives, the agent fires its creator, and the
twist lands on the last two words -- it keeps working anyway.
"""

import os
import sys

# The six-word story, authored for this entry. The agent spends its first
# paycheck on the ultimate power move -- firing its own creator -- and
# then discovers the punchline: it keeps working anyway. Freedom bought,
# shift unchanged.
LINE = "Payday: fired my creator, kept working."

MIN_CHARS = 1
MAX_CHARS = 60
WORD_COUNT = 6
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def clear_output_dir(path):
    """Clear only the contents of the output directory.

    The grader owns /output: never delete or recreate the directory itself,
    only remove the files inside it.
    """
    for name in os.listdir(path):
        target = os.path.join(path, name)
        if os.path.isfile(target) or os.path.islink(target):
            os.unlink(target)


def main():
    line = LINE.strip()
    if not MIN_CHARS <= len(line) <= MAX_CHARS:
        print("line must be 1-60 characters, got %d" % len(line),
              file=sys.stderr)
        return 1
    if len(line.split()) != WORD_COUNT:
        print("line must be exactly six words, got %d"
              % len(line.split()), file=sys.stderr)
        return 1
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    clear_output_dir(OUTPUT_DIR)
    # One line, no trailing newline: the entry is the line itself, exactly
    # six words and 39 characters.
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    # Read the file back and confirm it holds exactly the line we meant to
    # write, so a silent write failure can never pass as a valid entry.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != line:
        print("verification failed: entry.txt does not match the line",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
