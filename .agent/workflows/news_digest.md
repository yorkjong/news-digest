---
description: Process the daily news digest (Clean, Tag, Organize)
---

This workflow automates the daily news digest process.

1. **Ensure Daily Journal Exists**
   Run the script to make sure today's journal entry exists.
   // turbo
   Command: `python3 .agent/skills/ensure_daily_journal/ensure_journal.py`

2. **Clean Temp Links (Formatting)**
   Run the script to fix formatting and decode URLs in the temp file.
   // turbo
   Command: `python3 .agent/skills/clean_temp_links/clean_links.py "../notes/pages/TempLinks.md"`

3. **Clean Link Titles**
   Use the `clean_link_titles` skill to remove extraneous metadata from the link titles in `../notes/pages/TempLinks.md`.

4. **Add Hashtags**
   Use the `add_hashtags` skill to analyze content and append tags to the links in `../notes/pages/TempLinks.md`.

5. **Organize to Journal**
   Use the `organize_links_to_journal` skill to categorize and move the links from `TempLinks.md` to today's daily journal file.

6. **Clear Temp Links**
   Clear the temporary links file after processing is complete.
   // turbo
   Command: `python3 .agent/skills/clear_file/clear_file.py "../notes/pages/TempLinks.md"`
