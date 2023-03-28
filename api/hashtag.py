"""
Hashtag querying
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/03/24 (initial version) ~ 2023/03/28 (last revision)"

__all__ = [
    'get_hashtags',
    'get_lines_with_any_hashtags',
    'get_lines_with_all_hashtags',
]


import re


def get_hashtags(lines):
    '''Gets all hastags for given markdown lines.

    Args:
        lines (List[str]): a list of lines of markdown text.

    Returns:
        (List[str]): a list of hashtags.
    '''
    tags = set()
    for line in lines:
        if line.startswith('- ['):
            tags |= set(re.findall(r'\s+(#[\S]+)', line))
    tags = list(tags)
    return sorted(tags)


def hedear_links_lines(header, link_lines):
    if not link_lines:
        return []
    lines = []
    if header:
        lines.append(header)
    lines += link_lines
    return lines


def get_lines_with_any_hashtags(lines, query_tags):
    '''Get lines that have at least one of the specified query hashtags.

    Args:
        lines (List[str]): a list of lines of markdown text.
        query_tags (List[str]): a list of hashtags to query.

    Returns:
        (List[str]): a list of lines having at least one of query hashtags.
    '''
    def is_line_with_any_hashtags(line):
        line_tags = re.findall(r'\s+(#[\S]+)', line)
        for t in line_tags:
            if t in query_tags:
                return True
        return False

    lines = [line.strip() for line in lines]
    header, link_lines, out_lines = '', [], []

    for line in lines:
        if line.startswith('- ###'):
            line = line[2:]
        if line.startswith('###'):
            out_lines.extend(hedear_links_lines(header, link_lines))
            header, link_lines = line, []
        elif line.startswith('- [') and is_line_with_any_hashtags(line):
            link_lines.append(line)
        elif line in ('', '-'):
            out_lines.extend(hedear_links_lines(header, link_lines))
            if header:
                out_lines.append('')
            header, link_lines = '', []
    out_lines.extend(hedear_links_lines(header, link_lines))

    return out_lines


def get_lines_with_all_hashtags(lines, query_tags):
    '''Get lines that have all of the specified query hashtags.

    Args:
        lines (List[str]): a list of lines of markdown text.
        query_tags (List[str]): a list of hashtags to query.

    Returns:
        (List[str]): a list of lines containing all query hashtags.
    '''
    def is_line_with_all_hashtags(line):
        line_tags = re.findall(r'\s+(#[\S]+)', line)
        return query_tags.issubset(line_tags)

    lines = [line.strip() for line in lines]
    header, link_lines, out_lines = '', [], []
    query_tags = set(query_tags)

    for line in lines:
        if line.startswith('- ###'):
            line = line[2:]
        if line.startswith('###'):
            out_lines.extend(hedear_links_lines(header, link_lines))
            header, link_lines = line, []
        elif line.startswith('- [') and is_line_with_all_hashtags(line):
            link_lines.append(line)
        elif line in ('', '-'):
            out_lines.extend(hedear_links_lines(header, link_lines))
            if header:
                out_lines.append('')
            header, link_lines = '', []
    out_lines.extend(hedear_links_lines(header, link_lines))

    return out_lines


def main():
    import clip
    content = clip.merge_recent_journals(3)
    lines = clip.get_lines_of_categories(
                ['AI', 'Tesla', 'Tech'], content, with_hashtags=True)

    print('\n'.join(get_lines_with_any_hashtags(lines, ['#OpenAI', '#ChatGPT'])))
    print(f"{'-'*80}")
    print('\n'.join(get_lines_with_all_hashtags(lines, ['#NVDA', '#semicon'])))


if __name__ == '__main__':
    main()

