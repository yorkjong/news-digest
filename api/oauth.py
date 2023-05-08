"""
The module implement a Vercel Serverlesss Function to authorize Line Notify.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/05/04 (initial version) ~ 2023/05/08 (last revision)"

__all__ = [
    'handler',
]

import os
import secrets
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler

import requests

HOME_URL = "https://news-digest.vercel.app"
REDIRECT_URI = f"{HOME_URL}/api/oauth"


class handler(BaseHTTPRequestHandler):
    '''handler of the Vercel Serverless Function.

    Note: The class name must be handler.
    '''

    def do_GET(self):
        os.environ['STATE'] = secrets.token_hex(16)
        auth_params = {
            'response_type': 'code',
            'scope': 'notify',
            'response_mode': 'form_post',
            'redirect_uri': REDIRECT_URI,
            'client_id': os.environ['CLIENT_ID'],
            'state': os.environ['STATE']
        }
        params = '&'.join([f'{k}={v}' for k, v in auth_params.items()])
        url = f"https://notify-bot.line.me/oauth/authorize?{params}"
        self.send_response(302)
        self.send_header('Location', url)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        params = parse_qs(post_data)

        state = params.get('state', [''])[0]
        STATE = os.environ.get('STATE', '')
        if state != STATE:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid state parameter')
            return

        code = params.get('code', [''])[0]
        token_params = {
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': os.environ['CLIENT_ID'],
            'client_secret': os.environ['CLIENT_SECRET'],
            'code': code
        }
        url = 'https://notify-bot.line.me/oauth/token'
        response = requests.post(url, data=token_params)
        token = response.json().get('access_token', '')

        self.send_response(302)
        self.send_header('Location', f"{HOME_URL}/api/subscribe?token={token}")
        self.end_headers()

