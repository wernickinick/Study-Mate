import discord
from discord.ext import commands, tasks 
from dataclasses import dataclass
import datetime
import random
import os
from dotenv import load_dotenv

intents = discord.Intents.default()

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
channel_id = os.getenv('CHANNEL_ID')

#list of greeting that are selected at random
starter_greetings = [
    "Happy studying!",
    "Very studious of you!",
    "Thanks for coming!",
    "Welcome!"
]

motivational_qoute = [ # List of Motivational Qoutes
    "“If you can imagine it, you can achieve it. If you can dream it, you can become it.” - **William Arthur Ward**",
"“The people who are crazy enough to believe they can change the world are the ones who do.” - **Steve Jobs**",
"“You don't learn to walk by following rules. You learn by doing, and by falling over.” - **Richard Branson** ",
"“Learn from yesterday. Live for today. Hope for tomorrow.” - **Albert Einstein**",
"“I gave myself permission to make mistakes. I wouldn't ever give myself permission not to try.” - **Steve Pavlina**",
"“Mistakes are the portals of discovery.” - **James Joyce**",
"“Education is the most powerful weapon which you can use to change the world.” - **Nelson Mandela**",
"“Great things are done by a series of small things brought together.” - **Vincent Van Gogh**",
]

MAX_SESSION_TIME_MINUTES = 30

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0
    total_study_time: int = 0 # Track time for each user

session = Session()
study_session = {} #Dictionary for users tracking time
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event #when bot is turned on it texts in discord channel and says logged in, in terminal
async def on_ready():
    print("logged in as Study Mate")
    channel = bot.get_channel(int(channel_id))    
    await channel.send(f"Hello, I'm Study Mate! \nYour ultimate study companion.")

@bot.event #When someone joins it picks any choice from list to greet
async def on_member_join(member):
    join_channel = member.guild.get_channel(int(channel_id))
    await join_channel.send(f"{member.mention} {random.choice(starter_greetings)}")

@bot.command() #lets people know he cant give answers yet
async def answer(ctx):
    await ctx.send("I can't give Homework answers yet! \nThere will be an update soon!")

@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2) #so it doesnt tell people to take break write when they start
async def break_reminder():

#Ignore first time of it looping
    if break_reminder.current_loop == 0:
        return

    channel = bot.get_channel(int(channel_id)) #lets user know to take break after 30 min
    await channel.send(f"**Take a break!** You've been studying for **{MAX_SESSION_TIME_MINUTES}** minutes.")

@bot.command() #says hello
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author}!")

@bot.command() #lets user know theyve already started session if they tried to start without stopping
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return
    
    session.is_active = True #lets users start session 
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    break_reminder.start
    await ctx.send("Session started **Now**")

@bot.command() #tells users they cant end becuase they didnt start yet
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session is active!")
        return
    
    session.is_active = False #lets user know they ended theyre session
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    break_reminder.stop()
    await ctx.send(f"Session ended after {human_readable_duration}")

@bot.command() # gives a motivational qoute
async def motivation(ctx):
    await ctx.send(f"{random.choice(motivational_qoute)}")

bot.run(discord_token) 