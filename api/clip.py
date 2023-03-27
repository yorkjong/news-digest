"""
News clipping by categories within single markdown journal text.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/03/20 (initial version) ~ 2023/03/27 (last revision)"

__all__ = [
    'get_all_journal_filenames',
    'get_recent_journal_filenames',
    'get_latest_journal_filename',
    'get_latest_journal',
    'get_journal',
    'merge_recent_journals',
    'get_categories',
    'get_lines_of_category',
    'get_lines_of_categories',
    'get_sublist',
]

import requests
import re

import op

#------------------------------------------------------------------------------
# Journals
#------------------------------------------------------------------------------

repo = "YorkJong/news-digest"   # repository
path = 'journals'               # path of "journals" folder


def get_all_journal_filenames():
    '''Get all filenames of journals.

    Returns:
        ([str]): a list of filenames with YYYY_MM_DD.md format.
    '''
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
        days (int): max number of the recent days.

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
    file_url = f"https://raw.githubusercontent.com/{repo}/main/{path}/{fn}"

    response = requests.get(file_url)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        print(f"Error {response.status_code}: {response.reason}")
    return ""

#------------------------------------------------------------------------------

def merge_recent_journals(days=7):
    '''Merge recent journal files.

    Args:
        days (int): max number of the recent days.

    Returns:
        (str): the total content of the files.
    '''
    fns = get_recent_journal_filenames(days)
    lines1 = []
    for fn in reversed(fns):
        lines2 = get_journal(fn).split('\n')
        lines1 = op.union_links(lines1, lines2)
    return '\n'.join(lines1)


#------------------------------------------------------------------------------
# Categories
#------------------------------------------------------------------------------

def get_categories(content):
    '''Get category names of the content of a news-digest journal.

    Args:
        content (str): the content of a YYYY_MM_DD.md news file.

    Returns:
        ([str]): a list of categories (i.e., header texts).
    '''
    lines = content.split('\n')
    categorys = []
    mark = '### '
    for line in lines:
        if line.startswith(mark):
            categorys += [line[len(mark):]]
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

    if not with_hashtags:
        # Remove hashtags after each link
        lines = text.split('\n')
        lines = [re.sub(r'\s+#[\S]+', '', line) for line in lines]
        text = '\n'.join(lines)

    trigger = False
    lines = []
    for line in text.split('\n'):
        # match the begin of a category
        if line.startswith('###') and category in line:
            trigger = True
            continue
        # match the end of a category
        if line.startswith("###"):
            if trigger:
                break
        # match a link-line
        if trigger and line.startswith('- ['):
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
        cate_lines = get_lines_of_category(category, content, with_hashtags)
        if not cate_lines:
            continue
        if with_headers:
            lines += [f'### {category}']
        lines += cate_lines
        lines += ['']
    return lines


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
# Test
#------------------------------------------------------------------------------

def test_get_latest_journalXX():
    print(get_latest_journal_filename())
    content = get_latest_journal()
    print(f'\n\n{get_categories(content)}\n')

def test_get_lines_of_categories():
    content = get_latest_journal()
    lines = get_lines_of_categories(('ABC', 'XYZ'), content)
    print('\n'.join(lines))
    print(f"{'-'*80}\n")
    lines = get_lines_of_categories(('AI', 'Tesla'), content)
    print('\n'.join(lines))

def test_get_merge_recent_journals():
    print(get_recent_journal_filenames(2))
    content = merge_recent_journals(2)
    print(f'\n\n{get_categories(content)}\n')
    print(content)

def main():
    test_get_latest_journalXX()
    print(f"{'-'*80}\n")
    test_get_lines_of_categories()
    print(f"{'-'*80}\n")
    test_get_merge_recent_journals()


if __name__ == '__main__':
    main()

