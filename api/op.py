"""
Operations (e.g., difference, union) of links between markdown lines with a
sequence of heading:links structures.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/03/23 (initial version) ~ 2023/04/09 (last revision)"

__all__ = [
    'diff_links',
    'union_links',
]

from typing import List, Dict


def parse_markdown(lines: List[str]) -> Dict[str, List[str]]:
    """
    Parses the lines of a markdown text into a dictionary where the keys are
    heading strings and the values are lists of link strings.

    Args:
        lines: A list of lines of a markdown text.

    Returns:
        A dictionary where the keys are heading strings and the values are lists
        of link strings from the given markdown text.
    """
    heading_links = {}
    heading = None
    for line in lines:
        if line.startswith('- ### '):
            line = line[2:]
        if line.startswith('### '):
            heading = line.strip()
            heading_links[heading] = []
        elif line.startswith('- ['):
            link = line.strip()
            heading_links[heading].append(link)
    return heading_links


def diff_heading_links(dict1, dict2):
    """
    Builds the difference (subtraction) of two dictionaries that map headings
    to lists of links in markdown text.

    Args:
        dict1 ({str:[str]}): The first dictionary that maps headings to lists
            of links.
        dict2 ({str:[str]}): The second dictionary that maps headings to lists
            of links.

    Returns:
        ({str:[str]}): A dictionary that maps headings to the difference
        (subtraction) of their corresponding lists of links between the two
        input dictionaries.
    """
    diff = {}
    for heading in dict1:
        if heading in dict2:
            links1 = dict1[heading]
            links2 = dict2[heading]
            link_diff = [link for link in links1 if link not in links2]
            if link_diff:
                diff[heading] = link_diff
    return diff


def union_heading_links(dict1, dict2):
    """
    Builds the union of two dictionaries that map headings to lists of links in
    markdown text.

    Args:
        dict1 ({str:[str]}): The first dictionary that maps headings to lists
            of links.
        dict2 ({str:[str]}): The second dictionary that maps headings to lists
            of links.

    Returns:
        ({str:[str]}): A dictionary that maps headings to the union of their
        corresponding lists of links between the two input dictionaries.
    """
    union = {}
    #heading_links = dict1 | dict2
    heading_links = {**dict1, **dict2}
    for heading in heading_links:
        if heading in dict1 and heading in dict2:
            links1 = dict1[heading]
            links2 = dict2[heading]
            link_union = links1[:]
            link_union += [link for link in links2 if link not in links1]
            if link_union:
                union[heading] = link_union
        else:
            union[heading] = heading_links[heading]
    return union


def build_markdown_lines(heading_links: Dict[str, List[str]]) -> List[str]:
    """
    Builds the markdown lines from a heading:links dictionary.

    Args:
        heading_links (Dict[str, List[str]]): a heading:links dictionary.

    Returns:
        List[str]: the lines of the built markdown text.
    """
    lines = []
    for heading, links in heading_links.items():
        if not links:
            continue
        lines += [f'{heading}']
        for link in links:
            lines += [f'{link}']
        lines += ['']
    return lines


def diff_links(lines1: List[str], lines2: List[str]) -> List[str]:
    '''Get difference (subtraction) of links for two markdown lines. Each
    markdown contains a sequence of heading-with-links.

    Args:
        lines1 ([str]): 1st sequence of lines of a links markdown text.
        lines2 ([str]): 2nd sequence of lines of a links markdown text.

    Returns:
        ([str]): the difference of the two lines of heading-with-links sequence.
    '''
    dict1 = parse_markdown(lines1)
    dict2 = parse_markdown(lines2)
    diff = diff_heading_links(dict1, dict2)
    return build_markdown_lines(diff)


def union_links(lines1: List[str], lines2: List[str]) -> List[str]:
    '''Get union of links for two markdown lines. Each markdown contains a
    sequence of heading-with-links.

    Args:
        lines1 ([str]): 1st sequence of lines of a links markdown text.
        lines2 ([str]): 2nd sequence of lines of a links markdown text.

    Returns:
        ([str]): the union of the two lines of heading-with-links sequence.
    '''
    dict1 = parse_markdown(lines1)
    dict2 = parse_markdown(lines2)
    union = union_heading_links(dict1, dict2)
    return build_markdown_lines(union)


def main():
    with open('test_data/new.md', 'r') as f1:
        lines1 = f1.readlines()
    with open('test_data/old.md', 'r') as f2:
        lines2 = f2.readlines()

    lines = diff_links(lines1, lines2)
    print('\n'.join(lines))

    print(f"\n{'-'*80}\n")

    lines = union_links(lines1, lines2)
    print('\n'.join(lines))


if __name__ == '__main__':
    main()

