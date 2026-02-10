---
name: clean_link_titles
description: Removes extraneous information (source, author, etc.) from link titles using LLM intelligence.
---

# Clean Link Titles

This skill uses an LLM to intelligently clean news link titles by removing unnecessary metadata such as source names, author names, and site branding, while preserving the core headline.

## Execution Instructions for AI
1.  **Read Source**: Read the list of links (usually in `TempLinks.md`).
2.  **Analyze Titles**: For each link `[Title](URL)`, identify and remove extraneous suffixes or prefixes.
3.  **Preserve Core Content**: Ensure the main news headline remains intact. Do NOT summarize or rewrite the headline; only remove metadata.

## Cleaning Rules
- **Remove Suffixes**:
    - remove ` | SiteName` (e.g., ` | TechNews`, ` | iThome`, ` - MoneyDJ`).
    - remove ` - Source Name` (especially if it looks like a brand).
    - remove `(Source)` at the end.
- **Remove Prefixes**:
    - remove `【Source】` or `[Source]` if it's clearly a publisher tag.
    - remove `Author Name:` if present at start.
- **Handle Edge Cases**:
    - If the "suffix" is actually part of the meaning (e.g., "Review | Product Name"), keep it. Context matters.
    - If unsure, bias towards keeping text to avoid losing information.

## Example
**Input:**
`- [NVIDIA stock jumps 5% | CNBC](...)`
`- [【TechCrunch】OpenAI releases new model](...)`
`- [Review: iPhone 16 | The Verge](...)`

**Output:**
`- [NVIDIA stock jumps 5%](...)`
`- [OpenAI releases new model](...)`
`- [Review: iPhone 16](...)`
