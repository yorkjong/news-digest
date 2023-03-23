"""
Line Notify.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/03/23 (initial version) ~ 2023/03/23 (last revision)"

__all__ = [
    'notify_message',
]

import requests


#------------------------------------------------------------------------------
# Utility Functions
#------------------------------------------------------------------------------

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

    Examples:
        >>> s = '\n'.join(['1'*9, '2'*8, '3'*3, '4'*5])
        >>> split_string(s, 10)
        ['111111111\n', '22222222\n', '333\n44444']
        >>>  split_string(s, 5)
        ['11111', '1111\n', '22222', '222\n', '333\n', '44444']
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
        result.append(input_str[start:end])
        start = end
        end += max_chars
    # Add the last substring to the result list
    result.append(input_str[start:])
    return result


#------------------------------------------------------------------------------
# Line Notify
#------------------------------------------------------------------------------

def notify(msg, token):
    '''Send a notification to an 1-on-1 chat or a group.

    The Line Notify service has a limit of 1000 characters, and any message
    that exceeds this limit will be truncated and ignored.

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


def notify_message(msg, token, max_chars=1000):
    '''Send a notification to an 1-on-1 chat or a group.

    The Line Notify service has a limit of 1000 characters, and any message
    that exceeds this limit will be truncated and ignored.

    This function avoids the 1000 characters limit by splitting a long messages
    into multiple short messages.

    Args:
        msg (str): message to send
        token (str): line access token
        max_chars (int): The maximum number of characters per sub-message.
    '''
    msgs = split_string(msg, max_chars)
    for m in msgs:
        notify(f'\n{m}', token)


#------------------------------------------------------------------------------
# Test
#------------------------------------------------------------------------------

def test():
    s = '\n'.join(['1'*9, '2'*8, '3'*3, '4'*5])
    print(split_string(s, 10))
    print(split_string(s, 5))


if __name__ == '__main__':
    test()

