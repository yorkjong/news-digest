---
description: Process the daily news digest (Clean, Tag, Organize)
---

// turbo-all

This workflow automates the daily news digest process, intelligently designed to avoid macOS sandbox boundaries by running Python scripts only on internal workspace files.

1. **Ensure Daily Journal Exists**
   Run the script to make sure today's journal entry exists (creates `journals/YYYY_MM_DD.md`).
   // turbo
   Command: `python3 .agent/skills/ensure_daily_journal/ensure_journal.py`

2. **Clean Link Titles**
   Use the `clean_link_titles` skill to remove extraneous metadata from the link titles in `../notes/pages/TempLinks.md`.

3. **Add Hashtags**
   Use the `add_hashtags` skill to analyze content and append tags to the links in `../notes/pages/TempLinks.md`.

4. **Organize to Journal**
   Use the `organize_links_to_journal` skill to categorize and move the links from `TempLinks.md` to today's daily journal file (e.g., `journals/2026_03_18.md`).
   
5. **Clean Journal Links (Formatting)**
   Use the `clean_temp_links` script to fix formatting (remove timestamps) and decode URLs in the newly written journal file.
   // turbo
   Command: `python3 .agent/skills/clean_temp_links/clean_links.py "journals/$(date +%Y_%m_%d).md"`

6. **Clear Temp Links**
   Since `TempLinks.md` is outside the workspace and Python scripts trigger sandbox permission errors, use your internal Agent tools (`write_to_file` with empty content) to clear `../notes/pages/TempLinks.md`.
