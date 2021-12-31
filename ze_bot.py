import discord
from discord.ext import tasks
import os
import re
import datetime
import requests
import json

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    check_open_classes.start()

# Looks through the files and mentions if a class opens or closes
@tasks.loop(seconds=10)
async def check_open_classes():
    file_o = open("files/open_classes.txt","r+")
    file_c = open("files/closed_classes.txt","r+")
    o_list = file_o.readlines()
    c_list = file_c.readlines()
    spire_channel = client.get_channel(923237578617024532) # Test Channel
    o_flag = False
    c_flag = False
    msg_o = ''
    msg_c = ''
    if len(o_list) > 0:
        msg_o = "Classes Opened : \n" + ''.join(o_list) + "\n"
        o_flag = True
        file_o.truncate(0)
    if len(c_list) > 0:
        msg_c = "Classes Closed : \n" + ''.join(c_list) + "\n"
        c_flag = True
        file_c.truncate(0)
    file_o.close()
    file_c.close()
    if o_flag or c_flag:
        await spire_channel.send(msg_o + msg_c)
    


# Handles Messages and requests
@client.event
async def on_message(message):

    # Reads a bot's message
    if message.author == client.user:
        return
    
    # Spire Channel
    if message.channel.id == 923237578617024532:

        # Command to clear the channel
        if message.content == "!clear":
            await message.channel.purge()

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

        # Command to clear the channel
        if message.content == "!clear":
            await message.channel.purge()
            return
        
        return

    # Random Channel
    if message.channel.id == 926295887842529310:

        if message.content == '!Hello':
            await message.channel.send("Hey! How do you do?")
            await client.wait_for('message', check=lambda message: message.author == message.author and message != "")
            await message.channel.send("Hope you have a great day")
    
        if message.content == '!time':
            now = datetime.datetime.now()
            msg = ("The time is : " + now.strftime("%Y-%m-%d %H:%M:%S"))
            await message.channel.send(msg)

        if message.content == '!inspire':
            response = requests.get("https://zenquotes.io/api/random")
            json_data = json.loads(response.text)
            quote = json_data[0]['q'] + " -" + json_data[0]['a']
            await message.channel.send(quote)

        if message.content == "!clear":
            await message.channel.purge()
            return
    
    # Normal message
    return

        

def get_open_classes_array():
    with open("files/current_details.txt", "r") as f:
        past_details = f.readlines()
    return past_details


client.run(TOKEN)