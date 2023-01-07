# record-bookings

A script to transfers records from Bnova spreadsheet to Google spreadsheets.

## Installation

run the following command in command line:

```sh
pip install requirements.txt
```

## Basic Usage


1. To authorize google sheets:

   Create a developer account and create OAuth Client ID credentials for a Desktop application. These credentials give the python script access to a Google account ([instruction](https://pygsheets.readthedocs.io/en/stable/authorization.html#oauth-credentials)).
2. Download `.json` file with a client key and copy it to secret/desktop_client_secret.json file in the project.
3. Download spreadsheet from Bnova for desired period.

    _Note: Make sure to exclude records in 'cancelled' status._

4. Unpack downloaded archive with a spreadsheet and copy full path to a `.xslx` file

   Example: `/Users/user/Downloads/19057_bookings_20230106193908_1.xlsx`

5. To run the script for specified file in command line:

```sh
python main.py /Users/user/Downloads/19057_bookings_20230106193908_1.xlsx
```
