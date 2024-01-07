import discord
from discord.ext import commands, tasks
from scheduleUpdaters import return_first_game, update_schedule
from webRequests.hockeyRequests import get_score
from botHelpers import get_seconds, next_game_info, get_sport
from webRequests.soccerRequests import lafc_game, lafc_game_over
from webRequests.basketballRequests import missed_freethrows, clippers_game_over


#live scores from sofascores.com
#jsonLAFC schedule from jsonLAFC.com
#clippers schedule from nba.com
#angels schedule from ?
#ducks schedule from ?

SECONDS_PER_MINUTE = 60
TOKEN = "MTE2NTg0MDUyMDA2NTU4NTI1Mw.G1i4FN.LGzvlns6XSSBadfQpnZUv0zDCY1Op6y573kN90"
PREFIX = '!'


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has logged on')
    seconds_until_game = [get_seconds('jsonFiles/jsonDucks/ducksGamesUpdated.json',
                                      'jsonFiles/jsonLAFC/lafcGamesUpdated.json',
                                      'jsonFiles/jsonClippers/clippersGamesUpdated.json')]
    countdown_to_next_game.start(seconds_until_game)


@bot.command(name="nextGame")
async def nextGame(ctx):
    await ctx.send(next_game_info())
        
@tasks.loop(seconds=SECONDS_PER_MINUTE)
async def countdown_to_next_game(seconds_until_game):
    print(seconds_until_game[0])
    if seconds_until_game[0] <= 0:
        channel_id = 1187128458774585396
        channel = bot.get_channel(channel_id)

        if channel:
            sport = get_sport("jsonFiles/jsonDucks/ducksGamesUpdated.json",
                              'jsonFiles/jsonLAFC/lafcGamesUpdated.json',
                              'jsonFiles/jsonClippers/clippersGamesUpdated.json')

            if sport == "hockey":
                await channel.send(f'the Anaheim Ducks game has started! support your local team and potentially win free chicken!')
                ducks_goals.start()
                # update the json file
                update_schedule("jsonFiles/jsonDucks/ducksGamesUpdated.json")
            elif sport == "soccer":
                await channel.send(f'the LAFC game has started! support your local team and potentially win free chicken!')
                lafc_win.start(False)
                update_schedule("jsonFiles/jsonLAFC/lafcGamesUpdated.json")
            elif sport == "basketball":
                await channel.send(f'the LA Clippers game has started! support your local team and potentially win free chicken!')
                clippers_freethrows.start()
                update_schedule("jsonFiles/jsonClippers/clippersGamesUpdated.json")

        seconds_until_game[0] = get_seconds('jsonFiles/jsonDucks/ducksGamesUpdated.json',
                                            'jsonFiles/jsonLAFC/lafcGamesUpdated.json',
                                            'jsonFiles/jsonClippers/clippersGamesUpdated.json')
    else:
        seconds_until_game[0] -= SECONDS_PER_MINUTE
#
@tasks.loop(seconds=SECONDS_PER_MINUTE)
async def ducks_goals():
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
async def lafc_win(winner):
    if lafc_game_over():
        if winner:
            channel_id = 1187128458774585396
            channel = bot.get_channel(channel_id)
            await channel.send(f'@everyone LAFC has won at home! '
                               f'Claim your free chicken on the cfa app before midnight! '
                               f'(rewards may take up to 30 minutes from this announcement to show up on the cfa app)')
        lafc_win.stop()
    else:
        winner = lafc_game()

@tasks.loop(seconds=SECONDS_PER_MINUTE)
async def clippers_freethrows():
    gameId = return_first_game('jsonFiles/jsonClippers/clippersGamesUpdated.json')['gameId']
    if clippers_game_over(gameId) == False:
        if missed_freethrows():
            channel_id = 1187128458774585396
            channel = bot.get_channel(channel_id)
            await channel.send(f'@everyone the Clippers opponent have missed two free throws in a row! '
                               f'Claim your free chicken on the cfa app before midnight!'
                               f'(rewards may take up to 30 minutes from this announcement to show up on the cfa app)')
            clippers_freethrows.stop()
    else:
        return clippers_freethrows.stop()




bot.run(TOKEN)