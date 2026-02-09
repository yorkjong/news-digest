import sys
import re
import os

def clean_titles(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    cleaned_lines = []

    # Identify links: [Title](Url)
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    # List of regex replacements for title cleanup (executed in order)
    # Strategy: Conservative Approach
    # Only remove patterns that are highly likely to be metadata/source info

    replacements = [
        # --- Suffixes ---
        # Pipe separator: " | TechNews", " | iThome" (matches " | " and anything after)
        # This is generally safe as titles rarely use " | " for content
        (re.compile(r'\s\|\s.*$'), ''),

        # Pipe separator without spaces (often tags): "|Tag1|Tag2"
        # Matches a pipe followed by non-pipe chars, repeated at the end
        # Example: ...規則|AI文本生成|语义|模型|系统|工程
        (re.compile(r'\|[^|]+(?:\|[^|]+)+$'), ''),

        # Underscore separators (commonly used in Chinese sites like Sina, Tencent)
        # Risk: Some titles might use underscore. But usually it's a separator.
        (re.compile(r'_[^_]+$'), ''),

        # Specific high-confidence dash patterns
        # Matches " - " followed by "News", "新聞", "網", ".com" etc.
        (re.compile(r'\s-\s.*(新聞|網|News|Report|Times|Daily|\.com).*$'), ''),

        # Specific known trailing strings (no space)
        (re.compile(r'-51CTO\.COM$'), ''),
        (re.compile(r'-腾讯新闻$'), ''),
        (re.compile(r'-新浪财经$'), ''),
        (re.compile(r'-CSDN博客$'), ''),
        (re.compile(r'-知乎$'), ''),

        # --- Prefixes ---
        # Brackets at the start: 【Source】 Title
        (re.compile(r'^【[^】]+】\s*'), ''),

        # Square brackets at the start: [Source] Title
        # Risk: [Tags] might be useful content. But usually it's source/category.
        # We can limit the length to avoid cutting long "[How to do X...]" prefixes
        (re.compile(r'^\[[^\]]{1,15}\]\s*'), ''),
    ]

    def modify_title(match):
        title = match.group(1)
        url = match.group(2)

        original_title = title
        current_title = title

        for pattern, replacement in replacements:
            current_title = pattern.sub(replacement, current_title)

        # Safety check: If title became empty or too short (< 2 chars), revert to original
        if len(current_title.strip()) < 2:
            return f"[{original_title}]({url})"

        return f"[{current_title.strip()}]({url})"

    for line in lines:
        new_line = link_pattern.sub(modify_title, line)
        cleaned_lines.append(new_line)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)
        print(f"Successfully processed {file_path}")
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 clean_titles.py <file_path>")
        sys.exit(1)

    clean_titles(sys.argv[1])
