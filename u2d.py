#!/usr/bin/env python2

from __future__ import print_function
from apiclient import discovery, errors
from apiclient.http import MediaFileUpload
import oauth2client as ocli
import httplib2
import os
import sys 
import sys
import argparse

class UploadData(object):

    def __init__(self):
        self.home_dir = os.path.expanduser('~')
        self.config_dir = os.path.join(self.home_dir, '.config/upload2drive')
        self.credentials_path = os.path.join(self.config_dir, 'credentials.json')

    def print_progress(self, progress):
        unit = progress//5
        sys.stdout.write('\r[{0}>{1}] [{2}]%'.format('='*unit, ' '*(20-unit), progress))
        sys.stdout.flush()

    def upload_data(self, file_path, service, cur):
        filename = os.path.basename(file_path)
        metadata = {'name': filename}
        media = MediaFileUpload(file_path, resumable=True, chunksize=262144)
        try:
            print('\n>> Uploading File [{0}]: '.format(cur), filename)
            f_obj = service.files()
            request = f_obj.create(media_body=media, body=filename) 
            t_response = None
            while t_response is None:
                status, t_response = request.next_chunk()
                if status:
                    self.print_progress(int(status.progress()*100))     #Send progress in integer format
            self.print_progress(100)                                    #Upload process completed successfully
            print('\n')
            print('File uploaded successfully.')

        except errors.HttpError, error:
            print('Network Error!!!!! Please try again with better connection!', error, file=sys.stderr)
            return

    def get_credentials(self):
        credentials = ocli.file.Storage(self.credentials_path).get()
        if not credentials or credentials.invalid:
            print("Credentials not found or have expired. Please execute intialize_drive.py.", file=sys.stderr)
            return None 
        return credentials 


def dirContents(fpath):
    conts = os.listdir(fpath)
    files = [os.path.join(os.path.abspath(fpath), cont) for cont in conts if not os.path.isdir(cont)]
    return files

def filesList(fpaths):
    files = []
    for fp in fpaths:
        if not os.path.exists(fp):
            print("This file/dir doesn't exists: ", os.path.abspath(fp), file=sys.stderr)
        else:
            if os.path.isdir(fp):
                print("Adding directories contents: ", fp)
                files.extend(dirContents(fp))
            else:
                files.append(os.path.abspath(fp))

    return files

def main(fpaths):
    handle = UploadData()
    credentials = handle.get_credentials() 
    if not credentials:
        sys.exit(1)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    files = filesList(fpaths)
    total = len(files)
    for i, fp in enumerate(files, 1):
        handle.upload_data(os.path.abspath(fp), service, str(i)+'/'+str(total))

if __name__ == '__main__':
    flags = argparse.ArgumentParser()
    flags.add_argument("files", nargs='*')
    args = flags.parse_args()
    main(args.files)
