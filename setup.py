import os
"""Ask for secret token and then write to token.txt file"""
x=input("What is your discord bot Token: ")
with open('./configurations/token.txt', 'w') as token_file:
    token_file.write(x)

"""Ask for spreadsheet ID and then write to spreadsheetid.txt file"""
x=input("What is your spreadsheetid ID: ")
with open('./configurations/spreadsheetid.txt', 'w') as spreadsheetid_file:
    spreadsheetid_file.write(x)

"""Ask for google credentials and then write to credentials.json file"""
x=input("What is your google credentials.json: ")
with open('./configurations/credentials.json', 'w') as credentials_file:
    credentials_file.write(x)

"""Install all rewuirred rewuirements"""
os.system("python3 -m pip install -r requirements.txt")

"""Tell user to start the bot"""
os.system("echo You may now start the bot with 'python3 init.py'")