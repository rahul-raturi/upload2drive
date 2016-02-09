#!/usr/bin/env python2

from __future__ import print_function
from apiclient import discovery
from oauth2client import client, tools
import oauth2client as ocli
import httplib2
import os
import sys

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError, e:
    print(e)
    sys.exit(1)
    

class AuthorizeApp(object):
    """Authorize application to access Drive."""

    _SCOPE = 'https://www.googleapis.com/auth/drive'
    _CLIENT_SECRET_FILE = 'client_secret.json'
    _APP_NAME = 'upload2drive: Upload Files to Drive'

    def __init__(self):
        self.home_dir = os.path.expanduser('~')
        self.config_dir = os.path.join(self.home_dir, '.config/upload2drive')
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        self.credentials_path = os.path.join(self.config_dir, 'credentials.json')
        self.client_secret_file_path = os.path.join(self.config_dir, AuthorizeApp._CLIENT_SECRET_FILE)
        if not os.path.exists(self.client_secret_file_path):
            print("Client's secret file not found. Read README.md for more information.", file=sys.stderr)

    def check_credentials(self):
        credentials_store = ocli.file.Storage(self.credentials_path)
        credentials = credentials_store.get()
        return credentials
 
    def get_credentials(self):
	credentials = self.check_credentials()	
	if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.client_secret_file_path, \
                    AuthorizeApp._SCOPE)
            flow.user_agent = AuthorizeApp._APP_NAME
            credentials = tools.run_flow(flow, credentials_store, flags)
        return credentials


if __name__ == "__main__":
    credentials = AuthorizeApp().get_credentials()
    if not credentials:
        print("Credentials mismatch or not found! Try running script again", file=sys.stderr)
    else:
        print("Credentials saved. Now upload any file using u2d script.")

