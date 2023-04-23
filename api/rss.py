"""
This module define handler of a Vercel's serverless function.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/04/23 (initial version) ~ 2023/04/23 (last revision)"

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from . import clip, hashtag, feed


def rss(headings, tags, name):
    content = clip.get_latest_journal()
    categories = headings
    if not categories and tags:
        categories = clip.get_categories(content)
    if tags:
        lines = clip.get_lines_of_categories(categories, content, True, True)
        lines = hashtag.get_lines_with_any_hashtags(lines, tags)
    else:
        lines = clip.get_lines_of_categories(categories, content, True, True)
    return feed.rss_from_lines(lines, name)


# NOTE: must name "handler" (call-back class)
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)

        headings = params.get('heading', ['Tesla', 'Tech', 'Finance'])
        tags = [f"#{t}" for t in params.get('tag', [])]

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(rss(headings, tags, f"api/rss?{query}").encode())


def test():
    # Start the HTTP server on port 8080
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print('Starting server...')
    httpd.serve_forever()


if __name__ == '__main__':
    test()

