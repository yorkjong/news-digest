"""
Hashtag querying
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/03/24 (initial version) ~ 2023/03/27 (last revision)"

__all__ = [
    'get_hashtags',
    'get_lines_with_any_hashtag',
    'get_lines_with_all_hashtags',
]


import re


def get_hashtags(lines):
    '''Gets all hastags for given markdown lines.

    Args:
        lines ([str]): a list of lines of markdown text.

    Returns:
        ([str]): a list of hashtags.
    '''
    tags = set()
    for line in lines:
        if line.startswith('- ['):
            tags |= set(re.findall(r'\s+(#[\S]+)', line))
    tags = list(tags)
    return sorted(tags)


def get_lines_with_any_hashtag(lines, query_tags):
    '''Gets lines with any hashtag in given guery hashtags.

    Args:
        lines ([str]): a list of lines of markdown text.
        query_tags ([str]): a list of hashtags to query.

    Retruns:
        ([str]): a list of lines with any given hashtags.
    '''
    def is_line_with_any_hashtag(line):
        line_tags = re.findall(r'\s+(#[\S]+)', line)
        for t in line_tags:
            return t in query_tags
        return False

    out_lines = []

    for line in lines:
        if not line.startswith('- ['):
            out_lines.append(line)
            continue
        if is_line_with_any_hashtag(line):
            out_lines.append(line)

    return out_lines


def get_lines_with_all_hashtags(lines, query_tags):
    '''Gets lines with all given hashtags.

    Args:
        lines ([str]): a list of lines of markdown text.
        query_tags ([str]): a list of hashtags to query.

    Retruns:
        ([str]): a list of lines with all given hashtags.
    '''
    def is_line_with_all_hashtags(line):
        line_tags = re.findall(r'\s+(#[\S]+)', line)
        return query_tags.issubset(line_tags)

    out_lines = []
    query_tags = set(query_tags)

    for line in lines:
        if not line.startswith('- ['):
            out_lines.append(line)
            continue
        if is_line_with_all_hashtags(line):
            out_lines.append(line)

    return out_lines


def main():
    import clip
    content = clip.merge_recent_journals(3)
    lines = clip.get_lines_of_categories(
                ['AI', 'Tesla', 'Tech'], content, with_hashtags=True)

    print('\n'.join(get_lines_with_any_hashtag(lines, ['#OpenAI', '#ChatGPT'])))
    print(f"{'-'*80}\n")
    print('\n'.join(get_lines_with_all_hashtags(lines, ['#NVDA', '#semicon'])))


if __name__ == '__main__':
    main()

