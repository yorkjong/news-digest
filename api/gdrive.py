"""
The module implement operations of files in a folder in the Google Drive.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/05/05 (initial version) ~ 2023/05/05 (last revision)"


import os
import io
import json
import yaml

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError


class Drive:
    """Provide operations of files in "news-digest" folder in the Google Drive.
    """
    _instance = None    # for singleton pattern
    _service = None     # service client of Google Drive API
    _file_table = None  # map finename to file ID

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._service = cls._client(os.environ['SERVICE_ACCOUNT_INFO'])
            cls._file_table = cls._file_table(os.environ['FOLDER_ID'])
        return cls._instance

    def __init__(self):
        pass

    @staticmethod
    def _client(service_account_info):
        '''Create service client of Google Drive API.
        '''
        info = json.loads(service_account_info)

        # Create Credentials object
        creds = service_account.Credentials.from_service_account_info(
            info,
            scopes=['https://www.googleapis.com/auth/drive']
        )

        # Create a Drive API client
        return build('drive', 'v3', credentials=creds)

    @classmethod
    def _file_table(cls, folder_id):
        query = f"trashed = false and '{folder_id}' in parents"
        fields = "nextPageToken, files(id, name)"
        results = cls._service.files().list(q=query, fields=fields).execute()
        items = results.get("files", [])

        fn2id = {}
        for item in items:
            fn2id[item['name']] = item['id']
        return fn2id

    @classmethod
    def load_YAML(cls, filename):
        file_id = cls._file_table[filename]

        # Download file content from Google Drive
        try:
            file = cls._service.files().get(fileId=file_id).execute()
            content = cls._service.files().get_media(fileId=file_id).execute()
            if content:
                # Convert YAML text to Python object
                data = yaml.safe_load(content)
            else:
                print('File is empty.')
        except HttpError as error:
            print('An error occurred: %s' % error)
            data = None
        return data

    @classmethod
    def save_YAML(cls, data, filename):
        file_id = cls._file_table[filename]

        # Modify the content and upload it to Google Drive
        if data:
            # Convert the Python object to YAML
            updated_content = yaml.safe_dump(data, default_flow_style=False)

            # Upload the modified content to Google Drive
            try:
                media = MediaIoBaseUpload(
                    io.BytesIO(updated_content.encode()),
                    mimetype='application/x-yaml')

                cls._service.files().update(
                    fileId=file_id,
                    media_body=media,
                    fields='id'
                ).execute()
            except HttpError as error:
                print('An error occurred: %s' % error)


def test():
    drive = Drive()
    assert id(Drive()) == id(drive)
    assert id(drive._file_table) == id(Drive._file_table)
    print(drive._file_table.keys())

    fn = 'access_tokens.yml'
    tokens = drive.load_YAML(fn)
    print(tokens)
    drive.save_YAML(tokens, fn)


if __name__ == '__main__':
    test()

