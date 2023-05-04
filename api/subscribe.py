"""
The module implement a Vercel Serverlesss Function to subscrip topics of news.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/05/04 (initial version) ~ 2023/05/04 (last revision)"

__all__ = [
    'handler',
]

import requests
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler
from json import JSONDecodeError


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

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
        	<title>News Subscription Form</title>
        </head>
        <body>
        	<h1>News Subscription Form</h1>
        	<form method="post" action="/api/subscribe">
        		<label for="topics">Choose topics:</label>
        		<select name="topics" id="topics" multiple>
        			<option value="Finance">Finance</option>
        			<option value="Tesla">Tesla</option>
        			<option value="Crypto">Crypto</option>
        			<option value="IT">IT</option>
        			<option value="Taiwan">Taiwan</option>
        		</select>
        		<input type="hidden" name="token" value="{token}">
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

        # 處理訂閱信息
        # TODO: 在這裡加上訂閱處理的代碼

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
        	<title>News Subscription Form {token}</title>
        </head>
        <body>
        	<h1>Thanks for subscribing!</h1>
        	<p>You have subscribed to the following topics:</p>
        	<ul>
        """

        for topic in topics:
            html_body += f"<li>{topic}</li>"

        html_body += """
        	</ul>
        </body>
        </html>
        """

        self.wfile.write(html_body.encode())

