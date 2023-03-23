"""
Utility functions for clipping news of news-digest site.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/03/20 (initial version) ~ 2023/03/24 (last revision)"

__all__ = [
    'get_all_journal_filenames',
    'get_recent_journal_filenames',
    'get_latest_journal_filename',
    'get_latest_journal',
    'get_journal',
    'get_categories',
    'get_lines_of_category',
    'get_lines_of_categories',
    'get_sublist',
]

import requests
import re


# Assign GitHub repository and path of "journals" folder
repo = "YorkJong/news-digest"


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

def get_all_journal_filenames():
    '''Get all filenames of journals.

    Returns:
        ([str]): a list of filenames with YYYY_MM_DD.md format.
    '''
    path = 'journals'
    api_url = f"https://api.github.com/repos/{repo}/contents/{path}"

    # Request to the GitHub API to get all the archives under the journal folder
    response = requests.get(api_url)
    if response.status_code == 200:
        content = response.json()
        pattern = r'^\d{4}_\d{2}_\d{2}\.md$'
        return [f['name'] for f in content if re.match(pattern, f['name'])]
    else:
        print(f"Error {response.status_code}: {response.reason}")
        return []


def get_recent_journal_filenames(days=7):
    '''Get filenames of recent journals.

    Args:
        days (int): max number of the recently days.

    Returns:
        ([str]): a list of filenames with YYYY_MM_DD.md format.
    '''
    return sorted(get_all_journal_filenames())[-days:]


def get_latest_journal_filename():
    '''Get the filename (YYYY_MM_DD.md) of the latest jurnal.

    Returns:
        (str): the filename with latest date.
    '''
    return max(get_all_journal_filenames())


def get_latest_journal():
    '''Get the content of latest journal.
    '''
    fn = get_latest_journal_filename()
    return get_journal(fn)


def get_journal(fn):
    '''Get the content of a journal file.

    Args:
        fn (str): the filename to get.

    Returns:
        (str): the total content of the file.
    '''
    path = 'journals'
    file_url = f"https://raw.githubusercontent.com/{repo}/main/{path}/{fn}"

    response = requests.get(file_url)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(f"Error {response.status_code}: {response.reason}")
    return ""


def get_categories(content):
    '''Get category names of the content of a news-digest journal.

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


def get_lines_of_category(category, content, with_hashtags=False):
    '''Get links of given category.

    Args:
        category (str): the header-text of a category.
        content (str): the content of a YYYY_MM_DD.md news file.
        with_hashtags (bool): decide if keep the hashtags.

    Returns:
        ([str]): a list of lines of news links with desired category.
    '''
    text = content

    header = category
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

def main():
    print(get_recent_journal_filenames())
    print(get_latest_journal_filename())
    content = get_latest_journal()
    print(f'\n\n{get_categories(content)}\n')

    lines = get_lines_of_category('AI', content)
    print('\n'.join(lines))


if __name__ == '__main__':
    main()

