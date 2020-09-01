#imports
import discord
import pickle
import json
from random import randint
from discord.ext import commands, flags
import urllib
import typing
import requests
import sys
import logging
from colorama import Fore, Style

#bot setup
logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix='n!',description="spaghetti coded by RedstoneFlux#0666",owner_id=438418848811581452,)

#file setup
with open('trustedIDs.json', 'r') as filehandle:
    trustedIDs = json.load(filehandle)
with open("token.txt","r") as tk:
    token = tk.read()

#variable setup
nickdict={}
json2=""
hookname=""
conversations=["What was the last funny video you saw?", "What do you do to get rid of stress?", "What is something you are obsessed with?","What three words best describe you?","What would be your perfect weekend?","What’s your favorite number? Why?","What are you going to do this weekend?","What’s the most useful thing you own?","What’s your favorite way to waste time?","What do you think of tattoos? Do you have any?","Do you have any pets? What are their names?","Where did you go last weekend? / What did you do last weekend?","What is something popular now that annoys you?","What did you do on your last vacation?","When was the last time you worked incredibly hard?","Are you very active, or do you prefer to just relax in your free time?","What do you do when you hang out with your friends?","Who is your oldest friend? Where did you meet them?","What’s the best / worst thing about your work/school?","If you had intro music, what song would it be? Why?","What were you really into when you were a kid?","If you could have any animal as a pet, what animal would you choose?","Have you ever saved an animal’s life? How about a person’s life?","If you opened a business, what kind of business would it be?","Who is your favorite entertainer (comedian, musician, actor, etc.)?","Are you a very organized person?","Have you ever given a presentation in front of a large group of people? How did it go?","What is the strangest dream you have ever had?","What is a controversial opinion you have?","Who in your life brings you the most joy?","Who had the biggest impact on the person you have become?","What is the most annoying habit someone can have?","Where is the most beautiful place you have been?","Where do you spend most of your free time/day?","Who was your best friend in elementary school?","How often do you stay up past 3 a.m.?","What’s your favorite season? Why?","Which is more important, having a great car or a great house? Why?","What animal or insect do you wish humans could eradicate?","Where is the most beautiful place near where you live?","What do you bring with you everywhere you go?","How much time do you spend on the internet? What do you usually do?","What is the most disgusting habit some people have?","Where and when was the most amazing sunset you have ever seen?","Which recent news story is the most interesting?","Where is the worst place you have been stuck for a long time?","If you had to change your name, what would your new name be?","What is something that really annoys you but doesn’t bother most people?","What word or saying from the past do you think should come back?","How should success be measured? And by that measurement, who is the most successful person you know?"]
#checks
async def is_trusted(ctx):
    if ctx.author.id in trustedIDs:
        return True
    else:
        await ctx.send("You do not have permission to use this command")

#errors
@bot.listen("on_command_error")
async def errors(ctx,error):
    error = error.__cause__ or error
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command does not exist")
    elif isinstance(error, commands.NotOwner):
        await ctx.send("You do not have permission to use this command")
    elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument)or isinstance(error, ValueError):
        await ctx.send("Make sure you typed the command correctly, do n!help <command> to see the syntax")
    elif isinstance(error, commands.CheckFailure):
        return
    else:
        print(f"""{Fore.RED}COMMAND ERROR: {error}
ERROR TYPE: {type(error)}{Style.RESET_ALL}""")

#owner commands
@bot.command(hidden=True)
@commands.is_owner()
async def stop(ctx):
    "shuts the bot down"
    raise SystemExit(0)

@bot.command(hidden=True)
@commands.is_owner()
async def test(ctx):
    cmdlist={}
    
    for x in bot.commands:
        cmdlist[str(x)]=(f"""{x.help}
""")
    await ctx.send(cmdlist)
#trust level commands
@bot.command(hidden=True)
@commands.check(is_trusted)
async def showmorehelpstuff(ctx):
    """shows hidden commands in n!help"""
    commands.HelpCommand(show_hidden=True)

@bot.command(hidden=True)
@commands.check(is_trusted)
async def showlesshelpstuff(ctx):
    """hides hidden commands in n!help"""
    commands.HelpCommand(show_hidden=True)

@bot.command(hidden=True)
@commands.check(is_trusted)
async def disable(ctx,cmd):
    """temporarily removes a command from the bot"""
    bot.remove_command(cmd)
    await ctx.send(f"Disabled n!{cmd}")

