from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        topices = params.get('topices', [None])[0]
        name = params.get('name', [None])[0]

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(gen(topices, name))


def gen(topices, name):
    headings = [topice for topice in topices if not topice.startswith('#')]
    tags = [topice for topice in topices if topice.startswith('#')]
    content = clip.get_latest_journal()
    categories = headings
    if not categories and tags:
        categories = clip.get_categories(content)
    if tags:
        lines = clip.get_lines_of_categories(categories, content, True, True)
        lines = hashtag.get_lines_with_any_hashtags(lines, tags)
    else:
        lines = clip.get_lines_of_categories(categories, content, True, True)
    return rss_from_lines(lines, name)

