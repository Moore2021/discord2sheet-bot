# BSD 3-Clause License
# Copyright (c) 2019, Hugonun(https://github.com/hugonun)
# All rights reserved.
import discord
from discord.ext import commands
import os

description = '''Helping your discord server comminucate with a google sheet.'''
intents = discord.Intents.default()
intents.members = True
help_command = commands.DefaultHelpCommand(
    no_category = 'Need some help?'
)
client = commands.Bot(command_prefix='<', help_command= help_command, description=description, intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print('------')
    activity = discord.CustomActivity('record keeping')
    await client.change_presence(status=discord.Status.online, activity=activity)

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_message(message):

    await client.process_commands(message=message)
    
    # Whois
    # Please dont remove the copyright and github repo
    if len(message.mentions) > 0:
        for muser in message.mentions:
            if muser.id == client.user.id:
                if any(word in message.content for word in ['whois','who is','Help','help','info']):
                    await message.channel.send('This bot was made by hugonun(https://github.com/hugonun/).\nSource code: https://github.com/hugonun/discord2sheet-bot')

with open('./configurations/token.txt', 'r') as file:
    dtoken = file.read().replace('\n', '')

client.run(dtoken) # Add bot token here