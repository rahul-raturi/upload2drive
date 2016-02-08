Upload files to Google Drive from console
=========================================

A python script to upload data to Drive from console without hassle.


Requirements
------------

Check whether your system meets the following requirements before executing.

* python >= 2.7 (Not 3)
* Google's apiclient library for python.
Here: https://developers.google.com/api-client-library/python/start/installation
* Your own client_secret key. Apparantly Google doesn't recommends sharing client_secret keys.
Here's how to get the key: https://developers.google.com/api-client-library/python/guide/aaa_apikeys


Setting things up
-----------------

* Create a folder in *~/.config* with name upload2drive
* Put your client_secret.json in there.

Using
-----

* First allow the script to access your drive. To do so type:

	$ python2 access_drive.py

* To upload [a] file[s], type:

	$ python2 u2d.py /home/user/file.txt another_file.txt

One can specify absolute or relative path for uploading the file.
