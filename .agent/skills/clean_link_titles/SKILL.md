---
name: clean_link_titles
description: Removes extraneous information (source, author, etc.) from link titles in markdown files.
---

# Clean Link Titles

This skill cleans up the titles of markdown links by removing common suffixes that indicate the source, author, or site name.

## Inputs
- `file_path`: The absolute path to the markdown file to process.

## Supported Patterns (Conservative)
It removes only high-confidence patterns:

**Suffixes:**
- ` | SiteName` (e.g., ` | TechNews`)
- ` - Source` (Only if source contains "News", "新聞", "網", ".com" etc.)
- `_SourceName` (e.g., `_财经头条`)

**Prefixes:**
- `【Source】` (e.g., `【TechNews】`)
- `[Source]` (Length limited to < 15 chars to avoid removing content tags)

## Usage
Run the following command in the terminal:
`python3 .agent/skills/clean_link_titles/clean_titles.py "{file_path}"`

## Example
**Input:**
`- [Title | TechNews 科技新報](...)`
`- [【獨家】Title](...)`

**Output:**
`- [Title](...)`
`- [Title](...)`
