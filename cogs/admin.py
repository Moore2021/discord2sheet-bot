from discord.ext import commands
import discord
from utils.paginator import Pag
from utils.functions import *
from gsheet import SPREADSHEET_ID

class Admin(commands.Cog):
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, client):
        self.client = client
        self.SIZED_CHUNKS = 10
     
    def roleCheck(self, ctx):

        def openAndReadFile(file=str):
            with open(file, 'r') as file:
                if isFileEmpty(file=file.name):
                    results = file.read().replace('\n', '')
                else:
                    results = None
            return results

        def needsRequiredRole():
                results = openAndReadFile('./configurations/requiredrole.txt')

                REQUIREDROLE = None or results
                
                if REQUIREDROLE is not None:
                    '''Needs the role'''
                    return True
                else:
                    '''Does not need the role'''
                    return False
        
        def getRequiredRole():
            results = openAndReadFile('./configurations/requiredrole.txt')
            return results

        async def hasRequiredRole():
            REQUIREDROLE = getRequiredRole()
            if REQUIREDROLE is not None and discord.utils.get(ctx.author.roles, id=str(REQUIREDROLE)) is None:
                await ctx.send('You don\'t have the required role!')
                return False
            else: 
                return True
        
        if needsRequiredRole():
            return hasRequiredRole()
        else: 
            return True

    def authUsersCheck(self, ctx):

        def openAndReadFile(file=str):
            with open(file, 'r') as file:
                if isFileEmpty(file=file.name):
                    results = file.read().splitlines()
                else:
                    results = None
            return results

        def needsToBeAuthorizedUser():
                results = openAndReadFile('./configurations/authorizedusers.txt')

                authorized = None or results
                
                if authorized is not None:
                    '''Needs to be authorized'''
                    return True
                else:
                    '''Does not need to be authorized'''
                    return False
        
        def getAuthorizedUsers():
            results = openAndReadFile('./configurations/authorizedusers.txt')
            return results
        
        async def isAuthorizedUser():
            users = getAuthorizedUsers()
            if users is not None and str(ctx.author.id) not in users:
                await ctx.send('You are not authorized!')
                return False
            return True
        
        if needsToBeAuthorizedUser():
            return isAuthorizedUser()
        else: 
            return True

    def commandChecks(self, ctx):
        auth_users = self.authUsersCheck(ctx=ctx)
        auth_role = self.roleCheck(ctx=ctx)
        if auth_role is False or auth_users is False:
            return False
        else:
            return True

    @commands.command()
    async def lookup(self, ctx, searchPerameter):
        if self.commandChecks(ctx) is False:
            return
        paginator = Pag(client=self.client)
        paginator.set_pages([])
        response = sheet.read(SPREADSHEET_ID)
        
        response_obj_identifiers = []
        for response_obj in response:
            #print(response_obj)
            for element in response_obj:
                if element == searchPerameter:
                    index = response.index(response_obj)
                    if index not in response_obj_identifiers:
                        response_obj_identifiers.append(index)

        print(response_obj_identifiers)                
        if len(response_obj_identifiers)>=1: 
            for i in response_obj_identifiers:
                print(len(response[i]) == len(response[0]))
                test = [f'**{response[0][ind]}:** {s}' for ind, s in enumerate(response[i]) if len(response[i]) == len(response[0]) ]
                chunk = chunkarray(array=test, size=self.SIZED_CHUNKS)
                await paginator.chunktopage(chunk=chunk, color=discord.Color.green(),title="Viewing search results")
        else:
            await paginator.chunktopage(chunk='It seems no record has been made, if this seems wrong please go to the sheet in a browser and double check.', color=discord.Color.red(),title="Couldnt find any record(s)")
        
        await paginator.start(ctx=ctx)

    @commands.command()
    async def strike(self, ctx):
        ctx.send(f'Please use the form to input data')

def setup(bot):
    """Add class as a cog"""
    bot.add_cog(Admin(bot))