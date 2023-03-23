"""
Builds the diff of the header links between the two markdown files. This is
done by iterating over the headers and comparing the link lists of each.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/03/23 (initial version) ~ 2023/03/24 (last revision)"


def parse_markdown(lines):
    """
    Parses the markdown file into a dictionary where the keys are header strings
    and the values are lists of link strings.

    Args:
        lines (list): a list of lines of a markdown content.
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


def build_markdown_file(header_links):
    """
    Builds the markdown file from the header links dictionary.
    """
    markdown = ''
    for header, links in header_links.items():
        markdown += f'{header}\n'
        for link in links:
            markdown += f'{link}\n'
        markdown += '\n'
    return markdown


def main():
    with open('test_data/old.md', 'r') as old, open('test_data/new.md', 'r') as new:
        old_header_links = parse_markdown(old)
        new_header_links = parse_markdown(new)
    diff_header_links = build_diff_header_links(old_header_links, new_header_links)
    diff_markdown = build_markdown_file(diff_header_links)
    print(diff_markdown)


if __name__ == '__main__':
    main()

