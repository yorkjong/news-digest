"""
The module implement a Vercel Serverlesss Function to generate a RSS feed.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/04/23 (initial version) ~ 2023/05/08 (last revision)"

__all__ = [
    'handler',
]

import os
import sys
import glob
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

if __name__ == '__main__':
    sys.path.append('../src')
else:
    # on Vercel environment
    sys.path.append(os.path.join(os.getcwd(), 'src'))

import clip, hashtag, feed


#------------------------------------------------------------------------------
# Utility Functions
#------------------------------------------------------------------------------

def get_latest_journal_filename():
    '''Get the filename (YYYY_MM_DD.md) of the latest jurnal.

    Returns:
        (str): the filename with latest date.
    '''
    files = glob.glob(r"????_??_??.md")
    return max(files)


def get_latest_journal():
    '''Get the content of latest journal.

    Returns:
        (str): the conetent of latest journal.
    '''
    fn = get_latest_journal_filename()
    with open(fn, 'r') as f:
        text = f.read()
    return text

#------------------------------------------------------------------------------

def rss(headings, tags, name):
    '''Generate the content of subsdripted RSS feed.

    Args:
        headings ([str]): a list of headings to subscrip
        tags ([str]): a list of tags to subscrip
        name (str): name of the RSS.

    Returns:
        (str): the generated content of RSS feed
    '''
    #content = clip.get_latest_journal()
    content = get_latest_journal()
    categories = headings
    if not categories and tags:
        categories = clip.get_categories(content)
    if tags:
        lines = clip.get_lines_of_categories(categories, content, True, True)
        lines = hashtag.get_lines_with_any_hashtags(lines, tags)
    else:
        lines = clip.get_lines_of_categories(categories, content, True, True)
    return feed.rss_from_lines(lines, name)


#------------------------------------------------------------------------------
# handler of a Vercel serverless function
#------------------------------------------------------------------------------

class handler(BaseHTTPRequestHandler):
    '''handler of the Vercel Serverless Function.

    Note: The class name must be handler.
    '''
    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)

        headings = params.get('heading', ['Tesla', 'Tech', 'Finance'])
        tags = [f"#{t}" for t in params.get('tag', [])]

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(rss(headings, tags, f"api/rss?{query}").encode())

#------------------------------------------------------------------------------
# Test
#------------------------------------------------------------------------------

def test():
    # Start the HTTP server on port 8080
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, handler)
    print('Starting server...')
    httpd.serve_forever()


if __name__ == '__main__':
    import sys
    sys.path.append('../src')

    test()

