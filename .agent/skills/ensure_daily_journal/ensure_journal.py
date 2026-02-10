
import os
import sys
import datetime
import re

def ensure_daily_journal(date_str=None):
    # Determine date
    if not date_str:
        date_str = datetime.datetime.now().strftime("%Y_%m_%d")

    # Paths
    # Script is in .agent/skills/ensure_daily_journal/
    # We need to go up 3 levels to reach project root (news-digest/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
    journals_dir = os.path.join(base_dir, "journals")
    templates_path = os.path.join(base_dir, "pages", "templates.md")
    journal_path = os.path.join(journals_dir, f"{date_str}.md")

    # Check if journal exists
    if os.path.exists(journal_path):
        print(f"Journal {date_str}.md already exists.")
        return

    print(f"Creating journal {date_str}.md...")

    # Read template
    if not os.path.exists(templates_path):
        print(f"Error: Templates file not found at {templates_path}")
        sys.exit(1)

    with open(templates_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    lines = template_content.split('\n')
    start_index = -1

    # 1. Find the block containing "template:: Daily framework"
    # The structure is:
    # - Daily framework
    #   template:: Daily framework
    #   template-including-parent:: false
    #   - ### Tesla...

    for i, line in enumerate(lines):
        if "template:: Daily framework" in line:
            # Found the property. Now find the parent block (the line starting with "- " above it)
            for j in range(i, -1, -1):
                if lines[j].strip().startswith("- "):
                    start_index = j
                    break
            break

    if start_index == -1:
        print("Error: 'Daily framework' template not found.")
        sys.exit(1)

    # 2. Extract children
    # We need to collect all lines that are *more indented* than the parent block,
    # until we hit a line with same or less indentation.

    parent_line = lines[start_index]
    # Calculate indent level: tabs count as 1 char usually, but let's just count leading whitespace
    # Logseq usually uses tabs or spaces. The file view showed tabs ("\t- ...").
    # We need to be careful with mixed indentation.
    # Let's count visual indentation? Or just raw string prefix.

    def get_indent(s):
        return len(s) - len(s.lstrip())

    parent_indent = get_indent(parent_line)

    content_lines = []

    for i in range(start_index + 1, len(lines)):
        line = lines[i]

        # Skip empty lines, but keep them if they are part of the content block?
        # Logseq might have empty lines. But usually bullet points.
        if not line.strip():
            continue

        current_indent = get_indent(line)

        # If indentation is same or less than parent, we are out of the block
        if current_indent <= parent_indent:
            break

        # Skip properties
        if "template::" in line or "template-including-parent::" in line:
            continue

        # Remove one level of indentation.
        # In the file view:
        # Parent: "- Daily framework" (0 indent)
        # Child: "\t- ### Tesla..." (1 tab indent)
        # We want "- ### Tesla..." (0 indent)

        # Heuristic: Remove the first occurrence of indent step (tab or 2 spaces)
        # Check what the indentation char is
        stripped = line.lstrip()
        leading_whitespace = line[:len(line) - len(stripped)]

        # If it starts with tab, remove one tab
        if leading_whitespace.startswith('\t'):
            content_lines.append(line[1:])
        # If it starts with 2 spaces, remove 2 spaces
        elif leading_whitespace.startswith('  '):
            content_lines.append(line[2:])
        else:
            # Fallback: just strip and hope it works (might lose nested structure)
            # But wait, we want to preserve nested structure of children.
            # If Child is \t- ..., Grandchild is \t\t- ...
            # We want Child: - ..., Grandchild: \t- ...
            # So stripping one level of indentation is correct.
            # Let's try to detect the indent of the *first* child we find
            content_lines.append(line.lstrip()) # Fallback for now, simple flattened list is better than broken

    # Refined extraction logic:
    # Re-scanning to find the first child's indentation and remove exactly that amount from all children

    final_lines = []
    base_child_indent = -1

    for i in range(start_index + 1, len(lines)):
        line = lines[i]
        if not line.strip(): continue

        current_indent = get_indent(line)
        if current_indent <= parent_indent: break
        if "template::" in line or "template-including-parent::" in line: continue

        if base_child_indent == -1:
            base_child_indent = current_indent

        # Remove base_child_indent from start
        if len(line) >= base_child_indent:
             final_lines.append(line[base_child_indent:])
        else:
             final_lines.append(line.lstrip())

    if not final_lines:
        # Fallback if extraction fails or empty
        print("Warning: Template content empty or extraction failed. Creating empty journal.")
        final_lines = ["- "]

    # Write to journal
    with open(journal_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(final_lines))

    print(f"Successfully created {journal_path}")

if __name__ == "__main__":
    target_date = sys.argv[1] if len(sys.argv) > 1 else None
    ensure_daily_journal(target_date)
