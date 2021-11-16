# BSD 3-Clause License
# Copyright (c) 2019, Hugonun(https://github.com/hugonun)
# All rights reserved.

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from os.path import exists, isdir
from os import makedirs

configurations_dir = isdir('configurations')

if not configurations_dir:
    makedirs('configurations')

credentials_file_exists = exists('./configurations/credentials.json')
token_file_exists = exists('./configurations/token.txt')
spreadsheetid_file_exists = exists('./configurations/spreadsheetid.txt')
requiredrole_file_exists = exists('./configurations/requiredrole.txt')
authorizedusers_file_exists = exists('./configurations/authorizedusers.txt')

if not requiredrole_file_exists:
    open('./configurations/requiredrole.txt','a').close()
    
if not authorizedusers_file_exists:
    open('./configurations/authorizedusers.txt','a').close()

if not credentials_file_exists or not token_file_exists or not spreadsheetid_file_exists:
    print("please run python3 setup.py")
    exit()

class gsheet(object):
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = None
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
                flow = InstalledAppFlow.from_client_secrets_file(
                    './configurations/credentials.json', SCOPES)
                self.creds = flow.run_local_server()

            # Save the credentials for the next run
            with open('./configurations/token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('sheets', 'v4', credentials=self.creds)
    def add(self,sheetid,sheetrange,ivalue):
        # Call the Sheets API
        sheet = self.service.spreadsheets()
        values = []
        values.append(ivalue)
        body = {
            'values': values
        }
        result = sheet.values().append(
            spreadsheetId=sheetid, range=sheetrange,
            valueInputOption='RAW', body=body).execute()
        
    def read(self,sheetid):
        sheet = self.service.spreadsheets()
        # Call the Sheets API
        range_names = '\'Form Responses 1\'!A:F'
        result = sheet.values().get(spreadsheetId=sheetid, range=range_names).execute()
        ranges = result.get('values', [])
        print('{0} ranges retrieved.'.format(len(ranges)))
        return ranges
