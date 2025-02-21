import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix='!',intents=discord.Intents.all())

@client.event
async def on_ready():
    print('Bot is ready.')
    print(f'Logged in as {client.user}')
    print('---------------------------------')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def hello(ctx):
    await ctx.send('Hello!')

client.run(DISCORD_TOKEN)