import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game(name="with your feelings"))

initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append(f'cogs.{filename[:-3]}')

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)



print("Cogs to load:", initial_extensions)


client.run(DISCORD_TOKEN)