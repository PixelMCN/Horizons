import discord
from discord.ext import commands
from discord import Member
import os
from dotenv import load_dotenv
from discord import FFmpegPCMAudio
import requests
import json
import yt_dlp


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
    await client.change_presence(activity=discord.Game(name='Create: Weaponworks'))
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
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have the permission to kick members!')
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
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have the permission to ban members!')
#------------------------------------------------------------------------------------------
#this command is used to purge the messages in the channel.
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} messages have been cleared!')
#------------------------------------------------------------------------------------------
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have the permission to clear messages!')
#------------------------------------------------------------------------------------------
#this command fetches guild information the bot is in.
@client.command()
async def guild(ctx):
    guild = ctx.guild
    name = guild.name
    description = guild.description if guild.description else "No description available."
    owner = guild.owner
    icon = guild.icon.url if guild.icon else None  
    member_count = guild.member_count
    created_at = guild.created_at.strftime("%B %d, %Y")  # Format date
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    roles = len(guild.roles) - 1  # Excluding @everyone role
    boost_level = guild.premium_tier  # Boost level
    boost_count = guild.premium_subscription_count  # Boost count

    embed = discord.Embed(
        title=name,
        description=description,
        color=discord.Color.blue(),
        timestamp=ctx.message.created_at  # Shows when command was used
    )
    
    if icon:
        embed.set_thumbnail(url=icon)

    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Created On", value=created_at, inline=True)
    embed.add_field(name="Members", value=member_count, inline=True)
    embed.add_field(name="Text Channels", value=text_channels, inline=True)
    embed.add_field(name="Voice Channels", value=voice_channels, inline=True)
    embed.add_field(name="Roles", value=roles, inline=True)
    embed.add_field(name="Boost Level", value=f"Level {boost_level}", inline=True)
    embed.add_field(name="Boosts", value=boost_count, inline=True)

    await ctx.send(embed=embed)

    print("--------------------------------------------")
    print(f"Guild: {name} was fetched.")
    print(f"Description: {description}")
    print(f"Owner: {owner}")
    print(f"Icon: {icon}")
    print(f"Member Count: {member_count}")
    print(f"Created At: {created_at}")
    print(f"Text Channels: {text_channels}")
    print(f"Voice Channels: {voice_channels}")
    print(f"Roles: {roles}")
    print(f"Boost Level: Level {boost_level}")
    print(f"Boosts: {boost_count}")
    print("--------------------------------------------")
#------------------------------------------------------------------------------------------
"""
#command to play music from youtube api.
@client.command()
async def play_music(ctx, *, search):
    api_key = os.getenv("YOUTUBE_API")  
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={search}&key={api_key}"

    response = requests.get(url)
    json_data = json.loads(response.text)

    if "items" not in json_data or not json_data["items"]:
        await ctx.send("No results found!")
        return

    video_id = json_data["items"][0]["id"]["videoId"]
    video_title = json_data["items"][0]["snippet"]["title"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    
    if ctx.voice_client is None:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()
        else:
            await ctx.send("You must be in a voice channel!")
            return
    else:
        voice_client = ctx.voice_client

    
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        audio_url = info["url"]

    # Play the audio
    voice_client.stop()
    voice_client.play(discord.FFmpegPCMAudio(audio_url))

    await ctx.send(f"🎵 **Now Playing:** {video_title}\n {video_url}")

#------------------------------------------------------------------------------------------
"""
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used!')
#------------------------------------------------------------------------------------------
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have the permission to use this command!')
#------------------------------------------------------------------------------------------
@client.command()
async def message(ctx, member: discord.Member, *, message=None):
    if message is None:
        await ctx.send('Please provide a message!')
        return
    await member.send(message)
    await ctx.send(f'Message sent to {member}!')
#------------------------------------------------------------------------------------------


#running the bot.
client.run(DISCORD_TOKEN)