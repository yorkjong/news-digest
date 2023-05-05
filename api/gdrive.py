"""
The module implement operations of files in a folder in the Google Drive.
"""
__author__ = "York <york.jong@gmail.com>"
__date__ = "2023/05/05 (initial version) ~ 2023/05/05 (last revision)"

__all__ = [
    'Drive',
    'TokenTable',
    'Subscriptions',
]

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
        '''Load a token table from a YAML file.

        Args:
            filename (str): the filename of the token table.
        '''
        self.filename = filename
        self.table = Drive().load_YAML(filename)

    def save(self):
        '''Save the token table back to the original YAML file.
        '''
        Drive().save_YAML(self.table, self.filename)

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


class Subscriptions:
    '''Operations of a news-digest subscription table.
    '''
    def __init__(self, filename="subscriptions_Daily.yml"):
        '''
        Load a subscriptions from a YAML file.

        Args:
            filename (str): the filename of the token table.
        '''
        self.filename = filename
        self.table = Drive().load_YAML(filename)

    def save(self):
        '''Save the subscriptions back to the original YAML file.
        '''
        Drive().save_YAML(self.table, self.filename)

    def all_clients(self):
        '''Get all clients in subscriptions.

        Returns:
            (set): all clients.
        '''
        all = set()
        for topics, clients in self.table:
            all |= set(clients)
        return all

    def update_topics(self, client, new_topics):
        '''Update subscribed topics for a client.

        This method add topics listing in new_topics and remove topics not
        listing in new_tpoics.

        Args:
            client (str): the client.
            new_topics ([str]): a list of topics.
        '''
        for topics, clients in self.table:
            if topics[0] in new_topics:
                if client not in clients:
                    clients.append(client)
            else:
                if client in clients:
                    clients.remove(client)

    def add_item(self, heading, client):
        '''Add an item to subscriptions.

        Args:
            heading (str): heanding to subscribe.
            client (str): target name of a client.
        '''
        for topics, clients in self.table:
            if len(topics) != 1:
                continue
            if topics[0] == heading and client not in clients:
                clients.append(client)

    def remove_clients(self, clients_rm):
        '''Remove clients in the subscriptions.

        Args:
            clients_rm ([str]): a list of clients to remove.
        '''
        for _, clients in self.table:
            diff = set(clients) - set(clients_rm)
            if len(clients) > len(diff):
                # update clients
                clients[:] = list(diff)

    def remove_invalids(self, valid_clients):
        '''Remove invalid clients in the subscriptions.

        Args:
            valid_clients ([str]): a list of clients to keep.
        '''
        for _, clients in self.table:
            coms = set(clients) & set(valid_clients)
            if len(clients) > len(coms):
                # update clients
                clients[:] = list(coms)


def test_Drive():
    drive = Drive()
    assert id(Drive()) == id(drive)
    assert id(drive._file_table) == id(Drive._file_table)
    print(f"{drive._file_table.keys()}\n")

    fn = 'access_tokens.yml'
    tokens = drive.load_YAML(fn)
    print("{tokens}\n\n")
    drive.save_YAML(tokens, fn)


def test_TokenTable():
    tbl = TokenTable('access_tokens.yml')
    #tbl.save()
    tbl.add_item('TOKEN_OF_ANDY', 'Andy')
    tbl.add_item('TOKDN_OF_CINDY', 'Cindy')
    print(f"{tbl.table}\n")
    tbl.remove_tokens(['TOKEN_OF_ANDY', 'TOKDN_OF_CINDY'])
    print(f"{tbl.table}\n\n")


def test_Subscriptions():
    tbl = Subscriptions('subscriptions_Daily.yml')
    valid_clients = tbl.all_clients()
    #tbl.save()
    print(f"{tbl.table}\n")
    tbl.add_item('IT', 'Andy')
    tbl.add_item('Crypto', 'Tina')
    print(f"{tbl.table}\n")
    tbl.remove_invalids(valid_clients)
    #tbl.remove_clients(['Andy', 'Tina', '55688'])
    print(f"{tbl.table}\n")
    tbl.update_topics('55688', ['IT', 'Finance'])
    print(f"{tbl.table}\n\n")


def main():
    #test_Drive()
    #test_TokenTable()
    test_Subscriptions()


if __name__ == '__main__':
    main()

