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


import json
import requests
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

        if not target(token):
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Invalid access token')
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(f"token: {token}".encode())

