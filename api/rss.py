from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import clip
import hashtag
import feed


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
    return feed.rss_from_lines(lines, name)


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)
        headings = params.get('heading', ['Tesla', 'Tech', 'Finance'])
        tags = params.get('tag', [])

        hashtags = [f"#{t}" for t in tags]
        topices = headings + hashtags

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(rss(topices, f"api/rss?{query}").encode())


def test():
    # Start the HTTP server on port 8080
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print('Starting server...')
    httpd.serve_forever()


if __name__ == '__main__':
    test()

