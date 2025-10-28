#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""This script orchestrates the file conformation process."""

import subprocess


def main() -> None:
    """Reads a list of files and runs the conformation script on each."""
    with open("python_files.txt") as f:
        files = f.readlines()

    for file in files:
        file = file.strip()
        if file:
            print(f"--- Conforming {file} ---")
            subprocess.run(["python3", "conform.py", file])


if __name__ == "__main__":
    main()

# 🐍🏗️🔚
