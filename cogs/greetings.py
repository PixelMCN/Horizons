import discord
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Added the @commands.command() decorator to register the command properly
    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello!')

    # Added self parameter to on_member_join and properly decorated it as a listener
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} has joined the server.')
        await member.send(f'Welcome to the server {member}!')

# Renamed client_setup to setup (this is the correct naming convention for loading cogs)
def setup(client):
    client.add_cog(Greetings(client))
    print('Greetings cog loaded')
