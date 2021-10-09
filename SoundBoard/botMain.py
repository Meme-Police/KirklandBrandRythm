import discord
from discord.player import FFmpegPCMAudio
import nacl as pynacl
import opus_api
import ctypes
import json
import random
import time
import os
import bot
import asyncio
import pafy
import subprocess
VP = None
songs = []
TOKEN = bot.token
client = discord.Client()
loop = asyncio.get_event_loop()
connected = False

def convert_and_split(filename):
    command = ['ffmpeg', '-i', 'song1.webm', filename]
    subprocess.run(command,stdout=subprocess.PIPE,stdin=subprocess.PIPE)

# make sure of a sucessfull connection
@client.event
async def on_ready():
    print("We have loged in as {0.user}".format(client))
    return None

# the main boi (everything is controlled through message moderation so it's all in here)
@client.event
async def on_message(message):
    global songs
    global VP
    # make sure we aren't replying to ourselves  
    if message.author == client.user:
        return None


    # monitor for the command character
    elif message.content.startswith('!play '):
        url = message.content[6:]
        lenQ = len(songs)
        if message.author.voice != None or client.user.voice == None:
            if lenQ > 0:
                songs.append(url)
                await message.channel.send(f"There are {lenQ} song/s in the queue")
            else:
                try:
                    video = pafy.new(url)
                    songs.append(url)
                    # getting best stream
                    best = video.getbestaudio()

                    try:
                        os.remove("song.webm")
                    except FileNotFoundError as f:
                        print(f)
                    await message.channel.send("Downloading. This may take a moment depending on the video length.")
                    path = best.download("song.webm")
                
            
                
                    print("Number of users: " + str(len(message.author.voice.channel.voice_states)) + "\nUser Limit: " + str(message.author.voice.channel.user_limit))
                    # this long ass if statement makes sure that the channel we are trying to connect to isn't full
                    if message.author.voice.channel.user_limit > len(message.author.voice.channel.voice_states) or \
                    message.author.voice.channel.user_limit == 0:
                        await message.channel.send("Connecting")
                        print(client.voice_clients)
                        if len(client.voice_clients) == 0:
                            await connect(message)
                            print("made vp")
                        voiceHandler()
                    else:
                        await message.channel.send("That channel is full")
                except:
                    await message.channel.send("I can only do valid youtube urls")
        else:
            await message.channel.send("You must be in a voice channel to use that command")
    elif message.content.startswith("!clear") or message.content.startswith("!stop"):
        try:
            await VP.disconnect()
            songs = []
        except:
            pass
    elif message.content.startswith("!save"):
        url = message.content[6:]
        await message.channel.send("Downloading. This may take a moment depending on the video length.")
        try:
                    video = pafy.new(url)
                    songs.append(url)
                    # getting best stream
                    best = video.getbestaudio()

                    try:
                        os.remove("song.mp3")
                        os.remove("song1.webm")
                    except FileNotFoundError as f:
                        print(f)

                    path = best.download("song1.webm")
        except:
            await message.channel.send("I can only do valid youtube urls")
        await message.channel.send("Downloading. This may take a moment depending on the video length.")
        dest = str("song" + ".mp3")
        convert_and_split(dest)
        await message.channel.send(file=discord.File(r"song.mp3"))
            
        
    #gotta return something or else I feel weird
    return None

async def connect(message):
    global VP
    VP = await message.author.voice.channel.connect()

async def disconnect():
    await VP.disconnect()

def voiceHandler():
    global VP
   

    VP.play(discord.FFmpegPCMAudio("song.webm"), after=lambda x: playNext())
    
    VP.source = discord.PCMVolumeTransformer(VP.source)
    VP.source.volume = .5

    

def playNext():
    songs.pop(0)
    if len(songs) == 0:
        asyncio.run_coroutine_threadsafe(disconnect(), loop)
    else:
        try:
            video = pafy.new(songs[0])
            # getting best stream
            best = video.getbestaudio()

            try:
                os.remove("song.webm")
            except FileNotFoundError as f:
                print(f)

            path = best.download("song.webm")
            voiceHandler()
        except:
            pass

   

# runs the program using the super secret bot token
if TOKEN != "":
    print("Launching")
    loop.run_until_complete(client.run(TOKEN))
    
else:
    print("No bot token identified, please fill in, or create token.txt in the main directory with your bot token")