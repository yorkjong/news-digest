---
name: clean_temp_links
description: Removes timestamps and decodes URLs in the specified markdown file.
---

# Clean Temp Links

This skill cleans up a markdown file (specifically designed for `TempLinks.md` or similar "quick capture" lists).
It performs two main operations:
1.  **Remove Timestamp**: Strips the `- **HH:MM** [[quick capture]]:` prefix from lines.
2.  **Decode URLs**: Converts formatting like `%E5%...` back to readable Unicode characters (e.g., Chinese).

## Inputs
- `file_path`: The absolute path to the markdown file to clean.

## Usage
Run the following command in the terminal:
`python3 .agent/skills/clean_temp_links/clean_links.py "{file_path}"`

## Example
**Input:**
`- **17:25** [[quick capture]]: [Example](https://example.com/%E6%B8%AC%E8%A9%A6)`

**Output:**
`- [Example](https://example.com/測試)`
