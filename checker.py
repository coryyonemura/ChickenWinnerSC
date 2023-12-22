import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
# from dateutil import parser
import pytz
# import asyncio

TOKEN = "TOKEN"
PREFIX = '!'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has logged on')

@bot.command(name="set_game")
async def set_game(ctx, date_str, time_str, home_team, opponent):
    #example: !set_game 2023-01-01 18:00:00 home_team opponent

    # calculate time until game starts
    date_string = date_str+" "+time_str

    # Convert the date string to a datetime object
    target_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

    # Set the time zone to Eastern Time
    et_timezone = pytz.timezone('US/Eastern')

    # Get the current time in Eastern Time (aware of the timezone)
    current_time_et = datetime.now(et_timezone)

    target_date = et_timezone.localize(target_date)
    print(f'current_time_et = {current_time_et}')
    print(f'target_date = {target_date}')
    # Calculate the time difference
    time_difference = target_date-current_time_et

    # Extract the time difference in seconds
    time_until_game = [int(time_difference.total_seconds())]

    print(f'Time difference in seconds: {time_until_game[0]}')

    #schedule announcement task
    announce_winner.start(ctx, time_until_game, home_team, opponent)

@tasks.loop(seconds=1)
async def announce_winner(ctx, seconds_until_game, home_team, opponent):
    # print(seconds_until_game[0])
    if seconds_until_game[0] <= 0:
        #game has started, write the code that gets the data
        winner = home_team
        await ctx.send(f'The game against {opponent} has finished, the winning team is {home_team}')
        announce_winner.stop()
    else:
        # updates time until game
        seconds_until_game[0] -= 1



bot.run(TOKEN)