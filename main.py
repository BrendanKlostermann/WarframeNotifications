# Warframe Alerts for discord chat bot
# Written by Brendan Klostermann

#bot.py
import os
import aiohttp
import asyncio

import discord
from dotenv import load_dotenv

# Get custom class definitions
import models

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ALERTS_ROLE = os.getenv('ALERTS_ROLE')


intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.guild_messages = True


client = discord.Client(intents=discord.Intents.default())



@client.event
async def on_ready():
    # This for loop is to ensure the bot is setup correctly on the servers it is installed on. Only occurs on startup
    for guild in client.guilds:
        
        channels = guild.text_channels
        print(
            f'{client.user} has connected for the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
            )           
        #Check if "Warframe Notifications" category exists
        category = discord.utils.get(guild.categories, name="Warframe Notifications")
        #Create category if it doesnt exist
        if not category:
            try:
                category = await guild.create_category("Warframe Notifications")
                print(f"Created category: {category.name} for server: {guild.name}")
            except discord.Forbidden:
                print(f"Failed to create category: {category.name}. Bot lacks permissions.")

        #List of channel names required
        channel_names = ["alerts","arbitrations","fissures","events"]
        for channel_name in channel_names:
            existing_channel = discord.utils.get(category.channels, name=channel_name)

            if not existing_channel:
                try:
                    channel = await guild.create_text_channel(channel_name, category=category)
                    print(f"Created text channel: {channel_name} for category: {category.name} on server: {guild.name}")
                    
                    role = discord.utils.get(guild.roles, name=ALERTS_ROLE)
                    if role:
                        await channel.set_permissions(guild.default_role, read_messages=True)
                        await channel.set_permissions(role, read_messages=True, send_messages=True)
                except discord.Forbidden:
                    print(f"Failed to create text channel, permission not allowed.")





    # This is the loop that will constantly run to collect data and send notifications of new alerts
    while True:
        # Process Alert data
        try:
            alerts = await models.CollectNewAlertData()                
        except Exception as e:
            print(f"Error occured durring fetching and processing alert data. {e}")
        
        # Process Arbitration Data
        
        # Process Fissure Data
        
            
        # Wait one minute for next interation 
        await asyncio.sleep(60)
            
            
client.run(TOKEN)

