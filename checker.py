import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from dateutil import parser

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
    game_datetime = parser.parse(f'{date_str} {time_str}')
    await ctx.send(f'Set game of {home_team} against {opponent} on {game_datetime}')

    #calculate time until game starts
    time_until_game = game_datetime - datetime.utcnow()

    #schedule announcement task
    announce_winner.start(ctx, time_until_game.total_seconds(), opponent)

@tasks.loop(seconds=1)
async def announce_winner(ctx, seconds_until_game, opponent):
    if seconds_until_game <= 0:
        #game has started, write the code that gets the data
        winner = "Winning team"
        await ctx.send(f'The game against {opponent} has finished, the winning team is winner')
        announce_winner.stop()

    #updates time until game
    seconds_until_game -= 1

bot.run(TOKEN)