#!/usr/bin/env python

import configparser
import discord
from collections import Counter
from os import path
import hashlib

configFileName = "astria.config.ini"

config = configparser.ConfigParser()
if path.isfile(configFileName):
    config.read(configFileName)
else:
    print("No config found")
    exit(1)

client = discord.Client()

@client.event
async def on_ready():
    print('Online as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.lower() ==  "marco":
        await message.channel.send("Polo!")

    if client.user.mentioned_in(message):
        await message.channel.send("Hello!")


client.run(config.get("core", "token"))