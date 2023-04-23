from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


def rss(topices, name):
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


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)
        topices = params.get('topice', ['Tesla', 'Tech', 'Finance'])

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(rss(topices, f"api/rss?{query}"))

