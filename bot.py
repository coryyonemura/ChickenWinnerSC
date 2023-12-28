import discord
from discord.ext import commands, tasks
from scheduleUpdaters import return_first_game, update_schedule
from hockeyRequests import get_score
from botHelpers import get_seconds, next_game_info

#live scores from sofascores.com
#lafc schedule from lafc.com
#ducks schedule from ?

TOKEN = "MTE2NTg0MDUyMDA2NTU4NTI1Mw.GIWboH.YE-RlcxO0bQsY48Vj50JvYx6mTt-DCDOvXEYxE"
PREFIX = '!'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has logged on')
    global seconds_until_game
    seconds_until_game = [get_seconds(return_first_game('jsonFiles/ducksScheduleUpdated.json'),return_first_game('jsonFiles/lafcGamesUpdated.json'))]
    countdown_to_next_game.start()
    # count_goals.start()

@bot.command(name="nextGame")
async def nextGame(ctx):
    await ctx.send(next_game_info())
        
@tasks.loop(seconds=60)
async def countdown_to_next_game():
    global seconds_until_game
    print(seconds_until_game[0])
    if seconds_until_game[0] <= 0:
        channel_id = 1187128458774585396
        channel = bot.get_channel(channel_id)

        if channel:
            await channel.send(f'the game has started! support your local team and potentially win free chicken!')

        # call a new task function that calls the data from the live data and checks for goals scored
        count_goals.start()
        #update the json file
        update_schedule("jsonFiles/ducksScheduleUpdated.json")

        seconds_until_game = [get_seconds(get_seconds(return_first_game('jsonFiles/ducksScheduleUpdated.json'),return_first_game('jsonFiles/lafcGamesUpdated.json') ))]

    else:
        seconds_until_game[0] -= 60
#
@tasks.loop(seconds=60)
async def count_goals():
    print('hello')
    score = get_score()
    if score == -1:
        count_goals.stop()
    else:
        if score >= 5:
            channel_id = 1187128458774585396
            channel = bot.get_channel(channel_id)
            await channel.send(f'@everyone the Anaheim Ducks have scored 5 goals! '
                               f'Claim your free chicken on the cfa app before midnight! '
                               f'(rewards may take up to 30 minutes from this announcement to show up on the cfa app)')
            count_goals.stop()

bot.run(TOKEN)