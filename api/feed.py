"""
RSS/ATOM feed generator for news digestion
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/04/21 (initial version) ~ 2023/04/21 (last revision)"

import re
import pytz
from datetime import datetime
import clip
from feedgen.feed import FeedGenerator


content = clip.get_latest_journal()
lines = content.split('\n')

fg = FeedGenerator()
fg.title('Feed of my news digestion')
fg.author({'name': 'York Jong', 'email': 'york_jong@gmail.com'})
fg.id('https://news-digest.vercel.app') # for ATOM feed only
fg.link(href='https://news-digest.vercel.app/feed.xml', rel='alternate')
fg.description('Feed of my news digestion')

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
        fe = fg.add_entry()
        fe.id(url)  # for ATOM feed only
        fe.title(title)
        fe.link(href=url)
        fe.description(f'{title} {tags}')
        fe.category(term=heading, label=heading)
        #fe.content(title, type='html')

#fg.rss_file('feed.xml', pretty=True)
#print(fg.atom_str(pretty=True).decode('utf-8'))
print(fg.rss_str(pretty=True).decode('utf-8'))

