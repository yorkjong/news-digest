"""
RSS feed generation for news digestion
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/04/21 (initial version) ~ 2023/04/21 (last revision)"

__all__ = [
    'rss_from_lines',
]

import sys
import re
import pytz
from datetime import datetime
from feedgen.feed import FeedGenerator
import clip
import hashtag


def rss_from_lines(lines, name=''):
    '''Get RSS string from the lines of markdown text.

    Args:
        lines ([str]): lines of markdown text.
        name (str): name of the RSS feed.

    Returns:
        (str): RSS string.

    '''
    fg = FeedGenerator()
    fg.title(f'news-digest ({name})')
    fg.author({'name': 'York Jong', 'email': 'york.jong@gmail.com'})
    fg.id(f'https://news-digest.vercel.app/{name}') # for ATOM feed only
    fg.link(href='https://news-digest.vercel.app', rel='alternate')
    fg.description(f'Feed of news-digest ({name})')

    fg.language('zh-TW')
    pst = pytz.timezone('Asia/Taipei')
    now = datetime.now(pst)
    fg.updated(now)

    for line in lines:
        if line.startswith('### '):
            heading = line.strip('# ')
        elif line.startswith('- ['):
            title = re.search(r'\[(.+)\]\(', line).group(1)
            url = re.search(r'\]\((.+)\)', line).group(1)
            tags = re.search(r'\) +(#.+)', line).group(1)
            fe = fg.add_entry(order='append')
            fe.id(url)  # for ATOM feed only
            fe.title(title)
            fe.link(href=url)
            fe.description(f'{title} {tags}')
            fe.category(term=heading, label=heading)

    return fg.rss_str(pretty=True).decode('utf-8')


def main():
    topices = [t.strip() for t in sys.argv[1].split(',')]
    headings = [topice for topice in topices if not topice.startswith('#')]
    tags = [topice for topice in topices if topice.startswith('#')]
    name = sys.argv[2]
    content = clip.get_latest_journal()
    categories = headings
    if not categories and tags:
        categories = clip.get_categories(content)
    if tags:
        lines = clip.get_lines_of_categories(categories, content, True, True)
        lines = hashtag.get_lines_with_any_hashtags(lines, tags)
    else:
        lines = clip.get_lines_of_categories(categories, content, True, True)
    print(rss_from_lines(lines, name))


if __name__ == '__main__':
    main()

