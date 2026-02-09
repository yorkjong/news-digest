import sys
import re
import urllib.parse
import os

def clean_links(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    new_lines = []
    # Regex for timestamp: - **HH:MM** [[quick capture]]:
    # Matches starting with optional whitespace, dash, whitespace, bold time, whitespace, [[quick capture]], colon, whitespace.
    timestamp_pattern = re.compile(r'^\s*-\s*\*\*\d{1,2}:\d{2}\*\*\s*\[\[quick capture\]\]:\s*')

    # Regex for markdown links: [text](url)
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    def decode_match(m):
        text = m.group(1)
        url = m.group(2)
        try:
            # Unquote the URL to decode percent-encoded characters (like Chinese)
            decoded_url = urllib.parse.unquote(url)
            return f"[{text}]({decoded_url})"
        except Exception:
            return m.group(0) # Return original if decode fails

    for line in lines:
        # 1. Remove timestamp prefix
        match = timestamp_pattern.match(line)
        if match:
             # Replace the match with "- " to keep it as a list item
             cleaned_line = timestamp_pattern.sub('- ', line, count=1)
        else:
             cleaned_line = line

        # 2. Decode URLs
        cleaned_line = link_pattern.sub(decode_match, cleaned_line)

        new_lines.append(cleaned_line)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Successfully processed {file_path}")
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 clean_links.py <file_path>")
        sys.exit(1)

    clean_links(sys.argv[1])
