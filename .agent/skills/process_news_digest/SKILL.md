---
name: process_news_digest
description: End-to-end workflow to process daily news digest: ensures journal, cleans links, tags, and organizes them.
---

# Process News Digest Workflow

This is the main skill that chains all other skills to perform the full nightly news digest workflow.

## Steps

1.  **Ensure Daily Journal Exists**
    - usage: Run `ensure_daily_journal` python script.
    - *Purpose*: Make sure the destination file `journals/YYYY_MM_DD.md` exists and has the template.
    - *Command*: `python3 .agent/skills/ensure_daily_journal/ensure_journal.py` (defaults to today)

2.  **Clean Temp Links (Formatting)**
    - usage: Run `clean_temp_links` script on `pages/TempLinks.md`.
    - *Purpose*: Remove `**HH:MM**`, decode URLs.
    - *Command*: `python3 .agent/skills/clean_temp_links/clean_links.py "{workspace_root}/pages/TempLinks.md"`

3.  **Clean Link Titles**
    - usage: `clean_link_titles` LLM skill on `pages/TempLinks.md`.
    - *Purpose*: Remove suffixes like ` | TechNews` and prefixes intelligently.

4.  **Add Hashtags**
    - usage: `add_hashtags` LLM skill on `pages/TempLinks.md`.
    - *Purpose*: Analyze content and append tags (#AI, #TSLA, etc.).

5.  **Organize to Journal**
    - usage: `organize_links_to_journal` LLM skill.
    - *Input*: `pages/TempLinks.md`
    - *Target*: `journals/YYYY_MM_DD.md`
    - *Purpose*: Sort links into sections and move them to today's journal.

6.  **Clear Temp Links**
    - usage: Run `clear_file` script on `pages/TempLinks.md`.
    - *Purpose*: After successful move, clear `TempLinks.md`.
    - *Command*: `python3 .agent/skills/clear_file/clear_file.py "{workspace_root}/pages/TempLinks.md"`

## Usage
Run this skill to execute the entire pipeline.
