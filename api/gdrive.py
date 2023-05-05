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
        '''Support singleton pattern.
        '''
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

        Args:
            service_account_info (str): a string representing service account info.

        Returns:
            service object of Google Drive API client.
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
        '''Create the file table of a foldr.

        Args:
            folder_id (str): the ID of a folder.

        Returns:
            ({filename: file_id}): the file table to map a filename to a file
                ID.
        '''
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
        '''Load a YAML file from the folder of the Google Dirve.

        Args:
            filename (str): the filename of a YAML file.

        Returns:
            the Python object.
        '''
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
        '''Save a Python object to YAML on the folder of the Google Drive.

        Args:
            data: a Python object to save.
            filename (str): the filename of a YAML file.
        '''
        file_id = cls._file_table[filename]

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


class TokenTable:
    '''Operations to map a target (a user or a group) to a Line Notify token.
    '''
    def __init__(self, filename="access_tokens.yml"):
        self.table = Drive().load_YAML(filename)

    def add_item(self, token, target):
        """Add an item to the access_token table.

        Args:
            token (str): a token of Line Notify.
            target (str): target name of the token.

        Returns
            (str): the new name of target.
        """
        targets = list(self.table.keys())
        tokens = list(self.table.values())

        if target in targets and token not in tokens:
            prog = re.compile(f'{re.escape(target)}(_\d+)?$')
            d = sum(not not prog.match(t) for t in targets)
            target = f"{target}_{d}"
        elif target not in targets and token in tokens:
            i = tokens.index(token)
            target = targets[i]
        elif target in targets and token in tokens:
            if self.table[target] != token:
                i = tokens.index(token)
                target = targets[i]

        self.table[target] = token
        return target

    def remove_tokens(self, tokens=[]):
        '''Remove tokens in the table.

        Args:
            tokens ([str]): a list of tokens.
        '''
        targets = []
        for target, token in self.table.items():
            if token in tokens:
                targets.append(target)

        for target in targets:
            del self.table[target]


def test_Drive():
    drive = Drive()
    assert id(Drive()) == id(drive)
    assert id(drive._file_table) == id(Drive._file_table)
    print(drive._file_table.keys())

    fn = 'access_tokens.yml'
    tokens = drive.load_YAML(fn)
    print(tokens)
    drive.save_YAML(tokens, fn)


def test_TokenTable():
    tbl = TokenTable('access_tokens.yml')
    tbl.add_item('TOKEN_OF_ANDY', 'Andy')
    tbl.add_item('TOKDN_OF_CINDY', 'Cindy')
    print(tbl.table)
    tbl.remove_tokens(['TOKEN_OF_ANDY', 'TOKDN_OF_CINDY'])
    print(tbl.table)


def main():
    #test_Drive()
    test_TokenTable()


if __name__ == '__main__':
    main()

