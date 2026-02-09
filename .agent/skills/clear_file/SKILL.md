---
name: clear_file
description: Empties the content of a specified file. Use with caution.
---

# Clear File Content

This skill clears all content from a file, effectively emptying it. This is typically used as a cleanup step (e.g., clearing `TempLinks.md` after links have been processed).

## Inputs
- `file_path`: Absolute path to the file to be cleared.

## Usage
Run the following command:
`python3 .agent/skills/clear_file/clear_file.py "{file_path}"`
