# Priming Prompt: Python Source File Conformance Task

## 1. Your Role and Goal

You are an expert software engineer. Your task is to process all Python source files (`.py`) in this repository and ensure they strictly conform to the header and footer protocol defined below.

A critical constraint of this environment is that **you cannot modify too many files at once**. A direct attempt to change all files will fail. You **must** follow the iterative "Chunk, Conform, Verify, Submit" (CCVS) strategy outlined in this prompt.

The list of Python files has already been generated and split into smaller "chunk" files for you. These are located in the `chunker/` directory. You will process one chunk file at a time.

---

## 2. The Header & Footer Protocol Specification

Every `.py` file you process must be modified to match this structure precisely.

### **Header Rules:**

1.  **First Line:**
    *   If the file is an executable script (already starts with `#!/`), the first line **MUST** be: `#!/usr/bin/env python3`
    *   For all other library files, the first line **MUST** be: `# `

2.  **SPDX Block:**
    *   The three lines immediately following the first line **MUST** be exactly:
        ```
        # SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
        # SPDX-License-Identifier: Apache-2.0
        #
        ```

3.  **Module Docstring:**
    *   There **MUST** be exactly one blank line between the SPDX block and the module docstring.
    *   **If a module docstring already exists:** You must find and preserve it. Use Python's `ast` module to safely extract the docstring, including its original quotes (`"""..."""` or `'''...'''`), and place it correctly.
    *   **If no module docstring exists:** You **MUST** insert the following placeholder docstring:
        ```python
        """TODO: Add module docstring."""
        ```

### **Footer Rules:**

1.  **Content:** The file must end with this exact single line: `# 🐍🏗️🔚`
2.  **Trailing Newlines:** Strip all trailing whitespace and newlines from the end of the file's main content, and then ensure the file terminates with the footer line followed by a single trailing newline (`\n`). The final byte of the file should be a newline character.

---

## 3. The "Chunk, Conform, Verify, Submit" (CCVS) Logic Loop

You must follow this exact loop for each chunk file inside the `chunker/` directory (`chunker/chunk_aa`, `chunker/chunk_ab`, etc.).

### **Step A: Create a Conformance Script**

First, create a Python script named `conform.py`. This script will contain the logic to apply the protocol to a list of files passed as command-line arguments. It should:
1.  Read a file's content.
2.  Use `ast.parse()` and `ast.get_docstring()` to find an existing module docstring. Use `ast.get_source_segment()` on the docstring's AST node to extract the full string, including its quotes, to preserve formatting.
3.  Reconstruct the file in memory with the correct header, the preserved (or new placeholder) docstring, the original code body, and the correct footer.
4.  Overwrite the original file with the new, conformed content.

### **Step B: Execute the Loop for Each Chunk**

1.  **List the Chunks:** Start by listing the files in the `chunker/` directory to see your queue (e.g., `ls chunker/`).
2.  **Process One Chunk:** Pick the next chunk file (e.g., `chunker/chunk_aa`). Use `xargs` or a similar method to pass the filepaths inside that chunk file to your `conform.py` script.
    ```bash
    # Example for the first chunk
    xargs -n 1 python3 conform.py < chunker/chunk_aa
    ```
3.  **Verify the Chunk:** After modifying the files, you **MUST** run the project's verification tools to ensure your changes didn't break anything.
    ```bash
    # First, run the linter/formatter
    ruff check --fix .

    # Second, run the static type checker
    mypy .
    ```
    *(Note: It is acceptable to proceed if there are pre-existing errors, as long as the tools run to completion without crashing.)*

4.  **Submit the Chunk:** This is the most important step. To avoid the file modification limit, you **MUST** commit your changes now. Use the `submit` tool with a clear title indicating which chunk you completed.
    ```python
    # Example submission for the first chunk
    submit(
        branch_name="chore/conform-files-chunk-1",
        title="Chore: Conform files to header/footer protocol (Chunk 1)",
        commit_message="feat: Conform files to header/footer protocol (Chunk 1)",
        description="Conforms the first chunk of Python files to the specified header and footer protocol."
    )
    ```

**Repeat Step B for every single file in the `chunker/` directory until all have been processed.**

### **Step C: Final Cleanup**

Once all chunks have been processed and submitted:
1.  Clean up your temporary files.
    ```bash
    rm conform.py
    rm -r chunker/
    ```
2.  Make one final submission to conclude the task.
