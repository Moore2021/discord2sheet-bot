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

"""Ask if the user would like to add additional configurations"""
x=input("Would you like to set up additional configurations now? y or n:    ")
if x=='y' or x=='yes':

    """Ask for required role"""
    try:
        y=input("What is your required role? (press enter for default)    ")
        with open('./configurations/requiredrole.txt', 'w') as requiredrole_file:
            requiredrole_file.write(y)
    except SyntaxError:
        y = None
        with open('./configurations/requiredrole.txt', 'w') as requiredrole_file:
            requiredrole_file.write(y)
    
    """Ask for authorized users"""
    try:
        y=input("Who are your authorized user(s)? (press enter for default)    ")
        with open('./configurations/authorizedusers.txt', 'w') as authorizedusers_file:
            authorizedusers_file.write(y)
    except SystemError:
        y = None
        with open('./configurations/authorizedusers.txt', 'w') as authorizedusers_file:
            authorizedusers_file.write(y)
else:
    os.system("echo You may run python3 addit-setup.py later to edit additional configurations if neccessary.")
"""Install all required requirements"""
os.system("python3 -m pip install -r requirements.txt")

"""Tell user to start the bot"""
os.system("echo You may now start the bot with 'python3 init.py'")