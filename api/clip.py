"""
Utility functions for clipping news of news-digest site.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/03/20 (initial version) ~ 2023/03/23 (last revision)"

__all__ = [
    'get_sublist',
    'get_latest_fn',
    'get_file',
    'get_categories',
    'get_lines_of_category',
    'get_lines_of_categories',
]

import requests
import re


# Assign GitHub repository and path of "journals" folder
repo = "YorkJong/news-digest"
path = "journals"


#------------------------------------------------------------------------------
# Utility Functions
#------------------------------------------------------------------------------

def get_sublist(all, first, last):
    '''Get a subset of a list of given range.

    Args:
        all (list): The lsit of all items
        first (str): first item you want
        last (str): last item you want

    Returns:
        ([str]) The subset between [first last]

    Examples
        >>> get_sublist(list('abcdefg'), 'b', 'd')
        ['b', 'c', 'd']
    '''
    ret = []
    trigger = False
    for item in all:
        if item == first:
            trigger = True
        if trigger:
            ret += [item]
        if item == last:
            break
    return ret



#------------------------------------------------------------------------------
# Functions for news-digest
#------------------------------------------------------------------------------

def get_latest_fn(path):
    '''Get the filename with latest date.

    Args:
        path (str): the path of journals folder to store YYYY_MM_DD.md files.

    Returns:
        (str): the filename with latest date.
    '''
    api_url = f"https://api.github.com/repos/{repo}/contents/{path}"

    # Request to the GitHub API to get all the archives under the journal folder
    response = requests.get(api_url)
    if response.status_code == 200:
        content = response.json()
        pattern = r'^\d{4}_\d{2}_\d{2}\.md$'
        date_list = [f['name'] for f in content if re.match(pattern, f['name'])]

        # Find the filename with the latest date
        latest_date = max(date_list)
        #latest_date = sorted(date_list)[-1]
        return latest_date
    else:
        print(f"Error {response.status_code}: {response.reason}")
        return ""


def get_file(fn):
    '''Get a file content of the news-digest site.

    Args:
        fn (str): the filename to get.

    Returns:
        (str): the total content of the file.
    '''
    file_url = f"https://raw.githubusercontent.com/{repo}/main/{path}/{fn}"

    response = requests.get(file_url)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(f"Error {response.status_code}: {response.reason}")
    return ""


def get_categories(content):
    '''Get category names of the content of news-digest.

    Args:
        content (str): the content of a YYYY_MM_DD.md news file.

    Returns:
        ([str]): a list of categories (i.e., header texts).
    '''
    lines = content.split('\n')
    categorys = []
    tag = '### '
    for line in lines:
        if line.startswith(tag):
            categorys += [line[len(tag):]]
    return categorys


def get_lines_of_category(kind_name, content, with_hashtags=False):
    '''Get links of given kind.

    Args:
        kind_name (str): the header-text of a category.
        content (str): the content of a YYYY_MM_DD.md news file.
        with_hashtags (bool): decide if keep the hashtags.

    Returns:
        ([str]): a list of lines of news links with desired category.
    '''
    text = content

    header = kind_name
    if not header.startswith("### "):
        header = f'### {header}'

    if not with_hashtags:
        # Remove hashtags after each link
        lines = text.split('\n')
        lines = [re.sub(r'\s+#[\S]+', '', line) for line in lines]
        text = '\n'.join(lines)

    trigger = False
    lines = []
    for line in text.split('\n'):
        if header in line:
            trigger = True
            continue
        if line.startswith("###"):
            if trigger:
                break
        if trigger:
            lines += [line]
    return lines


def get_lines_of_categories(categories, content,
                            with_hashtags=False, with_headers=True):
    '''Gets lines of given categories.
    This will also show the category as headers.

    Args:
        categories ([str]): a sequence of categories to get lines.
        content (str): the content of a YYYY_MM_DD.md news file.
        with_hashtags (bool): decide if keep the hashtags.
        with_headers (bool): decide if keep the headers.

    Returns:
        ([str]): a list of lines of news links with desired categories.
    '''
    lines = []
    for category in categories:
        if with_headers:
            lines += [f'### {category}']
        lines += get_lines_of_category(category, content, with_hashtags)
    return lines


#------------------------------------------------------------------------------
# Test
#------------------------------------------------------------------------------

def test():
    fn = get_latest_fn(path)
    content = get_file(fn)
    print(f'{get_categories(content)}\n\n')

    content = get_file(fn)
    lines = get_lines_of_category('AI', content)
    print('\n'.join(lines))


if __name__ == '__main__':
    test()

