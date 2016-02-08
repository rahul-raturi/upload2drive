#!/usr/bin/env python2

from __future__ import print_function
from apiclient import discovery, errors
from apiclient.http import MediaFileUpload
import oauth2client as ocli
import httplib2
import os
from os import path
import sys
import argparse

class UploadData(object):

    def __init__(self):
        self.home_dir = path.expanduser('~')
        self.config_dir = path.join(self.home_dir, '.config/upload2drive')
        self.credentials_path = path.join(self.config_dir, 'credentials.json')

    def upload_data(self, file_path, service):
        media = MediaFileUpload(file_path)
        metadata = {'name': path.basename(file_path)}
        try:
            f_obj = service.files()
            response = f_obj.create(media_body=media, body=metadata).execute()
            return response
        except errors.HttpError, error:
            print("Something didn't happened right:", error)
            return None

    def get_credentials(self):
        credentials = ocli.file.Storage(self.credentials_path).get()
        if not credentials or credentials.invalid:
            print("Credentials not found or have expired. Please execute intialize_drive.py.", file=sys.stderr)
            return None 
        return credentials 

def main(files):
    handle = UploadData()
    credentials = handle.get_credentials() 
    if not credentials:
        sys.exit(1)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    for fp in files:
        if not os.path.exists(fp):
            print("File does not exists: ", os.path.abspath(fp), file=sys.stderr)
        else:
            response = handle.upload_data(path.abspath(fp), service)
            print("File uploaded successfully!")
            print(response)

if __name__ == '__main__':
    flags = argparse.ArgumentParser()
    flags.add_argument("files", nargs='*')
    args = flags.parse_args()
    main(args.files)
