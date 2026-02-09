---
name: ensure_daily_journal
description: Checks if the daily journal file exists for a given date. If not, creates it using the 'Daily framework' template.
---

# Ensure Daily Journal

This skill ensures that the Logseq journal file for a specific date exists.

## Inputs
- `date`: (Optional) The date string in `YYYY_MM_DD` format. Defaults to the current local date.

## Steps

1.  **Determine Target Date**
    - usage: `date` argument or current date.
    - format: `YYYY_MM_DD` (e.g., `2026_02_09`).

2.  **Check File Existence**
    - Check if `journals/{date}.md` exists.
    - **IF EXISTS**: Return success (Content already exists).

3.  **Read Template (If File Missing)**
    - Read `pages/templates.md`.
    - Parse the markdown to find the block named `Daily framework` with property `template:: Daily framework`.
    - Extract the *children* blocks of this template.
    - **Logic**: Since `template-including-parent:: false` is used, extract only the nested list items, removing one level of indentation.

4.  **Create Journal File**
    - Write the extracted content to `journals/{date}.md`.
    - Ensure the content is formatted as valid Logseq markdown (list items).

## Example Action
`ensure_daily_journal(date="2026_02_09")` -> ensures `journals/2026_02_09.md` exists.