@bot.command(hidden=True)
@commands.check(is_trusted)
async def koolnum(ctx, number):
    """sets the string that n!kooIness outputs"""
    with open("koolnum.txt","w") as koolfile:
        koolfile.write(str(number))
    await ctx.send(f"koolnum set to {number}")

@bot.command(hidden=True)
@commands.check(is_trusted)
async def kooIness(ctx):
    """output a string set by n!koolnum"""
    with open("koolnum.txt","r") as koolfile:
        num1 = koolfile.read()
        await ctx.send(f"This gets {str(num1)} out of 10")

@bot.command(hidden=True)
@commands.check(is_trusted)
async def trust(ctx,user: discord.User):
    """allows a given user to use trust-level commands"""
    trustedIDs.append(int(user.id))
    with open('trustedIDs.json', 'w') as filehandle:
        json.dump(trustedIDs, filehandle)
    await ctx.send(f"Added {user.id} to trusted")

@bot.command(hidden=True)
async def untrust(ctx,user: discord.User):
    """revokes a user's permission to use trust-level commands"""
    trustedIDs.remove(int(user.id))
    with open('trustedIDs.json', 'w') as filehandle:
        json.dump(trustedIDs, filehandle)
    await ctx.send(f"Removed {user.id} from trusted")

@bot.command(hidden=True)
@commands.check(is_trusted)
async def changenicks(ctx,*, nick):
    """changes the nickname of all bots in the server to a given string, can be reverted with n!changenicksback"""
    for member in ctx.guild.members:
        if member.bot:
            nickdict[member.id]=member.nick
            await member.edit(nick=nick)
    with open('filename.pickle', 'wb') as handle:
        pickle.dump(nickdict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    await ctx.send("Nicknames changed")

@bot.command(hidden=True)
async def changenicksback(ctx):
    """undoes the effects of n!changenicks"""
    with open('filename.pickle', 'rb') as handle:
        b = pickle.load(handle)
        e=dict(b)
        for x,y in e.items():
            user = ctx.message.guild.get_member(x)
            await user.edit(nick=y)
    await ctx.send("Nicknames reverted")

@bot.command(hidden=True)
@commands.check(is_trusted)
async def change_status(ctx,*,statuschange):
    """changes the bot's status"""  
    status = open("status.txt","w")
    status.write(statuschange)
    status = open("status.txt","r")
    statustext = status.read()
    status.close()
    await bot.change_presence(activity=discord.Game(name=statustext))
    await ctx.send("Changed status to "+statustext)

#general commands
@flags.add_flag("--count",type=int,default= 1)
@flags.command()
async def roll(ctx,number:int,**flags):
    """rolls a die a given number of times"""
    rolltimes=int("{count!r}".format(**flags))
    rolls=[]
    for x in range(rolltimes):
        rolls.append(randint(1,number))
    rollnum = 0
    for x in rolls:
        rollnum += x
    await ctx.send(f"You rolled **{rolltimes}** **d{number}(s)** and got **{rolls}** = **{rollnum}** ")
bot.add_command(roll)

@bot.command()
async def sudo(ctx, user:typing.Union[discord.Member, discord.User,str], *, message):
    """mimics another user"""
    if type(user) == type(""): 
        hookname = user
        avatar = "https://cdn.discordapp.com/avatars/689564772512825363/f05524fd9e011108fd227b85c53e3d87.png?size=128"
    else: 
        hookname = user.display_name
        avatar = user.avatar_url
    webhook = await ctx.channel.create_webhook(name=hookname,reason=ctx.author.name)
    await webhook.send(message,avatar_url=avatar)
    await ctx.message.delete()
    await webhook.delete()

@bot.command()
async def say(ctx,*, message):
    """Repeats your message"""
    await ctx.send(message)

@bot.command()
async def sayy(ctx,channel: discord.TextChannel,*,message):
    """Improved version of say"""
    await channel.send(message)    

@bot.command()
async def koolness(ctx):
    """Rates the koolness of something from 1 to 10"""
    koolText="This gets "+str(randint(1,10))+" out of 10"
    await ctx.send(koolText)

@bot.command()
async def yo(ctx):
    ""
    await ctx.send("what's popping famsquad")

@bot.command()
async def conversation(ctx):
    """gives a random conversation starter"""
    i=randint(1,len(conversations))-1
    await ctx.send(conversations[i])

@bot.event
async def on_ready():
    status = open("status.txt","r")
    await bot.change_presence(activity=discord.Game(name=str(status.read())))
    print(f'We have logged in as {bot.user} in discord.py version {discord.__version__}')
bot.run(token)
