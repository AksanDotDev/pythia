#!/usr/bin/env python

import discord
from config import config

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



client.run(config.discord.token)
