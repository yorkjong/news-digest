"""
Utility functions for clipping news of news-digest site.
"""
__software__ = "News Clip"
__version__ = "1.0"
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/03/20 (initial version) ~ 2023/03/21 (last revision)"

__all__ = [
    'get_sublist',
    'get_latest_fn',
    'get_file',
    'get_categories',
    'get_lines_of_category',
    'get_lines_of_categories',
    'send_to_line_notify',
]

import requests
import re


# Assign GitHub repository and path of "journals" folder
repo = "YorkJong/news-digest"
path = "journals"


#------------------------------------------------------------------------------
# Utility
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


def split_string(input_str, max_chars=1000):
    """
    Splits a string into substrings based on a maximum character limit per
    substring and the occurrence of '\n' characters.

    Args:
        input_str (str): The string to be split.
        max_chars (int): The maximum number of characters per substring.

    Returns:
        A list of substrings, where each substring has at most 'max_chars'
        characters and ends with a '\n' character, if one is present.
    """
    result = []
    start = 0
    end = max_chars
    while end < len(input_str):
        # Find the last occurrence of '\n' before the current 'end' position
        index = input_str.rfind('\n', start, end)
        if index != -1:
            # If '\n' is found, set 'end' to the position after '\n'
            end = index + 1
        # Add the substring between 'start' and 'end' to the result list
        result.append(input_str[start:end].strip())
        start = end
        end += max_chars
    # Add the last substring to the result list
    result.append(input_str[start:].strip())
    return result


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
        lines = [re.sub(r'\s*#\[\[\S+\]\]', '', line) for line in lines]
        lines = [re.sub(r'\s*#[\w/]+', '', line) for line in lines]
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
# Line Notify
#------------------------------------------------------------------------------

def _send_to_line_notify(msg, token):
    '''Send a message to a chat room via Line Notify.

    Args:
        msg (str): message to send
        token (str): line access token
    '''
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}

    # send the message
    r = requests.post(url, headers=headers, params=payload)


def send_to_line_notify(msg, token, max_chars=1000):
    '''Send a messae to a chat room via Line Notify.
    This function will split a message to sub-message with the `max_chars`
    limit.

    Args:
        msg (str): message to send
        token (str): line access token
        max_chars (int): The maximum number of characters per sub-message.
    '''
    msgs = split_string(msg, max_chars)
    for m in msgs:
        _send_to_notify(m, token)


#------------------------------------------------------------------------------
# Test
#------------------------------------------------------------------------------

def test():
    fn = get_latest_fn(path)
    content = get_file(fn)
    print(f'{get_categories(content)}\n\n')

    content = get_file(fn)
    lines = get_lines_of_category('Taiwan', content)
    print('\n'.join(lines))


if __name__ == '__main__':
    test()

