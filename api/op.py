"""
Operations (e.g., difference, union, merge) of links between news journal files.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/03/23 (initial version) ~ 2023/03/24 (last revision)"

__all__ = [
    'diff_markdown',
]


def parse_markdown(lines):
    """
    Parses the markdown file into a dictionary where the keys are header strings
    and the values are lists of link strings.

    Args:
        lines (list): a list of lines of a markdown content.

    Returns:
        ({str:[str]}): a header-links dictionary.
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


def build_diff_header_links(old_header_links, new_header_links):
    """
    Builds the diff of the header links between the two markdown files. This is
    done by iterating over the headers and comparing the link lists of each.

    Args:
        old_header_links ({str:[str]}): header-links dictionary of old markdown.
        new_header_links ({str:[str]}): header-links dictionary of new markdown.

    Returns:
        ({str:[str]}): the diff of header links.
    """
    diff_header_links = {}
    for header in old_header_links:
        if header in new_header_links:
            old_links = old_header_links[header]
            new_links = new_header_links[header]
            link_diff = [link for link in new_links if link not in old_links]
            if link_diff:
                diff_header_links[header] = link_diff
    return diff_header_links


def build_markdown_text(header_links):
    """
    Builds the markdown file from the header links dictionary.

    Args:
        header_links ({str:[str]}): a header-links dictionary.

    Returns:
        (str): the markdown text.
    """
    markdown = ''
    for header, links in header_links.items():
        markdown += f'{header}\n'
        for link in links:
            markdown += f'{link}\n'
        markdown += '\n'
    return markdown


def diff_markdown(old_lines, new_lines):
    '''Get diff of two news-items markdown text.

    Args:
        old_lines ([str]): a list of lines of the old markdown file.
        new_lines ([str]): a list of lines of the new markdown file.

    Returns:
        ([str]): a list of lines listing link-items in old markdown not in
        new one.
    '''
    old_header_links = parse_markdown(old_lines)
    new_header_links = parse_markdown(new_lines)
    diff = build_diff_header_links(old_header_links, new_header_links)
    return build_markdown_text(diff)


def main():
    with open('test_data/old.md', 'r') as old:
        old_lines = old.readlines()
    with open('test_data/new.md', 'r') as new:
        new_lines = new.readlines()

    md = diff_markdown(old_lines, new_lines)
    print(md)


if __name__ == '__main__':
    main()

