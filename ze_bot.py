import discord
import os
import time
import re

from discord import channel

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'
    .format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Spire Channel
    if message.channel.id == 923237578617024532:

        if message.content == "!open":
            array = get_open_classes_array()
            msg = ''.join(array)
            await message.channel.send("These are the open Classes : \n" + msg)
            return

        if re.fullmatch("![1-9]00s",message.content) != None:
            num = message.content[1]
            array = get_open_classes_array()
            small = [x for x in array if x.startswith("CS" + num)]
            msg = ''.join(small)
            if len(small) > 0:
                await message.channel.send("Open " + num + "00s : \n" + msg)
            else:
                await message.channel.send("No open " + num + "00s")
            return

        if re.fullmatch("![1-9][0-9][0-9]|![1-9][0-9][0-9][A-Z]", message.content) != None:
            array = get_open_classes_array()
            search = "CS" + message.content[1:4]
            small = [x for x in array if x.startswith(search)]
            if len(small) > 0:
                await message.channel.send(search + " is Open!")
            else:
                await message.channel.send(search + " is closed")
            return
        
        

                
        

    # Test Channel
    if message.channel.id == 925922171358953513:

        if message.content == "!ping":
            channel = client.get_channel(925922171358953513)
            await channel.send("!pong")
        
        return

        

def get_open_classes_array():
    with open("files/current_details.txt", "r") as f:
        past_details = f.readlines()
    return past_details

def printer():
    print("Hello!")

client.run(TOKEN)


