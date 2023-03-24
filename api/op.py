"""
Operations (e.g., difference, union, merge) of links between news journal files.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/03/23 (initial version) ~ 2023/03/24 (last revision)"

__all__ = [
    'diff_links',
    'union_links',
]


def parse_markdown(lines):
    """
    Parses the lines of a markdown text into a dictionary where the keys are
    header strings and the values are lists of link strings.

    Args:
        lines (list): a list of lines of a markdown text.

    Returns:
        ({str:[str]}): the header:links dictionary from given markdown text.
    """
    header_links = {}
    header = None
    for line in lines:
        if line.startswith('### '):
            header = line.strip()
            header_links[header] = []
        elif line.startswith('- ['):
            link = line.strip()
            header_links[header].append(link)
    return header_links


def diff_header_links(header_links1, header_links2):
    """
    Builds the difference (subtraction) of two header:links dictionary of
    markdown text.

    Args:
        header_links1 ({str:[str]}): 1st header:links dictionary of markdown text.
        header_links2 ({str:[str]}): 2nd header:links dictionary of markdown text.

    Returns:
        ({str:[str]}): the difference of the two header-links dictionaries.
    """
    diff = {}
    for header in header_links1:
        if header in header_links2:
            links1 = header_links1[header]
            links2 = header_links2[header]
            link_diff = [link for link in links1 if link not in links2]
            if link_diff:
                diff[header] = link_diff
    return diff


def union_header_links(header_links1, header_links2):
    """
    Builds the union of two header:links dictionary of markdown text.

    Args:
        header_links1 ({str:[str]}): 1st header:links dictionary of markdown text.
        header_links2 ({str:[str]}): 2nd header:links dictionary of markdown text.

    Returns:
        ({str:[str]}): the union of the two header:links dictionaries.
    """
    union = {}
    for header in header_links1:
        if header in header_links2:
            links1 = header_links1[header]
            links2 = header_links2[header]
            link_union = links1[:]
            link_union += [link for link in links2 if link not in links1]
            if link_union:
                union[header] = link_union
    return union


def build_markdown_text(header_links):
    """
    Builds the markdown file from a header:links dictionary.

    Args:
        header_links ({str:[str]}): a header:links dictionary.

    Returns:
        (str): the built markdown text.
    """
    markdown = ''
    for header, links in header_links.items():
        markdown += f'{header}\n'
        for link in links:
            markdown += f'{link}\n'
        markdown += '\n'
    return markdown


def diff_links(lines1, lines2):
    '''Get difference (subtraction) of links for two markdown lines. Each markdown
    contains a sequence of header-with-links.

    Args:
        lines1 ([str]): a sequence of lines of 1st markdown text.
        lines2 ([str]): a sequence of lines of 2nd markdown text.

    Returns:
        ([str]): the difference of the two lines of header-with-links sequence.
    '''
    header_links1 = parse_markdown(lines1)
    header_links2 = parse_markdown(lines2)
    diff = diff_header_links(header_links1, header_links2)
    return build_markdown_text(diff)


def union_links(lines1, lines2):
    '''Get union of links for two markdown lines. Each markdown contains a sequence
    of header-with-links.

    Args:
        lines1 ([str]): 1st sequence of lines of a links markdown text.
        lines2 ([str]): 2nd sequence of lines of a links markdown text.

    Returns:
        ([str]): the union of the two lines of header-with-links sequence.
    '''
    header_links1 = parse_markdown(lines1)
    header_links2 = parse_markdown(lines2)
    union = union_header_links(header_links1, header_links2)
    return build_markdown_text(union)


def main():
    with open('test_data/new.md', 'r') as f1:
        lines1 = f1.readlines()
    with open('test_data/old.md', 'r') as f2:
        lines2 = f2.readlines()

    md = diff_links(lines1, lines2)
    #md = union_links(lines1, lines2)
    print(md)


if __name__ == '__main__':
    main()

