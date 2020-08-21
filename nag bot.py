import discord
import json
from random import randint
from discord.ext import commands
bot = commands.Bot(command_prefix='n!',description="spaghetti coded by RedstoneFlux#0666")
conversations=["What was the last funny video you saw?", "What do you do to get rid of stress?", "What is something you are obsessed with?","What three words best describe you?","What would be your perfect weekend?","What’s your favorite number? Why?","What are you going to do this weekend?","What’s the most useful thing you own?","What’s your favorite way to waste time?","What do you think of tattoos? Do you have any?","Do you have any pets? What are their names?","Where did you go last weekend? / What did you do last weekend?","What is something popular now that annoys you?","What did you do on your last vacation?","When was the last time you worked incredibly hard?","Are you very active, or do you prefer to just relax in your free time?","What do you do when you hang out with your friends?","Who is your oldest friend? Where did you meet them?","What’s the best / worst thing about your work/school?","If you had intro music, what song would it be? Why?","What were you really into when you were a kid?","If you could have any animal as a pet, what animal would you choose?","Have you ever saved an animal’s life? How about a person’s life?","If you opened a business, what kind of business would it be?","Who is your favorite entertainer (comedian, musician, actor, etc.)?","Are you a very organized person?","Have you ever given a presentation in front of a large group of people? How did it go?","What is the strangest dream you have ever had?","What is a controversial opinion you have?","Who in your life brings you the most joy?","Who had the biggest impact on the person you have become?","What is the most annoying habit someone can have?","Where is the most beautiful place you have been?","Where do you spend most of your free time/day?","Who was your best friend in elementary school?","How often do you stay up past 3 a.m.?","What’s your favorite season? Why?","Which is more important, having a great car or a great house? Why?","What animal or insect do you wish humans could eradicate?","Where is the most beautiful place near where you live?","What do you bring with you everywhere you go?","How much time do you spend on the internet? What do you usually do?","What is the most disgusting habit some people have?","Where and when was the most amazing sunset you have ever seen?","Which recent news story is the most interesting?","Where is the worst place you have been stuck for a long time?","If you had to change your name, what would your new name be?","What is something that really annoys you but doesn’t bother most people?","What word or saying from the past do you think should come back?","How should success be measured? And by that measurement, who is the most successful person you know?"]
with open('trustedIDs.json', 'r') as filehandle:
    trustedIDs = json.load(filehandle)
with open("token.txt","r") as tk:
    token = tk.read()

@bot.command()
async def koolness(ctx,arg):
    """
    Rates the koolness of something from 1 to 10
    """
    koolText="This gets "+str(randint(1,10))+" out of 10"
    await ctx.send(koolText)
@bot.command()
async def kooIness(ctx,hidden=True):
    await ctx.send("This gets a 10 out of 10")
@bot.command()
async def say(ctx, arg):
    """
    Repeats your message
    """
    await ctx.send(arg)
@bot.command()
async def yo(ctx):
    await ctx.send("what's popping famsquad")
@bot.command()
async def conversation(ctx):
    """
    gives a random conversation starter
    """
    i=randint(1,len(conversations))-1
    await ctx.send(conversations[i])

"""These commands can only be used by trusted users"""
@bot.command()
async def change_status(self,ctx,arg):
    """
    changes the bot's status
    """
    if ctx.message.author.id in trustedIDs:   
        status = open("status.txt","w")
        status.write(arg)
        status = open("status.txt","r")
        statustext = status.read()
        await bot.change_presence(activity=discord.Game(name=statustext))
        await ctx.send("Changed status to "+statustext)
    else:
        await ctx.send("You do not have access to this command")
@bot.command()
async def trust(ctx,arg: discord.User):
    """
    allows a given user to use trust-level commands
    """
    if ctx.message.author.id in trustedIDs: 
        trustedIDs.append(int(arg.id))
        with open('trustedIDs.json', 'w') as filehandle:
            json.dump(trustedIDs, filehandle)
        await ctx.send(f"Added {arg.id} to trusted")
@bot.command()
async def untrust(ctx,arg: discord.User):
    """
    revokes a user's permission to use trust-level commands
    """
    if ctx.message.author.id in trustedIDs: 
        trustedIDs.remove(int(arg.id))
        with open('trustedIDs.json', 'w') as filehandle:
            json.dump(trustedIDs, filehandle)
        await ctx.send(f"Removed {arg.id} from trusted")
@bot.event
async def on_ready():
    status = open("status.txt","r")
    await bot.change_presence(activity=discord.Game(name=str(status.read())))
    print(f'We have logged in as {bot.user} in discord.py version {discord.__version__}')
bot.run(token)