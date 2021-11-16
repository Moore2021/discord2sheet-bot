# discord2sheet-bot

For the original README go [here](https://github.com/hugonun/discord2sheet-bot).

# Specific to Moore2021/discordsheet-bot fork

This bot allows users to submit messages directly to your Google Sheet and retrive.

## How to set it up

### Option 1

**Step 1:** Enable the API and download credentials.json. This can be done here: https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the

**Step 2:** Run python3 setup.py:

Enter all information that you are prompted for.

*For the google credentials, copy all contents of credentials.json and paste as answer.*

**Step 3:** Run the bot

`python init.py`

### Option 2

**Step 1:** Create directory 'configurations' in source folder.

Example: 'discord2sheet-bot/configurations'

**Step 2:** Enable the API and download credentials.json. This can be done here: https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the

Make sure credentials.json is stored in the configurations directory.
- discord2sheet-bot/configurations/credentials.json

**Step 3:** Create token.txt file and place in configurations directory

On a single line paste in your discord bot token.

**Step 4:** Create spreadsheetid.txt file and place in configurations directory

On a single line paste in your spreadsheet id.

**Step 5:** Run the bot

`python init.py`
------

## Additional configutations

Require a specific role:

### Option 1

**Step 1:** Run python3 addit-setup.py

Enter all information that you are prompted for.

### Option 2

**Step 1:** Create requiredrole.txt file and place in configurations directory

On a single line paste in your required role's id.

set authorized users:

### Option 1

**Step 1:** Run python3 addit-setup.py

Enter all information that you are prompted for.

### Option 2

**Step 1:** Create authorizedusers.txt file and place in configurations directory

Paste each user's id on a new line.
