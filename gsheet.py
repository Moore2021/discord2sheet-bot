# BSD 3-Clause License
# Copyright (c) 2019, Hugonun(https://github.com/hugonun)
# All rights reserved.

from __future__ import print_function
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from os.path import exists, isdir
from os import makedirs

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

if not requiredrole_file_exists:
    open('./configurations/requiredrole.txt','a').close()
    
if not authorizedusers_file_exists:
    open('./configurations/authorizedusers.txt','a').close()

if not clientsecret_file_exists or not token_file_exists or not spreadsheetid_file_exists or not googleuser_file_exists:
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
                secret_file = os.path.join(os.getcwd(), 'configurations/client_secret.json')
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

        #self.service = build('sheets', 'v4', credentials=self.creds)
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
        range_names = '\'Form Responses 6\'!A:F'
        result = sheet.values().get(spreadsheetId=sheetid, range=range_names).execute()
        ranges = result.get('values', [])
        print('{0} ranges retrieved.'.format(len(ranges)))
        return ranges
