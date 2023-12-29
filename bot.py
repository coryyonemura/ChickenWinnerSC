import discord
from discord.ext import commands, tasks
from scheduleUpdaters import return_first_game, update_schedule
from hockeyRequests import get_score
from botHelpers import get_seconds, next_game_info, get_sport
from soccerRequests import lafc_game, lafc_game_over

#live scores from sofascores.com
#lafc schedule from lafc.com
#ducks schedule from ?

SECONDS_PER_MINUTE = 60
TOKEN = "TOKEN"
PREFIX = '!'


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has logged on')
    global seconds_until_game
    lafcWin = False
    seconds_until_game = [get_seconds(return_first_game('jsonFiles/ducksGamesUpdated.json'), return_first_game('jsonFiles/lafcGamesUpdated.json'))]
    countdown_to_next_game.start()

@bot.command(name="nextGame")
async def nextGame(ctx):
    await ctx.send(next_game_info())
        
@tasks.loop(seconds=SECONDS_PER_MINUTE)
async def countdown_to_next_game():
    global seconds_until_game
    print(seconds_until_game[0])
    if seconds_until_game[0] <= 0:
        channel_id = 1187128458774585396
        channel = bot.get_channel(channel_id)

        if channel:
            sport = get_sport("jsonFiles/ducksGamesUpdated.json", 'jsonFiles/lafcGamesUpdated.json')

            if sport == "hockey":
                await channel.send(f'the Anaheim Ducks game has started! support your local team and potentially win free chicken!')
                ducks_goals.start()
                # update the json file
                update_schedule("jsonFiles/ducksGamesUpdated.json")
            elif sport == "soccer":
                await channel.send(f'the LAFC game has started! support your local team and potentially win free chicken!')
                lafc_win.start()
                update_schedule("jsonFiles/lafcGamesUpdated.json")
        seconds_until_game = [get_seconds(return_first_game('jsonFiles/ducksGamesUpdated.json'), return_first_game('jsonFiles/lafcGamesUpdated.json'))]

    else:
        seconds_until_game[0] -= SECONDS_PER_MINUTE
#
@tasks.loop(seconds=SECONDS_PER_MINUTE)
async def ducks_goals():
    print('hello')
    score = get_score()
    if score == -1:
        ducks_goals.stop()
    else:
        if score >= 5:
            channel_id = 1187128458774585396
            channel = bot.get_channel(channel_id)
            await channel.send(f'@everyone the Anaheim Ducks have scored 5 goals! '
                               f'Claim your free chicken on the cfa app before midnight! '
                               f'(rewards may take up to 30 minutes from this announcement to show up on the cfa app)')
            ducks_goals.stop()

@tasks.loop(seconds=SECONDS_PER_MINUTE)
async def lafc_win():
    global lafcWin
    if lafc_game_over():
        if lafcWin:
            channel_id = 1187128458774585396
            channel = bot.get_channel(channel_id)
            await channel.send(f'@everyone LAFC has won at home! '
                               f'Claim your free chicken on the cfa app before midnight! '
                               f'(rewards may take up to 30 minutes from this announcement to show up on the cfa app)')
        lafc_win.stop()
    else:
        lafcWin = lafc_game()


bot.run(TOKEN)