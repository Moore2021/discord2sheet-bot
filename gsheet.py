# BSD 3-Clause License
# Copyright (c) 2019, Hugonun(https://github.com/hugonun)
# All rights reserved.

from __future__ import print_function
import pickle
import os
#Uncomment for local testing
#from dotenv import load_dotenv
#load_dotenv()
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class gsheet(object):
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config({"installed":{"client_id":os.getenv('CLIENT_ID'),"project_id":os.getenv('PROJECT_ID'),"auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":os.getenv('CLIENT_SECRET'),"redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}, SCOPES)
                self.creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
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