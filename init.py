# BSD 3-Clause License
# Copyright (c) 2019, Hugonun(https://github.com/hugonun)
# All rights reserved.

import discord

from gsheet import *
from decouple import config

client = discord.Client()
sheet = gsheet()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Restrict the command to a role
    # Change REQUIREDROLE to a role id or None
    REQUIREDROLE = None
    if REQUIREDROLE is not None and discord.utils.get(message.author.roles, id=str(REQUIREDROLE)) is None:
        await message.channel.send('You don\'t have the required role!')
        return

    SPREADSHEET_ID = config('SPREADSHEET_ID') # Add ID here

    # Command to insert data to excel
    if message.content.startswith('>>strike '):
        RANGE_NAME = 'A1'
        FIELDS = 3 # Amount of fields/cells

        # Code
        msg = message.content[9:]
        result = [x.strip() for x in msg.split(';')]
        if len(result) == FIELDS:
            # Add
            print(message.created_at)
            target_user = await message.guild.fetch_member(result[0])
            offense_number = int(result[1])
            translate_offense_number = [
                'Warning',
                'first (3hr mute)',
                'second (24 hr mute)',
                'third (72 hr mute)',
                'fourth (ban)'
                ]
            result[1] = translate_offense_number[offense_number]
            result.insert(1, '{0}#{1}'.format(target_user.name, target_user.discriminator))
            DATA = [str(message.created_at)] + ['{0}#{1} ({2})'.format(message.author.name, message.author.discriminator, str(message.author.id))] + result
            sheet.add(SPREADSHEET_ID, RANGE_NAME, DATA)
            await message.channel.send('Your data has been successfully submitted!')
        else:
            # Needs more/less fields
            await message.channel.send('Error: You need to add {0} fields, meaning it can only have {1} comma.'.format(FIELDS,FIELDS-1))
    elif message.content.startswith('>>warn '):
        RANGE_NAME = 'A1'
        FIELDS = 2 # Amount of fields/cells

        # Code
        msg = message.content[7:]
        result = [x.strip() for x in msg.split(';')]
        if len(result) == FIELDS:
            # Add
            print(message.created_at)
            target_user = await message.guild.fetch_member(result[0])
            result[1] = translate_offense_number[offense_number]
            result.insert(1, 'Warning')
            result.insert(1, '{0}#{1}'.format(target_user.name, target_user.discriminator))
            DATA = [str(message.created_at)] + ['{0}#{1} ({2})'.format(message.author.name, message.author.discriminator, str(message.author.id))] + result
            sheet.add(SPREADSHEET_ID, RANGE_NAME, DATA)
            await message.channel.send('Your data has been successfully submitted!')
        else:
            # Needs more/less fields
            await message.channel.send('Error: You need to add {0} fields, meaning it can only have {1} comma.'.format(FIELDS,FIELDS-1))
    # Whois
    elif message.content.startswith('>>lookup '):
        RANGE_NAME = 'A1'
        FIELDS = 1 # Amount of fields/cells

        # Code
        msg = message.content[9:]
        result = [x.strip() for x in msg.split(';')]
        if len(result) == FIELDS:
            # Read
            print(message.created_at)
            response = sheet.read(SPREADSHEET_ID)
            retrieved_elements = []
            for response_obj in response:
                for element in response_obj:
                    if element == result[0]:
                        retrieved_elements.append(response_obj)

            failpage = discord.Embed(title='Couldnt find user record(s)', description='It seems no record has been made, if this seems wrong please go to the sheet in a browser and double check.', colour=discord.Colour.red())
            if len(retrieved_elements)>=1:
                #success
                successpages = []
                for i in range(len(retrieved_elements)):
                    formattedDescription = 'Report made by: {0}\nStrike number: {1}\nReason: {2}\nTimestamp: {3}'.format(retrieved_elements[i][1], retrieved_elements[i][4], retrieved_elements[i][5], retrieved_elements[i][0])
                    successpages.append(discord.Embed(title='{0} records were found for {1}'.format(len(retrieved_elements), result[0]), description=formattedDescription, colour=discord.Colour.green()))
                    successpages[len(successpages)-1].set_footer(text='page {0} of {1}'.format(i+1, len(retrieved_elements)))
                print(len(successpages))
                buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
                pageCount = 0
                msg = await message.channel.send(embed=successpages[pageCount])

                for button in buttons:
                    await msg.add_reaction(button)

                while True:
                    try:
                        reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == message.author and reaction.emoji in buttons, timeout=60.0)

                    except asyncio.TimeoutError:
                        return print("test")

                    else:
                        previous_page = pageCount
                        if reaction.emoji == u"\u23EA":
                            pageCount = 0
                            
                        elif reaction.emoji == u"\u2B05":
                            if pageCount > 0:
                                pageCount -= 1
                                
                        elif reaction.emoji == u"\u27A1":
                            if pageCount < len(successpages)-1:
                                pageCount += 1

                        elif reaction.emoji == u"\u23E9":
                            pageCount = len(successpages)-1

                        for button in buttons:
                            await msg.remove_reaction(button, message.author)

                        if pageCount != previous_page:
                            await msg.edit(embed=successpages[pageCount])
            else:
                #fail
                await message.channel.send(embed=failpage)
        else:
            # Needs more/less fields
            await message.channel.send('Error: You need to add {0} fields, meaning it can only have {1} comma.'.format(FIELDS,FIELDS-1))

    # Please dont remove the copyright and github repo
    elif len(message.mentions) > 0:
        for muser in message.mentions:
            if muser.id == client.user.id:
                if any(word in message.content for word in ['whois','who is','Help','help','info']):
                    await message.channel.send('This bot was made by hugonun(https://github.com/hugonun/).\nSource code: https://github.com/hugonun/discord2sheet-bot')


client.run(config('TOKEN')) # Add bot token here
