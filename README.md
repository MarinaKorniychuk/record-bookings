# record-bookings

A PyQT desktop application to record profits and expenses to Google spreadsheet.

## Installation

run the following command in command line:

```sh
pip install requirements.txt
```

## Basic Usage


1. To authorize Google Sheets:

   Create a developer account and create credentials for service account. These credentials give the python script access to a Google account ([instruction](https://pygsheets.readthedocs.io/en/stable/authorization.html#oauth-credentials)).
2. Download `.json` file with a service account and copy it to `secret/desktop_client_secret.json` file in the project.
3. Bnova credentials need to be set in clients/bnova_client.py

```sh
python main.py
```
