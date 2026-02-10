---
name: ensure_daily_journal
description: Checks if the daily journal file exists for a given date. If not, creates it using the 'Daily framework' template.
---

# Ensure Daily Journal

This skill ensures that the Logseq journal file for a specific date exists.

## Inputs
- `date`: (Optional) The date string in `YYYY_MM_DD` format. Defaults to the current local date.

## Usage
Run the following command:
`python3 .agent/skills/ensure_daily_journal/ensure_journal.py "{date}"`

- `date`: Optional. Target date (YYYY_MM_DD). Defaults to today.

## Example
`python3 .agent/skills/ensure_daily_journal/ensure_journal.py`
`python3 .agent/skills/ensure_daily_journal/ensure_journal.py 2026_02_10`
