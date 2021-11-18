# BSD 3-Clause License
# Copyright (c) 2019, Hugonun(https://github.com/hugonun)
# All rights reserved.

import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from os.path import exists, isdir
from os import makedirs, path, getcwd

configurations_dir = isdir('configurations')

if not configurations_dir:
    makedirs('configurations')


# Autogenerate blank files
requiredrole_file_exists = exists('./configurations/requiredrole.txt')
authorizedusers_file_exists = exists('./configurations/authorizedusers.txt')

# Need user input
spreadsheetid_file_exists = exists('./configurations/spreadsheetid.txt')
token_file_exists = exists('./configurations/token.txt')
clientsecret_file_exists = exists('./configurations/client_secret.json')
googleuser_file_exists = exists('./configurations/googleuser.txt')
rangenames_file_exists = exists('./configurations/rangenames.txt')

if not requiredrole_file_exists:
    open('./configurations/requiredrole.txt','a').close()
    
if not authorizedusers_file_exists:
    open('./configurations/authorizedusers.txt','a').close()

if not clientsecret_file_exists or not token_file_exists or not spreadsheetid_file_exists or not googleuser_file_exists or not rangenames_file_exists:
    print("please run python3 setup.py")
    exit()

with open('./configurations/rangenames.txt', 'r') as file:
    rangenames = file.read().replace('\n', '')

with open('./configurations/spreadsheetid.txt', 'r') as file:
    sheet_id = file.read().replace('\n', '')
SPREADSHEET_ID = sheet_id # Add ID here

class gsheet(object):
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = None
        self.range_names = rangenames
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if exists('./configurations/token.pickle'):
            with open('./configurations/token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                secret_file = path.join(getcwd(), 'configurations/client_secret.json')
                credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=SCOPES)
                with open('./configurations/googleuser.txt', 'r') as file:
                    user = file.read().replace('\n', '')
                self.creds = credentials.with_subject(user)
                

            # Save the credentials for the next run
            with open('./configurations/token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        try:
            self.service = build('sheets','v4', credentials=self.creds)
        except Exception as e:
            print(e)
            
    def read(self,sheetid):
        sheet = self.service.spreadsheets()
        # Call the Sheets API
        range_names = self.range_names
        result = sheet.values().get(spreadsheetId=sheetid, range=range_names).execute()
        ranges = result.get('values', [])
        print('{0} ranges retrieved.'.format(len(ranges)))
        return ranges
