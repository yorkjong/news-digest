"""
The module implement a Vercel Serverlesss Function to subscrip topics of news.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/05/04 (initial version) ~ 2023/05/06 (last revision)"

__all__ = [
    'handler',
]

import os
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import JSONDecodeError
import requests

try:
    from .gdrive import Drive, TokenTable, Subscriptions
except:
    from gdrive import Drive, TokenTable, Subscriptions


#------------------------------------------------------------------------------
# Token Status (Line Notify)
#------------------------------------------------------------------------------

def token_status(token):
    '''Check status of a Line Access Token.

    Args:
        token (str): line access token

    Returns:
        (dict): a dictionary of the reponsed JSON
    '''
    url = 'https://notify-api.line.me/api/status'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    resp = requests.get(url, headers=headers)
    try:
        return resp.json()
    except JSONDecodeError:
        print('Response could not be serialized')
        return {}


def token_target(token):
    '''Get target of a Line Access Token.

    Args:
        token (str): line access token

    Returns:
        (str): the target (e.g., the user name or the group name)
    '''
    return token_status(token).get('target', '')


#------------------------------------------------------------------------------
# handler of the Vercel serverless function
#------------------------------------------------------------------------------

class handler(BaseHTTPRequestHandler):
    '''handler of the Vercel Serverless Function.

    Note: The class name must be handler.
    '''

    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)

        token = params.get('token', [''])[0]
        target = token_target(token)

        if not target:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Invalid access token')
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        daily_topics = (
            ("Tesla & SpaceX; Vehicle", ""),
            ("Tech Industry", ""),
            ("Finance", ""),
            ("Taiwan", ""),
            ("Crypto", ""),
            ("IT", " (AI, Software)"),
        )
        weekly_topics = (
            ("Science & Technology", " (Weekly)"),
        )
        n_options = len(daily_topics) + len(weekly_topics)

        options_daily = "\n".join(
            f"{' '*12}<option value='{t}'>{t}{c}</option>" for t, c in daily_topics)
            #f"{' '*12}<option value='{t}' selected>{t}{c}</option>" for t, c in daily_topics)
        options_weekly = "\n".join(
            f"{' '*12}<option value='{t}'>{t}{c}</option>" for t, c in weekly_topics)
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Subscription to news-digest (token: {token})</title>
            <style>
                #topics {{
                    height: {n_options+2}em;
                }}
            </style>
        </head>
        <body>
            <h1>Subscription to news-digest</h1>
            <form method="post" action="/api/subscribe">
                <label for="topics">Choose topics:</label><br/><br/>
                <select name="topics" id="topics" multiple>
        {options_daily}
        {options_weekly}
                </select>
                <input type="hidden" name="token" value="{token}">
                <input type="hidden" name="target" value="{target}"><br/><br/>
                <input type="submit" value="Subscribe">
            </form>
        </body>
        </html>
        """
        self.wfile.write(html_body.encode())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        post_params = parse_qs(post_data.decode())

        topics = post_params.get('topics', [])
        token = post_params.get('token', [''])[0]
        target = post_params.get('target', [''])[0]

        if target:
            tok_tbl = TokenTable('access_tokens.yml')
            target = tok_tbl.add_item(token, target)
            tok_tbl.save()

            weekly = ["Science & Technology"]
            topics_daily = [t for t in topics if t not in weekly]
            topics_weekly = [t for t in topics if t in weekly]

            subscriptions_d = Subscriptions('subscriptions_Daily.yml')
            subscriptions_d.update_topics(target, topics_daily)
            subscriptions_d.save()
            subscriptions_w = Subscriptions('subscriptions_Weekly.yml')
            subscriptions_w.update_topics(target, topics_weekly)
            subscriptions_w.save()

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        html_topics = "\n".join(f"{' '*8}<li>{topic}</li>" for topic in topics)
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Subscription Result (token: {token})</title>
        </head>
        <body>
            <h1>Thanks for subscribing!</h1>
            <p>target: {target}</p>
            <p>token: {token}</p>
            <p>You have subscribed to the following topics:</p>
            <ul>
        {html_topics}
            </ul>
        </body>
        </html>
        """
        self.wfile.write(html_body.encode())


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
    test()

