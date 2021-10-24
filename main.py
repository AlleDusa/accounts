import sys
import os
from discord.ext import commands
import discord
import logging
import discord,json,os,random
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_role, MissingRole

with open("config.json") as file: # Load the config file
    info = json.load(file)
    token = info["token"]
    delete = info["autodelete"]
    prefix = info["prefix"]

bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    activity = discord.Game(name=">help", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print("Bot is ready! Have fun.")

@bot.command() # Stock command
async def stock(ctx):
    stockmenu = discord.Embed(title="Stock",description="  ") # Define the embed
    for filename in os.listdir("Accounts"):
        with open("Accounts\\"+filename) as f: # Open every file in the accounts folder
            ammount = len(f.read().splitlines()) # Get the ammount of lines
            name = (filename[0].upper() + filename[1:].lower()).replace(".txt","") #Make the name look nice
            stockmenu.description += f"*{name}* - {ammount}\n" # Add to the embed
    await ctx.send(embed=stockmenu) # Send the embed




@bot.command() #Gen command
async def gen(ctx,name=None):
    if name == None:
        await ctx.send("Enter the account you would like to generate!") # Say error if no name specified
    else:
        name = name.lower()+".txt" #Add the .txt ext
        if name not in os.listdir("Accounts"): # If the name not in the directory
            await ctx.send(f"Invalid account. `{prefix}stock`")
        else:
            with open("Accounts\\"+name) as file:
                lines = file.read().splitlines() #Read the lines in the file
            if len(lines) == 0: # If the file is empty
                await ctx.send("We don't have this account at this time, select other one.") #Send error if lines = 0
                embed=discord.Embed(title="Generator", color=0xff0000)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/814934254294925352/896393135180115998/download.jpg")
                embed.add_field(name=f"{ctx.message.author}", value=f"ERROR: need to restock`", inline=False)
                embed.set_footer(text="Accounts")
                    channel=bot.get_channel(YourID) # Add your own discord channel id
                    channel=bot.get_channel(YourID) # Add your own discord channel id
                await channel.send(embed=embed)
            else:
                with open("Accounts\\"+name) as file:
                    account = random.choice(lines) # Get a random line
                try: #Try to send the account to the sender
                    embed=discord.Embed(title="Generator", description="Account generated successfully", color=0x1eff00)
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/814934254294925352/896393135180115998/download.jpg")
                    embed.add_field(name="Account logins", value=f"`{str(account)}`", inline=False)
                    embed.add_field(name="DISCLAIMER", value="THIS MESSAGE WILL BE DELETED AUTOMATICALLY IN **30 SEC.**", inline=True)
                    embed.set_footer(text="Accounts")
                    await ctx.author.send(embed=embed,delete_after=delete)
                    await ctx.author.send(f"Copy and Paste this: `{str(account)}`",delete_after=delete)             
                except: # If it failed send a message in the chat
                    await ctx.send("Error! We can't send you logins!")
                    embed=discord.Embed(title="Generator", color=0xff0000)
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/814934254294925352/896393135180115998/download.jpg")
                    embed.add_field(name=f"{ctx.message.author}", value="ERROR:: unable to send message", inline=False)
                    channel=bot.get_channel(YourID) # Add your own discord channel id
                    channel=bot.get_channel(YourID) # Add your own discord channel id
                    await channel.send(embed=embed)
                else: # If it sent the account, say so then remove the account from the file
                    await ctx.send(f'Your account has been sent to you in a private message! {ctx.message.author.mention}')
                    embed=discord.Embed(title="Generator", color=0x28e901)
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/814934254294925352/896393135180115998/download.jpg")
                    embed.add_field(name=f"{ctx.message.author}", value="An account has been generated and gas been successfully sent privately", inline=False)
                    embed.add_field(name=f"Account logins", value=f"`{str(account)}` {name}", inline=False)
                    embed.set_footer(text="Accounts")
                    channel=bot.get_channel(YourID) # Add your own discord channel id
                    channel=bot.get_channel(YourID) # Add your own discord channel id
                    await channel.send(embed=embed)
                    with open("Accounts\\"+name,"w") as file:
                        file.write("") #Clear the file
                    with open("Accounts\\"+name,"a") as file:
                        for line in lines: #Add the lines back
                            if line != account: #Dont add the account back to the file
                                file.write(line+"\n") # Add other lines to file

def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv) 

@bot.command(name= 'restart') # Bot restart command
async def shutdown(ctx):
    id = str(ctx.author.id)
    if id == 'YourID': # Add you own discord account ID
        await ctx.send('Restarting..')
        embed=discord.Embed(title="Owner commands", color=0xff0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/814934254294925352/896393135180115998/download.jpg")
        embed.add_field(name=f"{ctx.message.author}", value="Restarted bot", inline=False)
        embed.set_footer(text="Accounts")
        channel=bot.get_channel(YourID) # Add your own discord channel id
        await channel.send(embed=embed)
        print("Bot is restarting!")
        restart_bot()
    else:
        await ctx.send(f"You don't have permission to do this! {ctx.message.author.mention}",delete_after=delete)
    
bot.run(token)