import discord
from discord.ext import commands
from discord import Member
import os
from dotenv import load_dotenv
from discord import FFmpegPCMAudio
import requests
import json



load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
#------------------------------------------------------------------------------------------
#dictionary to store the audio queues of the guilds.
queues = {}

def check_queue(ctx, id):
    if queues[id] != []:
        voice = voice = ctx.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)
#------------------------------------------------------------------------------------------
       
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
#------------------------------------------------------------------------------------------
#on_ready event: This event triggers when the bot has finished setting up the bot.
@client.event
async def on_ready():
    print('Bot is ready.')
    print(f'Logged in as {client.user}')
    print('---------------------------------')
#------------------------------------------------------------------------------------------
#This commands checks the latency of the bot.
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')
#------------------------------------------------------------------------------------------
#on_message event: This event triggers when a message is sent in the server. This commands greets the user.
@client.command()
async def hello(ctx):
    await ctx.send('Hello!')
#------------------------------------------------------------------------------------------
#on_member_join event: This event triggers when someone joins the server.
@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')
    await member.send(f'Welcome to the server {member}!')
#------------------------------------------------------------------------------------------
#on_memeber_remove: This event triggers when someone leaves the server.
@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')
#------------------------------------------------------------------------------------------
#this command makes the bot to join the voice channel.
@client.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
    else:
        await ctx.send('You are not in a voice channel!')
#------------------------------------------------------------------------------------------
#this command makes the bot to leave the voice channel.
@client.command(pass_context=True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send('I have left the voice channel!')
    else:
        await ctx.send('I am not in a voice channel!')
#------------------------------------------------------------------------------------------
#this command pauses the audio playing in the voice channel.
@client.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send('I have paused the audio!')
    else:
        await ctx.send('I am not playing anything!')
#------------------------------------------------------------------------------------------
#this command resumes the audio platying in the voice channel.
@client.command(pass_context=True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send('I have resumed the audio!')
    else:
        await ctx.send('I am not paused!')
#------------------------------------------------------------------------------------------
#this command stops the audio playing in the voice channel.
@client.command(pass_context=True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.send('I have stopped the audio!')
#------------------------------------------------------------------------------------------
# this command plays the audio in the voice channel.
@client.command(pass_context=True)
async def play(ctx, filename: str):
    voice = voice = ctx.voice_client
    song = filename + '.mp3'
    source = FFmpegPCMAudio(song)
    player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))
    await ctx.send(f'Playing {filename}!')
#------------------------------------------------------------------------------------------
@client.command(pass_context=True)
async def queue(ctx, filename: str):
    voice = voice = ctx.voice_client
    song = filename + '.mp3'
    source = FFmpegPCMAudio(song)

    guild_id = ctx.message.guild.id

    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id] = [source]

    await ctx("Added to queue!")
#------------------------------------------------------------------------------------------
#exception handling for the commands.
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')
#------------------------------------------------------------------------------------------
#trying events, responds with hello when hi is sent.
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if "hi" in message.content.casefold():  
        await message.channel.send('Hello!')

    await client.process_commands(message)  #This line is important to process the commands.
#------------------------------------------------------------------------------------------
#this command kicks the user from the server.
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked from the server.')
#------------------------------------------------------------------------------------------
#this command bans the user from the server.
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned from the server.')
#------------------------------------------------------------------------------------------
#this command unbans the user from the server.
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} has been unbanned from the server.')
            return
#------------------------------------------------------------------------------------------
#this command is used to purge the messages in the channel.
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} messages have been cleared!')
#------------------------------------------------------------------------------------------


client.run(DISCORD_TOKEN)